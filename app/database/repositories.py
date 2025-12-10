"""
MPCIM Thesis - Database Repositories (CRUD Operations)
Author: Deni Sulaeman
Date: November 22, 2025

Repository pattern for database operations.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from .models import (
    Employee, Prediction, User, AuditLog, 
    ModelPerformance, AIAnalysisCache, Feedback
)
import hashlib
import json


class EmployeeRepository:
    """Repository for Employee operations"""
    
    @staticmethod
    def create(session: Session, **kwargs) -> Employee:
        """Create new employee"""
        employee = Employee(**kwargs)
        session.add(employee)
        session.flush()
        return employee
    
    @staticmethod
    def get_by_id(session: Session, employee_id: str) -> Optional[Employee]:
        """Get employee by ID"""
        return session.query(Employee).filter(
            Employee.employee_id == employee_id
        ).first()
    
    @staticmethod
    def get_all(session: Session, active_only: bool = True) -> List[Employee]:
        """Get all employees"""
        query = session.query(Employee)
        if active_only:
            query = query.filter(Employee.is_active == True)
        return query.all()
    
    @staticmethod
    def get_by_department(session: Session, department: str) -> List[Employee]:
        """Get employees by department"""
        return session.query(Employee).filter(
            Employee.department == department,
            Employee.is_active == True
        ).all()
    
    @staticmethod
    def get_promoted(session: Session) -> List[Employee]:
        """Get promoted employees"""
        return session.query(Employee).filter(
            Employee.has_promotion == True
        ).all()
    
    @staticmethod
    def search(session: Session, query: str) -> List[Employee]:
        """Search employees by name or ID"""
        search_term = f"%{query}%"
        return session.query(Employee).filter(
            or_(
                Employee.name.ilike(search_term),
                Employee.employee_id.ilike(search_term),
                Employee.email.ilike(search_term)
            )
        ).all()
    
    @staticmethod
    def update(session: Session, employee_id: str, **kwargs) -> Optional[Employee]:
        """Update employee"""
        employee = EmployeeRepository.get_by_id(session, employee_id)
        if employee:
            for key, value in kwargs.items():
                if hasattr(employee, key):
                    setattr(employee, key, value)
            session.flush()
        return employee
    
    @staticmethod
    def delete(session: Session, employee_id: str) -> bool:
        """Soft delete employee"""
        employee = EmployeeRepository.get_by_id(session, employee_id)
        if employee:
            employee.is_active = False
            session.flush()
            return True
        return False
    
    @staticmethod
    def get_statistics(session: Session) -> Dict[str, Any]:
        """Get employee statistics"""
        total = session.query(func.count(Employee.id)).filter(
            Employee.is_active == True
        ).scalar()
        
        promoted = session.query(func.count(Employee.id)).filter(
            Employee.has_promotion == True,
            Employee.is_active == True
        ).scalar()
        
        with_qa = session.query(func.count(Employee.id)).filter(
            Employee.has_quick_assessment == True,
            Employee.is_active == True
        ).scalar()
        
        avg_performance = session.query(func.avg(Employee.performance_score)).filter(
            Employee.is_active == True
        ).scalar()
        
        avg_behavioral = session.query(func.avg(Employee.behavioral_score)).filter(
            Employee.is_active == True
        ).scalar()
        
        return {
            'total_employees': total or 0,
            'promoted_count': promoted or 0,
            'promotion_rate': (promoted / total * 100) if total > 0 else 0,
            'with_quick_assessment': with_qa or 0,
            'avg_performance_score': float(avg_performance) if avg_performance else 0,
            'avg_behavioral_score': float(avg_behavioral) if avg_behavioral else 0
        }


class PredictionRepository:
    """Repository for Prediction operations"""
    
    @staticmethod
    def create(session: Session, **kwargs) -> Prediction:
        """Create new prediction"""
        prediction = Prediction(**kwargs)
        session.add(prediction)
        session.flush()
        return prediction
    
    @staticmethod
    def get_by_id(session: Session, prediction_id: int) -> Optional[Prediction]:
        """Get prediction by ID"""
        return session.query(Prediction).filter(
            Prediction.id == prediction_id
        ).first()
    
    @staticmethod
    def get_by_employee(session: Session, employee_id: str) -> List[Prediction]:
        """Get all predictions for an employee"""
        return session.query(Prediction).filter(
            Prediction.employee_id == employee_id
        ).order_by(Prediction.predicted_at.desc()).all()
    
    @staticmethod
    def get_recent(session: Session, limit: int = 100) -> List[Prediction]:
        """Get recent predictions"""
        return session.query(Prediction).order_by(
            Prediction.predicted_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_by_model(session: Session, model_name: str) -> List[Prediction]:
        """Get predictions by model"""
        return session.query(Prediction).filter(
            Prediction.model_name == model_name
        ).all()
    
    @staticmethod
    def get_by_date_range(
        session: Session, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Prediction]:
        """Get predictions within date range"""
        return session.query(Prediction).filter(
            and_(
                Prediction.predicted_at >= start_date,
                Prediction.predicted_at <= end_date
            )
        ).all()
    
    @staticmethod
    def update_actual_outcome(
        session: Session, 
        prediction_id: int, 
        actual_outcome: int
    ) -> Optional[Prediction]:
        """Update actual outcome for prediction"""
        prediction = PredictionRepository.get_by_id(session, prediction_id)
        if prediction:
            prediction.actual_outcome = actual_outcome
            prediction.outcome_date = datetime.now()
            prediction.is_correct = (prediction.prediction == actual_outcome)
            session.flush()
        return prediction
    
    @staticmethod
    def get_accuracy_stats(session: Session, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Get prediction accuracy statistics"""
        query = session.query(Prediction).filter(
            Prediction.actual_outcome.isnot(None)
        )
        
        if model_name:
            query = query.filter(Prediction.model_name == model_name)
        
        predictions = query.all()
        
        if not predictions:
            return {'total': 0, 'correct': 0, 'accuracy': 0}
        
        total = len(predictions)
        correct = sum(1 for p in predictions if p.is_correct)
        
        return {
            'total': total,
            'correct': correct,
            'incorrect': total - correct,
            'accuracy': (correct / total * 100) if total > 0 else 0
        }


