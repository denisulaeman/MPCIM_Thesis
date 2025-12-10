"""
MPCIM Thesis - Database Models (SQLAlchemy ORM)
Author: Deni Sulaeman
Date: November 22, 2025

SQLAlchemy models for PostgreSQL database integration.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, Text, 
    Numeric, ForeignKey, JSON, Index, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Employee(Base):
    """Employee master data"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    department = Column(String(100), index=True)
    position = Column(String(100))
    
    # Performance Metrics
    performance_score = Column(Numeric(5, 2))
    performance_rating = Column(String(50))
    
    # Behavioral Metrics
    behavioral_score = Column(Numeric(5, 2))
    collaboration_score = Column(Numeric(5, 2))
    leadership_score = Column(Numeric(5, 2))
    
    # Demographic
    gender = Column(String(20))
    marital_status = Column(String(50))
    age = Column(Integer)
    tenure_years = Column(Numeric(5, 2))
    is_permanent = Column(Boolean, default=True)
    
    # Quick Assessment
    has_quick_assessment = Column(Boolean, default=False)
    psychological_score = Column(Numeric(5, 2))
    drive_score = Column(Numeric(5, 2))
    mental_strength_score = Column(Numeric(5, 2))
    adaptability_score = Column(Numeric(5, 2))
    
    # Promotion Status
    has_promotion = Column(Boolean, default=False, index=True)
    promotion_date = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    predictions = relationship("Prediction", back_populates="employee", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="employee", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Employee(id={self.employee_id}, name={self.name})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'position': self.position,
            'performance_score': float(self.performance_score) if self.performance_score else None,
            'behavioral_score': float(self.behavioral_score) if self.behavioral_score else None,
            'has_promotion': self.has_promotion,
            'has_quick_assessment': self.has_quick_assessment,
            'is_active': self.is_active
        }


class Prediction(Base):
    """Prediction logs"""
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(50), ForeignKey('employees.employee_id', ondelete='CASCADE'), 
                        nullable=False, index=True)
    
    # Prediction Details
    model_name = Column(String(100), nullable=False, index=True)
    model_version = Column(String(50))
    prediction = Column(Integer, nullable=False, index=True)  # 0 or 1
    probability = Column(Numeric(5, 4), nullable=False)
    confidence_level = Column(String(20))  # High, Medium, Low
    
    # Input Features (JSON)
    input_features = Column(JSON)
    
    # SHAP Explanation
    shap_values = Column(JSON)
    top_contributing_features = Column(JSON)
    
    # Threshold Info
    threshold_used = Column(Numeric(5, 4), default=0.70)
    distance_from_threshold = Column(Numeric(5, 4))
    
    # Metadata
    predicted_by = Column(String(255))
    predicted_at = Column(DateTime, default=func.now(), index=True)
    
    # Actual Outcome (for monitoring)
    actual_outcome = Column(Integer)  # NULL until known
    outcome_date = Column(DateTime)
    is_correct = Column(Boolean)
    
    # Relationships
    employee = relationship("Employee", back_populates="predictions")
    feedback = relationship("Feedback", back_populates="prediction", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, employee={self.employee_id}, prediction={self.prediction})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'model_name': self.model_name,
            'prediction': self.prediction,
            'probability': float(self.probability),
            'confidence_level': self.confidence_level,
            'threshold_used': float(self.threshold_used) if self.threshold_used else 0.70,
            'predicted_at': self.predicted_at.isoformat() if self.predicted_at else None,
            'predicted_by': self.predicted_by,
            'actual_outcome': self.actual_outcome,
            'is_correct': self.is_correct
        }


class User(Base):
    """HR Users"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # User Info
    full_name = Column(String(255))
    role = Column(String(50), default='hr_user', index=True)  # admin, hr_user, viewer
    department = Column(String(100))
    
    # Permissions
    can_predict = Column(Boolean, default=True)
    can_view_all = Column(Boolean, default=False)
    can_export = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"
    
    def to_dict(self):
        """Convert to dictionary (exclude password)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'department': self.department,
            'is_active': self.is_active
        }


