# Architecture Documentation

## System Overview

The Visa Dispute Agent is an event-driven autonomous system that processes payment disputes through a sophisticated workflow combining RAG (Retrieval-Augmented Generation), fraud detection, and confidence-scored decision making.

## High-Level Architecture

```mermaid
graph TB
    subgraph "External Systems"
        PS[Payment Processor<br/>Stripe/Visa]
        ES[Enrichment Service<br/>Transaction History]
        GA[Gmail API<br/>Email Notifications]
    end
    
    subgraph "API Layer"
        API[FastAPI Server<br/>REST Endpoints]
    end
    
    subgraph "Orchestration Layer"
        LG[LangGraph<br/>State Machine]
    end
    
    subgraph "Processing Nodes"
        IN[Input Node<br/>Validation]
        EN[Enrichment Node<br/>Transaction History]
        LR[Legal Research Node<br/>RAG + Self-Correction]
        AD[Adjudication Node<br/>LLM Decision]
        AN[Action Node<br/>Email Sending]
        HR[Human Review Node<br/>Escalation]
    end
    
    subgraph "Tools & Services"
        RAG[RAG Retriever<br/>Query Rewriting]
        TE[Transaction Enrichment<br/>Fraud Detection]
        AL[Audit Logger<br/>PostgreSQL]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Audit & Queue)]
        CB[(ChromaDB<br/>Visa Rules)]
    end
    
    PS -->|Webhook| API
    API --> LG
    LG --> IN
    IN --> EN
    EN --> LR
    LR --> AD
    AD -->|High Confidence| AN
    AD -->|Low Confidence| HR
    
    EN --> TE
    TE --> ES
    LR --> RAG
    RAG --> CB
    AN --> GA
    
    IN --> AL
    EN --> AL
    LR --> AL
    AD --> AL
    AN --> AL
    HR --> AL
    
    AL --> PG
    HR --> PG
    
    style PS fill:#e1f5ff
    style ES fill:#e1f5ff
    style GA fill:#e1f5ff
    style API fill:#fff4e6
    style LG fill:#f3e5f5
    style AD fill:#e8f5e9
    style HR fill:#ffebee
    style PG fill:#fce4ec
    style CB fill:#fce4ec
```

## Workflow State Machine

```mermaid
stateDiagram-v2
    [*] --> Input
    Input --> Enrichment
    Enrichment --> LegalResearch
    
    LegalResearch --> SimilarityCheck
    SimilarityCheck --> LegalResearch: Low Similarity<br/>(< 0.7, attempts < 3)
    SimilarityCheck --> Adjudication: High Similarity<br/>(≥ 0.7)
    SimilarityCheck --> HumanReview: Max Attempts<br/>(3 attempts, still low)
    
    Adjudication --> ConfidenceCheck
    ConfidenceCheck --> Action: High Confidence<br/>(≥ 0.85)
    ConfidenceCheck --> HumanReview: Low Confidence<br/>(< 0.85)
    
    Action --> [*]
    HumanReview --> [*]
    
    note right of LegalResearch
        Self-Reflective RAG
        - Attempt 1: Entity extraction
        - Attempt 2: Category-based
        - Attempt 3: Reason code focus
    end note
    
    note right of Adjudication
        LLM Decision with
        - Validation retry (max 3)
        - Structured output
        - Confidence scoring
    end note
```

## Component Architecture

### 1. API Layer

```mermaid
graph LR
    subgraph "FastAPI Application"
        WH[Webhook Endpoint<br/>POST /webhooks/dispute]
        ST[Status Endpoint<br/>GET /disputes/:id]
        RQ[Review Queue<br/>GET /review-queue]
        HC[Health Check<br/>GET /health]
    end
    
    subgraph "Middleware"
        CORS[CORS Handler]
        VAL[Request Validator]
        ERR[Error Handler]
    end
    
    WH --> CORS
    ST --> CORS
    RQ --> CORS
    HC --> CORS
    
    CORS --> VAL
    VAL --> ERR
```

### 2. State Machine

```mermaid
graph TB
    subgraph "LangGraph State Machine"
        STATE[DisputeState<br/>TypedDict]
        
        subgraph "Nodes"
            N1[input_node]
            N2[enrichment_node]
            N3[legal_research_node]
            N4[adjudication_node]
            N5[action_node]
            N6[human_review_node]
        end
        
        subgraph "Conditional Edges"
            C1{similarity_check}
            C2{confidence_check}
        end
        
        STATE --> N1
        N1 --> N2
        N2 --> N3
        N3 --> C1
        C1 -->|Low| N3
        C1 -->|High| N4
        C1 -->|Max Attempts| N6
        N4 --> C2
        C2 -->|High| N5
        C2 -->|Low| N6
    end
```

### 3. RAG System

