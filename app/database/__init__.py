"""
MPCIM Thesis - Database Package
Author: Deni Sulaeman
Date: November 22, 2025

Database integration for MPCIM Thesis application.
"""

from .connection import (
    db_manager,
    get_db,
    init_database,
    reset_database,
    check_database_health
)

from .models import (
    Base,
    Employee,
    Prediction,
    User,
    AuditLog,
    ModelPerformance,
    AIAnalysisCache,
    Feedback
)

from .repositories import (
    EmployeeRepository,
    PredictionRepository,
    UserRepository,
    AuditLogRepository,
    ModelPerformanceRepository,
    AIAnalysisCacheRepository,
    FeedbackRepository
)

__all__ = [
    # Connection
    'db_manager',
    'get_db',
    'init_database',
    'reset_database',
    'check_database_health',
    
    # Models
    'Base',
    'Employee',
    'Prediction',
    'User',
    'AuditLog',
    'ModelPerformance',
    'AIAnalysisCache',
    'Feedback',
    
    # Repositories
    'EmployeeRepository',
    'PredictionRepository',
    'UserRepository',
    'AuditLogRepository',
    'ModelPerformanceRepository',
    'AIAnalysisCacheRepository',
    'FeedbackRepository',
]