class AuditLog(Base):
    """Activity tracking"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), index=True)
    username = Column(String(100))
    
    # Action Details
    action = Column(String(100), nullable=False, index=True)  # predict, view, export, update
    entity_type = Column(String(50))  # employee, prediction, model
    entity_id = Column(String(100))
    
    # Details
    description = Column(Text)
    metadata = Column(JSON)
    
    # Request Info
    ip_address = Column(String(50))
    user_agent = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime, default=func.now(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, user={self.username})>"


class ModelPerformance(Base):
    """Model monitoring"""
    __tablename__ = 'model_performance'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(100), nullable=False, index=True)
    model_version = Column(String(50))
    
    # Performance Metrics
    accuracy = Column(Numeric(5, 4))
    precision_score = Column(Numeric(5, 4))
    recall = Column(Numeric(5, 4))
    f1_score = Column(Numeric(5, 4))
    roc_auc = Column(Numeric(5, 4))
    
    # Confusion Matrix
    true_positives = Column(Integer)
    true_negatives = Column(Integer)
    false_positives = Column(Integer)
    false_negatives = Column(Integer)
    
    # Threshold Info
    threshold = Column(Numeric(5, 4), default=0.70)
    
    # Dataset Info
    test_size = Column(Integer)
    train_size = Column(Integer)
    
    # Metadata
    evaluation_date = Column(DateTime, default=func.now(), index=True)
    notes = Column(Text)
    
    def __repr__(self):
        return f"<ModelPerformance(model={self.model_name}, accuracy={self.accuracy})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'model_name': self.model_name,
            'model_version': self.model_version,
            'accuracy': float(self.accuracy) if self.accuracy else None,
            'precision': float(self.precision_score) if self.precision_score else None,
            'recall': float(self.recall) if self.recall else None,
            'f1_score': float(self.f1_score) if self.f1_score else None,
            'roc_auc': float(self.roc_auc) if self.roc_auc else None,
            'evaluation_date': self.evaluation_date.isoformat() if self.evaluation_date else None
        }


class AIAnalysisCache(Base):
    """Cache for AI analysis results"""
    __tablename__ = 'ai_analysis_cache'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cache_key = Column(String(255), unique=True, nullable=False, index=True)
    
    # Analysis Details
    analysis_type = Column(String(100), index=True)  # model_performance, data_explorer, eda
    input_hash = Column(String(64))  # MD5 hash of input
    
    # AI Response
    ai_provider = Column(String(50))  # gemini, openai
    ai_model = Column(String(100))
    analysis_result = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, index=True)
    hit_count = Column(Integer, default=0)
    
    # Cost tracking
    tokens_used = Column(Integer)
    cost_usd = Column(Numeric(10, 6))
    
    def __repr__(self):
        return f"<AIAnalysisCache(key={self.cache_key}, type={self.analysis_type})>"


class Feedback(Base):
    """User feedback on predictions"""
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    prediction_id = Column(Integer, ForeignKey('predictions.id', ondelete='CASCADE'), 
                          nullable=False, index=True)
    employee_id = Column(String(50), ForeignKey('employees.employee_id', ondelete='CASCADE'), 
                        nullable=False, index=True)
    
    # Feedback Details
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    is_accurate = Column(Boolean)
    comments = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    prediction = relationship("Prediction", back_populates="feedback")
    employee = relationship("Employee", back_populates="feedback")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, prediction={self.prediction_id}, rating={self.rating})>"


# ============================================================================
# Indexes (additional composite indexes)
# ============================================================================

# Composite index for predictions filtering
Index('idx_predictions_employee_model', Prediction.employee_id, Prediction.model_name)
Index('idx_predictions_date_model', Prediction.predicted_at, Prediction.model_name)

# Composite index for audit logs
Index('idx_audit_user_action', AuditLog.user_id, AuditLog.action)
Index('idx_audit_date_action', AuditLog.created_at, AuditLog.action)
