-- Audit log table for complete agent reasoning trail
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    dispute_id VARCHAR(255) NOT NULL,
    node_name VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    state_data JSONB,
    reasoning TEXT,
    confidence_score DECIMAL(3, 2),
    supporting_evidence JSONB,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_log_dispute_id ON audit_log(dispute_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_log_node_name ON audit_log(node_name);

-- Human review queue for low-confidence cases
CREATE TABLE IF NOT EXISTS human_review_queue (
    id SERIAL PRIMARY KEY,
    dispute_id VARCHAR(255) UNIQUE NOT NULL,
    confidence_score DECIMAL(3, 2) NOT NULL,
    decision VARCHAR(50) NOT NULL,
    reasoning TEXT NOT NULL,
    supporting_rules JSONB,
    status VARCHAR(50) NOT NULL DEFAULT 'pending_review',
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    reviewed_by VARCHAR(255),
    reviewed_at TIMESTAMP
);

CREATE INDEX idx_human_review_status ON human_review_queue(status);
CREATE INDEX idx_human_review_created_at ON human_review_queue(created_at);

-- Dispute history for all processed disputes
CREATE TABLE IF NOT EXISTS dispute_history (
    id SERIAL PRIMARY KEY,
    dispute_id VARCHAR(255) UNIQUE NOT NULL,
    payload JSONB NOT NULL,
    final_decision VARCHAR(50),
    confidence_score DECIMAL(3, 2),
    actions_taken JSONB,
    status VARCHAR(50) NOT NULL,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_dispute_history_dispute_id ON dispute_history(dispute_id);
CREATE INDEX idx_dispute_history_status ON dispute_history(status);
CREATE INDEX idx_dispute_history_created_at ON dispute_history(created_at);
