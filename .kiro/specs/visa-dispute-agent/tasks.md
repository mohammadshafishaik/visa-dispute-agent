# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create modular folder structure: /app/agents, /app/tools, /app/schema, /app/db, /app/api, /app/config
  - Initialize Python 3.11+ project with pyproject.toml
  - Install core dependencies: FastAPI, LangGraph, LangChain, Pydantic v2, ChromaDB, AsyncPG, pytest, hypothesis
  - Configure development environment with pre-commit hooks and linting
  - _Requirements: 9.1, 9.2, 9.3_

- [x] 2. Implement Pydantic schemas and data models
  - Create DisputeWebhook schema with all required fields (dispute_id, customer_id, transaction_id, amount, currency, reason_code, description, timestamp)
  - Create DisputeDecision schema with decision type, confidence_score, reasoning, supporting_rules, recommended_action
  - Create TransactionData schema for enrichment service responses
  - Create RetrievalResult schema for RAG outputs with documents and similarity_scores
  - Create DisputeState TypedDict for LangGraph state management
  - _Requirements: 1.2, 4.2, 8.4, 8.5_

- [x]* 2.1 Write property test for schema validation
  - **Property 1: Webhook payload validation**
  - **Validates: Requirements 1.2, 1.3**

- [x] 3. Set up database layer
  - Create PostgreSQL connection pool using AsyncPG
  - Define database schema for audit_log table (dispute_id, node_name, timestamp, state_data, event_type)
  - Define database schema for human_review_queue table (dispute_id, confidence_score, decision, status, created_at)
  - Define database schema for dispute_history table (dispute_id, payload, final_decision, actions_taken, completed_at)
  - Implement AuditLogger class with async methods for logging node entries, decisions, and actions
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 4.5_

- [ ]* 3.1 Write property test for audit trail completeness
  - **Property 3: Audit trail completeness**
  - **Validates: Requirements 1.5, 7.1, 7.2, 7.3, 7.4**

- [x] 4. Initialize ChromaDB vector store
  - Set up ChromaDB client connection
  - Create collection for Visa rules with embedding function
  - Implement script to seed ChromaDB with sample Visa regulations
  - Create utility functions for adding and querying documents
  - _Requirements: 9.4_

- [x] 5. Implement RAG retriever tool
  - Create RAGRetriever class with async retrieve() method
  - Implement similarity score calculation for retrieved documents
  - Implement query rewriting logic with multiple strategies (entity extraction, synonyms, category-based)
  - Add self-correction loop that rewrites queries when similarity < 0.7
  - Limit query rewriting to maximum 3 attempts
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 10.1, 10.2, 10.3, 10.4_

- [x]* 5.1 Write property test for similarity score calculation
  - **Property 8: Similarity score calculation**
  - **Validates: Requirements 3.2, 10.1**

- [x]* 5.2 Write property test for self-reflective query rewriting
  - **Property 9: Self-reflective query rewriting**
  - **Validates: Requirements 3.3, 3.4, 10.2, 10.3, 10.4**

- [x]* 5.3 Write property test for RAG query generation
  - **Property 7: RAG query generation**
  - **Validates: Requirements 3.1**

- [x] 6. Implement transaction enrichment tool
  - Create TransactionEnrichment class with async fetch_history() method
  - Implement mock Enrichment Service API client (or real client if available)
  - Add 3-year date range calculation for transaction history requests
  - Implement detect_fraud_patterns() method to analyze transaction history
  - Add retry logic with exponential backoff for API timeouts
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ]* 6.1 Write property test for enrichment service invocation
  - **Property 4: Enrichment service invocation**
  - **Validates: Requirements 2.1, 2.2**

- [x]* 6.2 Write property test for retry with exponential backoff
  - **Property 6: Retry with exponential backoff**
  - **Validates: Requirements 2.4, 5.4, 6.2**

- [x] 7. Implement LangGraph state machine
  - Define DisputeState TypedDict with all required fields
  - Create input_node function to initialize state from webhook
  - Create enrichment_node function to call TransactionEnrichment tool
  - Create legal_research_node function to call RAGRetriever tool
  - Create adjudication_node function to make decisions using LLM
  - Create action_node function to draft and send emails
  - Create human_review_node function to write to review queue
  - _Requirements: 6.1, 6.3_

- [x]* 7.1 Write property test for state initialization completeness
  - **Property 2: State initialization completeness**
  - **Validates: Requirements 1.4**

- [x] 8. Implement conditional routing logic
  - Create similarity_check conditional edge (routes to query rewrite if < 0.7, else to adjudication)
  - Create confidence_check conditional edge (routes to human review if < 0.85, else to action)
  - Create retry_exhausted conditional edge (routes to human review after max attempts)
  - Implement routing functions that evaluate state and return next node name
  - _Requirements: 3.5, 4.4, 5.1, 6.3, 6.4, 6.5_

- [x]* 8.1 Write property test for high-quality retrieval progression
  - **Property 10: High-quality retrieval progression**
  - **Validates: Requirements 3.5**

- [x]* 8.2 Write property test for confidence-based routing
  - **Property 12: Confidence-based routing**
  - **Validates: Requirements 4.4, 5.1**

- [x]* 8.3 Write property test for conditional routing correctness
  - **Property 16: Conditional routing correctness**
  - **Validates: Requirements 6.3, 6.4**

