"""LangGraph state machine for dispute resolution workflow"""
from typing import Literal
from langgraph.graph import StateGraph, END
from app.schema.state import DisputeState
from app.schema.models import DisputeDecision, DisputeWebhook
from app.tools.rag_retriever import RAGRetriever
from app.tools.transaction_enrichment import TransactionEnrichment
from app.db.audit_logger import audit_logger
from app.db.human_review import add_to_review_queue
from app.config.settings import settings


# Initialize LLM - using Ollama (free, local)
from langchain_ollama import ChatOllama
llm = ChatOllama(
    model=settings.llm_model,
    temperature=0,
    base_url="http://host.docker.internal:11434"
)

# Initialize tools
rag_retriever = RAGRetriever(llm, similarity_threshold=settings.similarity_threshold)
transaction_enrichment = TransactionEnrichment(settings.enrichment_api_url)


async def input_node(state: DisputeState) -> DisputeState:
    """Initialize state from webhook payload"""
    await audit_logger.log_node_entry(
        state["dispute_id"],
        "input_node",
        {"payload": state["payload"]}
    )
    
    state["current_node"] = "input_node"
    state["actions_taken"] = []
    state["query_attempts"] = 0
    
    return state


async def enrichment_node(state: DisputeState) -> DisputeState:
    """Enrich dispute with transaction history"""
    await audit_logger.log_node_entry(
        state["dispute_id"],
        "enrichment_node",
        {"customer_id": state["payload"].get("customer_id")}
    )
    
    try:
        customer_id = state["payload"]["customer_id"]
        transactions = await transaction_enrichment.fetch_history(customer_id, years=3)
        
        state["transaction_history"] = transactions
        state["current_node"] = "enrichment_node"
        state["actions_taken"].append("transaction_history_fetched")
        
    except Exception as e:
        await audit_logger.log_error(
            state["dispute_id"],
            "enrichment_node",
            str(e),
            state
        )
        state["error"] = f"Enrichment failed: {str(e)}"
    
    return state


async def legal_research_node(state: DisputeState) -> DisputeState:
    """Perform RAG-based legal research"""
    await audit_logger.log_node_entry(
        state["dispute_id"],
        "legal_research_node",
        {"query_attempts": state["query_attempts"]}
    )
    
    try:
        # Generate initial query from dispute details
        dispute_desc = state["payload"].get("description", "")
        reason_code = state["payload"].get("reason_code", "")
        amount = state["payload"].get("amount", "")
        
        initial_query = f"Visa dispute reason code {reason_code}: {dispute_desc}. Amount: {amount}"
        
        # Perform retrieval with self-correction
        result, attempts = await rag_retriever.retrieve_with_self_correction(
            initial_query,
            state["payload"],
            max_attempts=3
        )
        
        # Convert Document objects to dicts for JSON serialization
        state["retrieved_rules"] = [
            {"content": doc.content, "metadata": doc.metadata, "similarity_score": doc.similarity_score}
            for doc in result.documents
        ]
        state["similarity_scores"] = [doc.similarity_score for doc in result.documents]
        state["query_attempts"] = attempts
        state["current_node"] = "legal_research_node"
        state["actions_taken"].append(f"rag_retrieval_completed_{attempts}_attempts")
        
        await audit_logger.log_retrieval(
            state["dispute_id"],
            result.query,
            [{"content": doc.content, "metadata": doc.metadata} for doc in result.documents],
            state["similarity_scores"]
        )
        
    except Exception as e:
        await audit_logger.log_error(
            state["dispute_id"],
            "legal_research_node",
            str(e),
            state
        )
        state["error"] = f"Legal research failed: {str(e)}"
    
    return state