```mermaid
graph TB
    subgraph "RAG Retriever"
        QG[Query Generator]
        VS[Vector Search<br/>ChromaDB]
        SC[Similarity Calculator]
        QR[Query Rewriter]
        
        QG --> VS
        VS --> SC
        SC -->|< 0.7| QR
        QR --> QG
        SC -->|≥ 0.7| OUT[Return Results]
    end
    
    subgraph "Query Strategies"
        S1[Strategy 1:<br/>Entity Extraction]
        S2[Strategy 2:<br/>Category-Based]
        S3[Strategy 3:<br/>Reason Code Focus]
    end
    
    QR --> S1
    QR --> S2
    QR --> S3
```

### 4. Database Schema

```mermaid
erDiagram
    AUDIT_LOG {
        int id PK
        string dispute_id
        string node_name
        string event_type
        timestamp timestamp
        jsonb state_data
        text reasoning
        decimal confidence_score
        jsonb supporting_evidence
        text error_message
        timestamp created_at
    }
    
    HUMAN_REVIEW_QUEUE {
        int id PK
        string dispute_id UK
        decimal confidence_score
        string decision
        text reasoning
        jsonb supporting_rules
        string status
        jsonb payload
        timestamp created_at
        timestamp updated_at
        string reviewed_by
        timestamp reviewed_at
    }
    
    DISPUTE_HISTORY {
        int id PK
        string dispute_id UK
        jsonb payload
        string final_decision
        decimal confidence_score
        jsonb actions_taken
        string status
        timestamp completed_at
        timestamp created_at
        timestamp updated_at
    }
    
    AUDIT_LOG ||--o{ DISPUTE_HISTORY : "tracks"
    HUMAN_REVIEW_QUEUE ||--o| DISPUTE_HISTORY : "escalates"
```

## Data Flow

### Happy Path (High Confidence)

```mermaid
sequenceDiagram
    participant PS as Payment Processor
    participant API as FastAPI
    participant LG as LangGraph
    participant RAG as RAG Retriever
    participant LLM as LLM (GPT-4)
    participant DB as PostgreSQL
    participant Email as Gmail API
    
    PS->>API: POST /webhooks/dispute
    API->>API: Validate payload
    API->>LG: Initialize state
    
    LG->>DB: Log input node
    LG->>LG: Fetch transaction history
    LG->>DB: Log enrichment
    
    LG->>RAG: Query Visa rules
    RAG->>RAG: Calculate similarity
    RAG-->>LG: Return documents (score ≥ 0.7)
    LG->>DB: Log retrieval
    
    LG->>LLM: Request decision
    LLM-->>LG: Return decision (confidence ≥ 0.85)
    LG->>DB: Log decision
    
    LG->>Email: Send notification
    Email-->>LG: Confirm sent
    LG->>DB: Log action
    
    LG-->>API: Complete
    API-->>PS: 202 Accepted
```

### Self-Correction Path (Low Similarity)

```mermaid
sequenceDiagram
    participant LG as LangGraph
    participant RAG as RAG Retriever
    participant CB as ChromaDB
    participant DB as PostgreSQL
    
    LG->>RAG: Query (attempt 1)
    RAG->>CB: Vector search
    CB-->>RAG: Documents
    RAG->>RAG: Calculate similarity
    RAG-->>LG: Low similarity (< 0.7)
    
    LG->>RAG: Rewrite query (attempt 2)
    RAG->>RAG: Apply strategy 2
    RAG->>CB: Vector search
    CB-->>RAG: Documents
    RAG->>RAG: Calculate similarity
    RAG-->>LG: Still low (< 0.7)
    
    LG->>RAG: Rewrite query (attempt 3)
    RAG->>RAG: Apply strategy 3
    RAG->>CB: Vector search
    CB-->>RAG: Documents
    RAG->>RAG: Calculate similarity
    
    alt Similarity improved
        RAG-->>LG: High similarity (≥ 0.7)
        LG->>LG: Proceed to adjudication
    else Still low after 3 attempts
        RAG-->>LG: Low similarity
        LG->>DB: Route to human review
    end
```

### Escalation Path (Low Confidence)

```mermaid
sequenceDiagram
    participant LG as LangGraph
    participant LLM as LLM
    participant DB as PostgreSQL
    participant HR as Human Review Queue
    
    LG->>LLM: Request decision
    LLM-->>LG: Decision (confidence < 0.85)
    LG->>DB: Log decision
    
    LG->>LG: Check confidence threshold
    LG->>HR: Add to review queue
    HR->>DB: INSERT into human_review_queue
    DB-->>HR: Confirm
    HR-->>LG: Queued
    
    LG->>DB: Log escalation
    LG-->>LG: Complete workflow
```

## Deployment Architecture

### Local Development

