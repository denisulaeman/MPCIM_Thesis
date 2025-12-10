-- MPCIM Thesis - Database Schema
-- PostgreSQL Database Schema for Production Deployment
-- Author: Deni Sulaeman
-- Date: November 22, 2025

-- ============================================================================
-- 1. EMPLOYEES TABLE (Master Data)
-- ============================================================================

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    department VARCHAR(100),
    position VARCHAR(100),
    
    -- Performance Metrics
    performance_score DECIMAL(5,2),
    performance_rating VARCHAR(50),
    
    -- Behavioral Metrics
    behavioral_score DECIMAL(5,2),
    collaboration_score DECIMAL(5,2),
    leadership_score DECIMAL(5,2),
    
    -- Demographic
    gender VARCHAR(20),
    marital_status VARCHAR(50),
    age INTEGER,
    tenure_years DECIMAL(5,2),
    is_permanent BOOLEAN DEFAULT TRUE,
    
    -- Quick Assessment (if available)
    has_quick_assessment BOOLEAN DEFAULT FALSE,
    psychological_score DECIMAL(5,2),
    drive_score DECIMAL(5,2),
    mental_strength_score DECIMAL(5,2),
    adaptability_score DECIMAL(5,2),
    
    -- Promotion Status
    has_promotion BOOLEAN DEFAULT FALSE,
    promotion_date DATE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Indexes for performance
CREATE INDEX idx_employees_employee_id ON employees(employee_id);
CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_employees_has_promotion ON employees(has_promotion);
CREATE INDEX idx_employees_is_active ON employees(is_active);

-- ============================================================================
-- 2. PREDICTIONS TABLE (Prediction Logs)
-- ============================================================================

CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    
    -- Prediction Details
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    prediction INTEGER NOT NULL, -- 0 or 1
    probability DECIMAL(5,4) NOT NULL,
    confidence_level VARCHAR(20), -- High, Medium, Low
    
    -- Input Features (JSON for flexibility)
    input_features JSONB,
    
    -- SHAP Explanation (optional)
    shap_values JSONB,
    top_contributing_features JSONB,
    
    -- Threshold Info
    threshold_used DECIMAL(5,4) DEFAULT 0.70,
    distance_from_threshold DECIMAL(5,4),
    
    -- Metadata
    predicted_by VARCHAR(255), -- HR user who made prediction
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Actual Outcome (for model monitoring)
    actual_outcome INTEGER, -- NULL until known
    outcome_date DATE,
    is_correct BOOLEAN,
    
    -- Foreign Key
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_predictions_employee_id ON predictions(employee_id);
CREATE INDEX idx_predictions_model_name ON predictions(model_name);
CREATE INDEX idx_predictions_predicted_at ON predictions(predicted_at);
CREATE INDEX idx_predictions_prediction ON predictions(prediction);

-- ============================================================================
-- 3. USERS TABLE (HR Users)
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- User Info
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'hr_user', -- admin, hr_user, viewer
    department VARCHAR(100),
    
    -- Permissions
    can_predict BOOLEAN DEFAULT TRUE,
    can_view_all BOOLEAN DEFAULT FALSE,
    can_export BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================================================
-- 4. AUDIT_LOGS TABLE (Activity Tracking)
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    username VARCHAR(100),
    
    -- Action Details
    action VARCHAR(100) NOT NULL, -- predict, view, export, update
    entity_type VARCHAR(50), -- employee, prediction, model
    entity_id VARCHAR(100),
    
    -- Details
    description TEXT,
    metadata JSONB,
    
    -- Request Info
    ip_address VARCHAR(50),
    user_agent TEXT,
    
    -- Timestamp
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- ============================================================================
-- 5. MODEL_PERFORMANCE TABLE (Model Monitoring)
-- ============================================================================