async def adjudication_node(state: DisputeState) -> DisputeState:
    """Make adjudication decision using LLM with structured output and validation retry"""
    await audit_logger.log_node_entry(
        state["dispute_id"],
        "adjudication_node",
        {"num_rules": len(state.get("retrieved_rules", []))}
    )
    
    try:
        # Build context from retrieved rules (now dicts)
        rules_context = "\n\n".join([
            f"Rule {i+1}: {doc['content']}"
            for i, doc in enumerate(state.get("retrieved_rules", []))
        ])
        
        # Analyze fraud patterns
        fraud_analysis = None
        if state.get("transaction_history"):
            fraud_analysis = transaction_enrichment.detect_fraud_patterns(
                state["transaction_history"],
                state["payload"]["amount"]
            )
        
        fraud_context = ""
        if fraud_analysis:
            fraud_context = f"""
Fraud Analysis:
- Chargeback Rate: {fraud_analysis.chargeback_rate:.2%}
- Risk Score: {fraud_analysis.risk_score:.2f}
- Suspicious Patterns: {fraud_analysis.has_suspicious_patterns}
- Pattern Details: {', '.join(fraud_analysis.pattern_details) if fraud_analysis.pattern_details else 'None detected'}
"""
        
        # Try to generate valid decision with retry logic
        decision = None
        max_attempts = 3
        validation_errors = []
        
        for attempt in range(max_attempts):
            try:
                # Create adjudication prompt
                error_context = ""
                if validation_errors:
                    error_context = f"""
IMPORTANT: Previous attempt failed validation with these errors:
{chr(10).join(f'- {err}' for err in validation_errors)}

Please correct these issues in your response.
"""
                
                prompt = f"""You are a Visa dispute adjudication specialist. Analyze this dispute and make a decision.

Dispute Details:
- Dispute ID: {state['dispute_id']}
- Customer ID: {state['payload']['customer_id']}
- Transaction ID: {state['payload']['transaction_id']}
- Amount: {state['payload']['amount']} {state['payload']['currency']}
- Reason Code: {state['payload']['reason_code']}
- Description: {state['payload']['description']}

{fraud_context}

Relevant Visa Rules:
{rules_context}

{error_context}

Based on the evidence, make a decision:
1. "accept" - Accept the dispute (refund customer)
2. "reject" - Reject the dispute (merchant wins)
3. "escalate" - Escalate to human review

CRITICAL: Provide your response as VALID JSON ONLY, no additional text:
{{
    "decision": "accept|reject|escalate",
    "confidence_score": 0.85,
    "reasoning": "detailed explanation of at least 20 characters",
    "supporting_rules": ["rule reference 1", "rule reference 2"],
    "recommended_action": "specific action to take"
}}

Rules:
- decision must be exactly one of: "accept", "reject", or "escalate"
- confidence_score must be a number between 0.0 and 1.0
- reasoning must be at least 20 characters
- supporting_rules must be an array of strings
- recommended_action must be a non-empty string"""
                
                # Generate decision
                response = await llm.ainvoke(prompt)
                
                # Parse JSON response
                import json
                import re
                
                # Extract JSON from response (handle cases where LLM adds extra text)
                content = response.content.strip()
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    content = json_match.group(0)
                
                decision_data = json.loads(content)
                decision_data["dispute_id"] = state["dispute_id"]
                
                # Validate with Pydantic
                decision = DisputeDecision(**decision_data)
                
                # Success! Break out of retry loop
                break
                
            except (json.JSONDecodeError, ValueError) as e:
                validation_errors.append(f"JSON parsing error: {str(e)}")
                if attempt == max_attempts - 1:
                    raise ValueError(f"Failed to generate valid decision after {max_attempts} attempts: {validation_errors}")
            except Exception as e:
                validation_errors.append(f"Validation error: {str(e)}")
                if attempt == max_attempts - 1:
                    raise ValueError(f"Failed to generate valid decision after {max_attempts} attempts: {validation_errors}")
        
        if not decision:
            raise ValueError("Failed to generate decision")
        
        # Convert DisputeDecision to dict for JSON serialization
        state["decision"] = decision.model_dump()
        state["confidence_score"] = decision.confidence_score
        state["current_node"] = "adjudication_node"
        state["actions_taken"].append("decision_made")
        
        await audit_logger.log_decision(state["dispute_id"], decision)
        
    except Exception as e:
        await audit_logger.log_error(
            state["dispute_id"],
            "adjudication_node",
            str(e),
            state
        )
        state["error"] = f"Adjudication failed: {str(e)}"
    
    return state


async def action_node(state: DisputeState) -> DisputeState:
    """Execute actions (send email) with real email service"""
    await audit_logger.log_node_entry(
        state["dispute_id"],
        "action_node",
        {"decision": state.get("decision")}
    )
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            decision = state["decision"]  # Now a dict
            
            # Get customer email from payload
            customer_email = state["payload"].get("customer_email", "customer@example.com")
            customer_name = state["payload"].get("customer_name", "Customer")
            amount = state["payload"].get("amount", 0)
            currency = state["payload"].get("currency", "INR")
            
            # Convert amount to float if it's a string
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                amount = 0.0
            
            # Send real email using unified email service (tries multiple providers)
            from app.tools.unified_email_service import unified_email_service
            
            result = unified_email_service.send_dispute_decision(
                to_email=customer_email,
                dispute_id=state["dispute_id"],
                customer_name=customer_name,
                decision=decision['decision'],
                reasoning=decision['reasoning'],
                amount=amount,
                currency=currency
            )
            
            if result['success']:
                # Email sent successfully
                from datetime import datetime
                email_metadata = {
                    "recipient": customer_email,
                    "subject": f"Dispute Resolution - {state['dispute_id']}",
                    "sent_at": datetime.utcnow().isoformat(),
                    "attempt": retry_count + 1,
                    "method": "smtp_gmail",
                    "status": "sent"
                }
                
                state["actions_taken"].append(f"email_sent_attempt_{retry_count + 1}")
                state["current_node"] = "action_node"
                
                await audit_logger.log_action(
                    state["dispute_id"],
                    "email_sent",
                    email_metadata
            )
            
            # Success - break out of retry loop
            break
            
        except Exception as e:
            retry_count += 1
            await audit_logger.log_error(
                state["dispute_id"],
                "action_node",
                f"Email send attempt {retry_count} failed: {str(e)}",
                state
            )
            
            if retry_count >= max_retries:
                # All retries exhausted - route to human review
                state["error"] = f"Action execution failed after {max_retries} attempts: {str(e)}"
                state["actions_taken"].append("email_failed_routing_to_human_review")
                # The routing logic will handle sending to human review
                break
            
            # Exponential backoff
            import asyncio
            await asyncio.sleep(2 ** retry_count)
    
    return state