```mermaid
graph TB
    subgraph "Developer Machine"
        CODE[Source Code]
        POETRY[Poetry<br/>Dependencies]
        
        subgraph "Docker Compose"
            PG[PostgreSQL<br/>:5432]
            CB[ChromaDB<br/>:8000]
        end
        
        APP[FastAPI App<br/>:8000]
    end
    
    CODE --> POETRY
    POETRY --> APP
    APP --> PG
    APP --> CB
```

### Production Deployment

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[NGINX/ALB]
    end
    
    subgraph "Application Tier"
        APP1[FastAPI Instance 1]
        APP2[FastAPI Instance 2]
        APP3[FastAPI Instance N]
    end
    
    subgraph "Data Tier"
        PG[(PostgreSQL<br/>Primary)]
        PGR[(PostgreSQL<br/>Replica)]
        CB[(ChromaDB<br/>Cluster)]
        REDIS[(Redis<br/>Cache)]
    end
    
    subgraph "External Services"
        LLM[OpenAI API]
        EMAIL[Gmail API]
        ENRICH[Enrichment Service]
    end
    
    subgraph "Monitoring"
        PROM[Prometheus]
        GRAF[Grafana]
        LOGS[ELK Stack]
    end
    
    LB --> APP1
    LB --> APP2
    LB --> APP3
    
    APP1 --> PG
    APP2 --> PG
    APP3 --> PG
    
    PG --> PGR
    
    APP1 --> CB
    APP2 --> CB
    APP3 --> CB
    
    APP1 --> REDIS
    APP2 --> REDIS
    APP3 --> REDIS
    
    APP1 --> LLM
    APP1 --> EMAIL
    APP1 --> ENRICH
    
    APP1 --> PROM
    APP2 --> PROM
    APP3 --> PROM
    
    PROM --> GRAF
    APP1 --> LOGS
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Network Security"
            TLS[TLS/HTTPS]
            FW[Firewall]
        end
        
        subgraph "Application Security"
            AUTH[API Key Auth]
            HMAC[Webhook Signature]
            RATE[Rate Limiting]
            VAL[Input Validation]
        end
        
        subgraph "Data Security"
            ENC[Encryption at Rest]
            AUDIT[Audit Logging]
            RBAC[Role-Based Access]
        end
    end
    
    TLS --> AUTH
    FW --> AUTH
    AUTH --> HMAC
    HMAC --> RATE
    RATE --> VAL
    VAL --> ENC
    ENC --> AUDIT
    AUDIT --> RBAC
```

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers
- Shared database and vector store
- Load balancer distribution
- Connection pooling

### Vertical Scaling
- Increase database resources
- Optimize ChromaDB index
- Cache frequently accessed rules
- Batch processing

### Performance Optimization
- Async operations throughout
- Database query optimization
- Vector search tuning
- LLM response caching

## Monitoring & Observability

```mermaid
graph LR
    subgraph "Application"
        APP[FastAPI App]
    end
    
    subgraph "Metrics"
        PROM[Prometheus]
        GRAF[Grafana]
    end
    
    subgraph "Logs"
        LOGS[Structured Logs]
        ELK[ELK Stack]
    end
    
    subgraph "Tracing"
        TRACE[Correlation IDs]
        JAEGER[Jaeger]
    end
    
    subgraph "Alerts"
        ALERT[Alert Manager]
        SLACK[Slack/PagerDuty]
    end
    
    APP --> PROM
    APP --> LOGS
    APP --> TRACE
    
    PROM --> GRAF
    LOGS --> ELK
    TRACE --> JAEGER
    
    PROM --> ALERT
    ALERT --> SLACK
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API | FastAPI | REST API server |
| Orchestration | LangGraph | State machine workflow |
| LLM | LangChain + OpenAI | Decision making |
| Validation | Pydantic v2 | Schema validation |
| Database | PostgreSQL + AsyncPG | Audit & queue storage |
| Vector Store | ChromaDB | Visa rules search |
| Testing | Pytest + Hypothesis | Property-based testing |
| Deployment | Docker + Docker Compose | Containerization |
| Migrations | Alembic | Database versioning |

## Design Patterns Used

1. **State Machine Pattern** - LangGraph for workflow management
2. **Repository Pattern** - Database abstraction layer
3. **Strategy Pattern** - Multiple query rewriting strategies
4. **Retry Pattern** - Exponential backoff for failures
5. **Circuit Breaker Pattern** - External service protection (planned)
6. **Observer Pattern** - Audit logging for all events
7. **Factory Pattern** - State initialization
8. **Template Method Pattern** - Node execution flow

## Future Enhancements

1. **Caching Layer** - Redis for frequently accessed data
2. **Message Queue** - RabbitMQ/Kafka for async processing
3. **GraphQL API** - Alternative to REST
4. **WebSocket Support** - Real-time updates
5. **Multi-tenancy** - Support multiple organizations
6. **A/B Testing** - Experiment with different strategies
7. **ML Model Training** - Learn from human reviews
8. **Batch Processing** - Handle multiple disputes efficiently