CREATE TABLE IF NOT EXISTS model_performance (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    
    -- Performance Metrics
    accuracy DECIMAL(5,4),
    precision_score DECIMAL(5,4),
    recall DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    roc_auc DECIMAL(5,4),
    
    -- Confusion Matrix
    true_positives INTEGER,
    true_negatives INTEGER,
    false_positives INTEGER,
    false_negatives INTEGER,
    
    -- Threshold Info
    threshold DECIMAL(5,4) DEFAULT 0.70,
    
    -- Dataset Info
    test_size INTEGER,
    train_size INTEGER,
    
    -- Metadata
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- Indexes
CREATE INDEX idx_model_performance_model_name ON model_performance(model_name);
CREATE INDEX idx_model_performance_evaluation_date ON model_performance(evaluation_date);

-- ============================================================================
-- 6. AI_ANALYSIS_CACHE TABLE (Cache Gemini AI Results)
-- ============================================================================

CREATE TABLE IF NOT EXISTS ai_analysis_cache (
    id SERIAL PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    
    -- Analysis Details
    analysis_type VARCHAR(100), -- model_performance, data_explorer, eda
    input_hash VARCHAR(64), -- MD5 hash of input data
    
    -- AI Response
    ai_provider VARCHAR(50), -- gemini, openai
    ai_model VARCHAR(100),
    analysis_result TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0,
    
    -- Cost tracking (optional)
    tokens_used INTEGER,
    cost_usd DECIMAL(10,6)
);

-- Indexes
CREATE INDEX idx_ai_cache_key ON ai_analysis_cache(cache_key);
CREATE INDEX idx_ai_cache_type ON ai_analysis_cache(analysis_type);
CREATE INDEX idx_ai_cache_expires_at ON ai_analysis_cache(expires_at);

-- ============================================================================
-- 7. FEEDBACK TABLE (User Feedback on Predictions)
-- ============================================================================

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    prediction_id INTEGER NOT NULL,
    employee_id VARCHAR(50) NOT NULL,
    
    -- Feedback Details
    user_id INTEGER,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    is_accurate BOOLEAN,
    comments TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes
CREATE INDEX idx_feedback_prediction_id ON feedback(prediction_id);
CREATE INDEX idx_feedback_employee_id ON feedback(employee_id);

-- ============================================================================
-- 8. VIEWS (Useful Queries)
-- ============================================================================

-- View: Recent Predictions with Employee Info
CREATE OR REPLACE VIEW v_recent_predictions AS
SELECT 
    p.id,
    p.employee_id,
    e.name,
    e.department,
    e.position,
    p.model_name,
    p.prediction,
    p.probability,
    p.confidence_level,
    p.predicted_at,
    p.predicted_by,
    p.actual_outcome,
    p.is_correct
FROM predictions p
JOIN employees e ON p.employee_id = e.employee_id
ORDER BY p.predicted_at DESC;

-- View: Model Performance Summary
CREATE OR REPLACE VIEW v_model_performance_summary AS
SELECT 
    model_name,
    model_version,
    AVG(accuracy) as avg_accuracy,
    AVG(precision_score) as avg_precision,
    AVG(recall) as avg_recall,
    AVG(f1_score) as avg_f1,
    COUNT(*) as evaluation_count,
    MAX(evaluation_date) as last_evaluation
FROM model_performance
GROUP BY model_name, model_version
ORDER BY last_evaluation DESC;

-- View: Prediction Accuracy by Model
CREATE OR REPLACE VIEW v_prediction_accuracy AS
SELECT 
    model_name,
    COUNT(*) as total_predictions,
    SUM(CASE WHEN is_correct = TRUE THEN 1 ELSE 0 END) as correct_predictions,
    ROUND(
        SUM(CASE WHEN is_correct = TRUE THEN 1 ELSE 0 END)::NUMERIC / 
        NULLIF(COUNT(*), 0) * 100, 
        2
    ) as accuracy_percentage
FROM predictions
WHERE actual_outcome IS NOT NULL
GROUP BY model_name
ORDER BY accuracy_percentage DESC;

-- ============================================================================
-- 9. FUNCTIONS (Useful Procedures)
-- ============================================================================

-- Function: Update employee's updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-update updated_at for employees
CREATE TRIGGER trigger_employees_updated_at
    BEFORE UPDATE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function: Calculate prediction correctness
CREATE OR REPLACE FUNCTION update_prediction_correctness()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.actual_outcome IS NOT NULL THEN
        NEW.is_correct = (NEW.prediction = NEW.actual_outcome);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-calculate is_correct when actual_outcome is set
CREATE TRIGGER trigger_prediction_correctness
    BEFORE UPDATE ON predictions
    FOR EACH ROW
    WHEN (NEW.actual_outcome IS DISTINCT FROM OLD.actual_outcome)
    EXECUTE FUNCTION update_prediction_correctness();

-- ============================================================================
-- 10. SAMPLE DATA (For Testing)
-- ============================================================================

-- Insert sample user
INSERT INTO users (username, email, password_hash, full_name, role)
VALUES 
    ('admin', 'admin@company.com', 'hashed_password_here', 'System Admin', 'admin'),
    ('hr_user1', 'hr1@company.com', 'hashed_password_here', 'HR Manager', 'hr_user')
ON CONFLICT (username) DO NOTHING;

-- ============================================================================
-- NOTES FOR IMPLEMENTATION
-- ============================================================================

/*
1. Connection String Format:
   postgresql://username:password@host:port/database

2. Environment Variables (.env):
   DATABASE_URL=postgresql://user:pass@localhost:5432/mpcim_thesis
   DATABASE_POOL_SIZE=10
   DATABASE_MAX_OVERFLOW=20

3. Free Hosting Options:
   - Supabase: https://supabase.com (PostgreSQL + Auth + Storage)
   - Neon: https://neon.tech (Serverless PostgreSQL)
   - Railway: https://railway.app (PostgreSQL + Deployment)
   - ElephantSQL: https://www.elephantsql.com (Free tier: 20MB)

4. Migration Tools:
   - Alembic (Python)
   - Flyway
   - Liquibase

5. ORM Options:
   - SQLAlchemy (Recommended)
   - Tortoise ORM
   - Peewee
*/