async def human_review_node(state: DisputeState) -> DisputeState:
    """Route to human review queue"""
    await audit_logger.log_node_entry(
        state["dispute_id"],
        "human_review_node",
        {"reason": "low_confidence" if state.get("confidence_score") else "error"}
    )
    
    try:
        decision = state.get("decision")
        if not decision:
            # Create placeholder decision dict for error cases
            decision = {
                "dispute_id": state["dispute_id"],
                "decision": "escalate",
                "confidence_score": 0.0,
                "reasoning": state.get("error", "Processing error occurred - requires human review"),
                "supporting_rules": [],
                "recommended_action": "human_review"
            }
        elif isinstance(decision, dict):
            # Ensure reasoning is never null/empty
            if not decision.get("reasoning"):
                decision["reasoning"] = "Low confidence decision - requires human review for final determination"
        
        await add_to_review_queue(
            state["dispute_id"],
            decision,
            state["payload"]
        )
        
        # Send email notification for human review cases too
        customer_email = state["payload"].get("customer_email")
        if customer_email:
            from app.tools.email_service import email_service
            
            customer_name = state["payload"].get("customer_name", "Customer")
            amount = state["payload"].get("amount", 0)
            currency = state["payload"].get("currency", "INR")
            
            reasoning_text = decision.get("reasoning", "") if isinstance(decision, dict) else decision.reasoning
            decision_value = decision.get("decision", "escalate") if isinstance(decision, dict) else decision.decision
            
            # Send email about escalation
            from app.tools.unified_email_service import unified_email_service
            
            email_result = unified_email_service.send_dispute_decision(
                to_email=customer_email,
                dispute_id=state["dispute_id"],
                customer_name=customer_name,
                decision="under_review",  # Special status for human review
                reasoning=f"Your dispute requires specialist review. {reasoning_text}\n\nExpected resolution within 24-48 hours.",
                amount=float(amount),
                currency=currency
            )
            
            if email_result['success']:
                state["actions_taken"].append("email_sent_human_review")
        
        state["actions_taken"].append("routed_to_human_review")
        state["current_node"] = "human_review_node"
        
    except Exception as e:
        await audit_logger.log_error(
            state["dispute_id"],
            "human_review_node",
            str(e),
            state
        )
    
    return state


# Conditional routing functions
def should_rewrite_query(state: DisputeState) -> Literal["rewrite", "proceed"]:
    """Check if RAG retrieval quality is sufficient"""
    if state.get("error"):
        return "escalate"
    
    similarity_scores = state.get("similarity_scores", [])
    if not similarity_scores:
        return "escalate"
    
    avg_similarity = sum(similarity_scores) / len(similarity_scores)
    query_attempts = state.get("query_attempts", 0)
    
    # If quality is low and haven't exhausted attempts, rewrite
    if avg_similarity < settings.similarity_threshold and query_attempts < 3:
        return "rewrite"
    
    # If exhausted attempts with low quality, escalate
    if avg_similarity < settings.similarity_threshold:
        return "escalate"
    
    return "proceed"


def route_by_confidence(state: DisputeState) -> Literal["action", "human_review"]:
    """Route based on confidence score"""
    if state.get("error"):
        return "human_review"
    
    confidence = state.get("confidence_score", 0.0)
    
    if confidence >= settings.confidence_threshold:
        return "action"
    else:
        return "human_review"


# Build the state graph
def create_dispute_graph() -> StateGraph:
    """Create and compile the dispute resolution state graph"""
    workflow = StateGraph(DisputeState)
    
    # Add nodes
    workflow.add_node("input", input_node)
    workflow.add_node("enrichment", enrichment_node)
    workflow.add_node("legal_research", legal_research_node)
    workflow.add_node("adjudication", adjudication_node)
    workflow.add_node("action", action_node)
    workflow.add_node("human_review", human_review_node)
    
    # Add edges
    workflow.set_entry_point("input")
    workflow.add_edge("input", "enrichment")
    workflow.add_edge("enrichment", "legal_research")
    
    # Conditional edge after legal research
    workflow.add_conditional_edges(
        "legal_research",
        should_rewrite_query,
        {
            "rewrite": "legal_research",  # Self-loop for query rewriting
            "proceed": "adjudication",
            "escalate": "human_review"
        }
    )
    
    # Conditional edge after adjudication
    workflow.add_conditional_edges(
        "adjudication",
        route_by_confidence,
        {
            "action": "action",
            "human_review": "human_review"
        }
    )
    
    # Terminal nodes
    workflow.add_edge("action", END)
    workflow.add_edge("human_review", END)
    
    return workflow.compile()


# Global graph instance
dispute_graph = create_dispute_graph()