class UserRepository:
    """Repository for User operations"""
    
    @staticmethod
    def create(session: Session, **kwargs) -> User:
        """Create new user"""
        user = User(**kwargs)
        session.add(user)
        session.flush()
        return user
    
    @staticmethod
    def get_by_username(session: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return session.query(User).filter(
            User.username == username
        ).first()
    
    @staticmethod
    def get_by_email(session: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return session.query(User).filter(
            User.email == email
        ).first()
    
    @staticmethod
    def authenticate(session: Session, username: str, password_hash: str) -> Optional[User]:
        """Authenticate user"""
        user = UserRepository.get_by_username(session, username)
        if user and user.password_hash == password_hash and user.is_active:
            user.last_login = datetime.now()
            session.flush()
            return user
        return None
    
    @staticmethod
    def get_all(session: Session, active_only: bool = True) -> List[User]:
        """Get all users"""
        query = session.query(User)
        if active_only:
            query = query.filter(User.is_active == True)
        return query.all()


class AuditLogRepository:
    """Repository for Audit Log operations"""
    
    @staticmethod
    def log(
        session: Session,
        user_id: Optional[int],
        username: str,
        action: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Create audit log entry"""
        log = AuditLog(
            user_id=user_id,
            username=username,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent
        )
        session.add(log)
        session.flush()
        return log
    
    @staticmethod
    def get_by_user(session: Session, user_id: int, limit: int = 100) -> List[AuditLog]:
        """Get audit logs for a user"""
        return session.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_by_action(session: Session, action: str, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by action type"""
        return session.query(AuditLog).filter(
            AuditLog.action == action
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_recent(session: Session, limit: int = 100) -> List[AuditLog]:
        """Get recent audit logs"""
        return session.query(AuditLog).order_by(
            AuditLog.created_at.desc()
        ).limit(limit).all()


class ModelPerformanceRepository:
    """Repository for Model Performance operations"""
    
    @staticmethod
    def create(session: Session, **kwargs) -> ModelPerformance:
        """Create model performance record"""
        perf = ModelPerformance(**kwargs)
        session.add(perf)
        session.flush()
        return perf
    
    @staticmethod
    def get_latest(session: Session, model_name: str) -> Optional[ModelPerformance]:
        """Get latest performance for a model"""
        return session.query(ModelPerformance).filter(
            ModelPerformance.model_name == model_name
        ).order_by(ModelPerformance.evaluation_date.desc()).first()
    
    @staticmethod
    def get_history(session: Session, model_name: str) -> List[ModelPerformance]:
        """Get performance history for a model"""
        return session.query(ModelPerformance).filter(
            ModelPerformance.model_name == model_name
        ).order_by(ModelPerformance.evaluation_date.desc()).all()
    
    @staticmethod
    def get_all_latest(session: Session) -> List[ModelPerformance]:
        """Get latest performance for all models"""
        # Subquery to get latest evaluation date for each model
        subquery = session.query(
            ModelPerformance.model_name,
            func.max(ModelPerformance.evaluation_date).label('max_date')
        ).group_by(ModelPerformance.model_name).subquery()
        
        # Join to get full records
        return session.query(ModelPerformance).join(
            subquery,
            and_(
                ModelPerformance.model_name == subquery.c.model_name,
                ModelPerformance.evaluation_date == subquery.c.max_date
            )
        ).all()


class AIAnalysisCacheRepository:
    """Repository for AI Analysis Cache operations"""
    
    @staticmethod
    def _generate_cache_key(analysis_type: str, input_data: Dict) -> str:
        """Generate cache key from input data"""
        # Create deterministic hash of input
        input_str = json.dumps(input_data, sort_keys=True)
        hash_obj = hashlib.md5(input_str.encode())
        return f"{analysis_type}:{hash_obj.hexdigest()}"
    
    @staticmethod
    def get_or_none(
        session: Session, 
        analysis_type: str, 
        input_data: Dict
    ) -> Optional[AIAnalysisCache]:
        """Get cached analysis if exists and not expired"""
        cache_key = AIAnalysisCacheRepository._generate_cache_key(analysis_type, input_data)
        
        cache = session.query(AIAnalysisCache).filter(
            AIAnalysisCache.cache_key == cache_key,
            or_(
                AIAnalysisCache.expires_at.is_(None),
                AIAnalysisCache.expires_at > datetime.now()
            )
        ).first()
        
        if cache:
            # Increment hit count
            cache.hit_count += 1
            session.flush()
        
        return cache
    
    @staticmethod
    def set(
        session: Session,
        analysis_type: str,
        input_data: Dict,
        analysis_result: str,
        ai_provider: str,
        ai_model: str,
        expires_in_hours: int = 24,
        tokens_used: Optional[int] = None,
        cost_usd: Optional[float] = None
    ) -> AIAnalysisCache:
        """Cache AI analysis result"""
        cache_key = AIAnalysisCacheRepository._generate_cache_key(analysis_type, input_data)
        input_hash = hashlib.md5(json.dumps(input_data, sort_keys=True).encode()).hexdigest()
        
        # Check if exists
        cache = session.query(AIAnalysisCache).filter(
            AIAnalysisCache.cache_key == cache_key
        ).first()
        
        if cache:
            # Update existing
            cache.analysis_result = analysis_result
            cache.ai_provider = ai_provider
            cache.ai_model = ai_model
            cache.expires_at = datetime.now() + timedelta(hours=expires_in_hours)
            cache.tokens_used = tokens_used
            cache.cost_usd = cost_usd
        else:
            # Create new
            cache = AIAnalysisCache(
                cache_key=cache_key,
                analysis_type=analysis_type,
                input_hash=input_hash,
                ai_provider=ai_provider,
                ai_model=ai_model,
                analysis_result=analysis_result,
                expires_at=datetime.now() + timedelta(hours=expires_in_hours),
                tokens_used=tokens_used,
                cost_usd=cost_usd
            )
            session.add(cache)
        
        session.flush()
        return cache
    
    @staticmethod
    def clear_expired(session: Session) -> int:
        """Clear expired cache entries"""
        count = session.query(AIAnalysisCache).filter(
            AIAnalysisCache.expires_at < datetime.now()
        ).delete()
        session.flush()
        return count
    
    @staticmethod
    def get_statistics(session: Session) -> Dict[str, Any]:
        """Get cache statistics"""
        total = session.query(func.count(AIAnalysisCache.id)).scalar()
        total_hits = session.query(func.sum(AIAnalysisCache.hit_count)).scalar()
        total_cost = session.query(func.sum(AIAnalysisCache.cost_usd)).scalar()
        
        return {
            'total_entries': total or 0,
            'total_hits': total_hits or 0,
            'total_cost_usd': float(total_cost) if total_cost else 0
        }


class FeedbackRepository:
    """Repository for Feedback operations"""
    
    @staticmethod
    def create(session: Session, **kwargs) -> Feedback:
        """Create feedback"""
        feedback = Feedback(**kwargs)
        session.add(feedback)
        session.flush()
        return feedback
    
    @staticmethod
    def get_by_prediction(session: Session, prediction_id: int) -> List[Feedback]:
        """Get feedback for a prediction"""
        return session.query(Feedback).filter(
            Feedback.prediction_id == prediction_id
        ).all()
    
    @staticmethod
    def get_statistics(session: Session) -> Dict[str, Any]:
        """Get feedback statistics"""
        total = session.query(func.count(Feedback.id)).scalar()
        avg_rating = session.query(func.avg(Feedback.rating)).scalar()
        accurate_count = session.query(func.count(Feedback.id)).filter(
            Feedback.is_accurate == True
        ).scalar()
        
        return {
            'total_feedback': total or 0,
            'average_rating': float(avg_rating) if avg_rating else 0,
            'accurate_predictions': accurate_count or 0,
            'accuracy_rate': (accurate_count / total * 100) if total > 0 else 0
        }