- [x] 9. Implement adjudication node with LLM integration
  - Set up LangChain LLM client (OpenAI/Anthropic)
  - Create prompt template for dispute adjudication with retrieved rules
  - Implement structured output generation using Pydantic schema binding
  - Add validation retry logic (up to 3 attempts with corrective prompts)
  - Extract confidence score from LLM response
  - _Requirements: 4.1, 4.2, 4.3, 8.1, 8.2_

- [x]* 9.1 Write property test for adjudication decision structure
  - **Property 11: Adjudication decision structure**
  - **Validates: Requirements 4.2, 4.3, 8.4**

- [x]* 9.2 Write property test for schema validation enforcement
  - **Property 18: Schema validation enforcement**
  - **Validates: Requirements 8.1, 8.5**

- [x]* 9.3 Write property test for validation retry with correction
  - **Property 19: Validation retry with correction**
  - **Validates: Requirements 8.2**

- [x] 10. Implement human review queue functionality
  - Create function to write dispute to human_review_queue table with status "pending_review"
  - Include all case details: dispute_id, confidence_score, decision, reasoning, supporting_rules
  - Add timestamp and metadata fields
  - Implement query endpoint to retrieve pending cases
  - _Requirements: 4.5_

- [x]* 10.1 Write property test for human review queue persistence
  - **Property 13: Human review queue persistence**
  - **Validates: Requirements 4.5**

- [x]* 10.2 Write property test for failure escalation
  - **Property 17: Failure escalation**
  - **Validates: Requirements 6.5, 8.3, 10.5**

- [ ] 11. Implement action node with Gmail integration
  - Set up Gmail API client with OAuth credentials
  - Create email template function that formats DisputeDecision into email body
  - Implement async send_email() function with Gmail API call
  - Add retry logic for Gmail API failures (up to 3 attempts)
  - Route to human review queue if all email attempts fail
  - Log email metadata (recipient, subject, message_id) to audit trail
  - _Requirements: 5.2, 5.3, 5.4, 5.5_

- [ ]* 11.1 Write property test for email action execution
  - **Property 14: Email action execution**
  - **Validates: Requirements 5.2, 5.3**

- [ ]* 11.2 Write property test for action logging with metadata
  - **Property 15: Action logging with metadata**
  - **Validates: Requirements 5.5**

- [x] 12. Wire up complete LangGraph workflow
  - Create StateGraph instance with all nodes
  - Add edges between nodes: input → enrichment → legal_research → adjudication → action
  - Add conditional edges: similarity_check, confidence_check, retry_exhausted
  - Add self-loop edge from legal_research back to itself for query rewriting
  - Compile graph and test state transitions
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 12.1 Write property test for enrichment state update
  - **Property 5: Enrichment state update**
  - **Validates: Requirements 2.3, 2.5**

- [x] 13. Implement FastAPI server and endpoints
  - Create FastAPI app instance with CORS and middleware
  - Implement POST /webhooks/dispute endpoint to receive webhooks
  - Validate incoming webhooks with DisputeWebhook schema
  - Return HTTP 400 for validation failures with error details
  - Invoke LangGraph workflow for valid disputes
  - Implement GET /disputes/{dispute_id} endpoint to query status
  - Implement GET /health endpoint for health checks
  - Implement GET /review-queue endpoint to list pending cases
  - _Requirements: 1.1, 1.2, 1.3, 9.1, 9.5_

- [x]* 13.1 Write property test for transaction data schema conformance
  - **Property 20: Transaction data schema conformance**
  - **Validates: Requirements 8.5**

- [ ] 14. Add error handling and logging
  - Implement try-catch blocks in all node functions
  - Add error logging with full stack traces
  - Implement circuit breaker pattern for external services
  - Add graceful degradation for non-critical failures
  - Ensure all errors are logged to audit trail
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 15. Create configuration management
  - Implement config module to load environment variables
  - Add validation for required configuration (DATABASE_URL, CHROMADB_HOST, etc.)
  - Create configuration classes for different environments (dev, staging, prod)
  - Add sensible defaults for optional configuration
  - _Requirements: 9.2_

- [x] 16. Set up database migrations
  - Install and configure Alembic for PostgreSQL migrations
  - Create initial migration for audit_log, human_review_queue, and dispute_history tables
  - Add migration for indexes on frequently queried columns
  - Create seed script for ChromaDB with sample Visa rules
  - _Requirements: 9.2_

- [ ] 17. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 18. Add integration tests
  - Create end-to-end test for happy path (webhook → high confidence → email sent)
  - Create test for self-correction path (low similarity → query rewrite → success)
  - Create test for human escalation path (low confidence → review queue)
  - Create test for retry logic (API timeout → backoff → success)
  - Create test for failure escalation (max retries → review queue)
  - Use Docker Compose for test databases (PostgreSQL, ChromaDB)
  - _Requirements: All requirements (integration validation)_

- [ ] 19. Add monitoring and observability
  - Implement structured JSON logging with correlation IDs
  - Add metrics collection for request rate, latency, error rate
  - Track human review queue depth metric
  - Track RAG retrieval quality metrics (average similarity scores)
  - Track confidence score distribution
  - Add health check endpoint with database connectivity checks
  - _Requirements: 9.1_

- [ ] 20. Create deployment documentation
  - Document required environment variables
  - Create Docker Compose file for local development
  - Create Dockerfile for production deployment
  - Document database setup and migration process
  - Add README with setup instructions and architecture overview
  - _Requirements: 9.1, 9.2_

- [ ] 21. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
