"""
MPCIM Thesis - Database Connection Manager
Author: Deni Sulaeman
Date: November 22, 2025

Handles database connections, sessions, and initialization.
"""

import os
from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from .models import Base
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Singleton database manager"""
    
    _instance: Optional['DatabaseManager'] = None
    _engine = None
    _session_factory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database manager"""
        if self._engine is None:
            self._initialize()
    
    def _initialize(self):
        """Initialize database connection"""
        # Get database URL from environment
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            logger.warning("DATABASE_URL not found. Using SQLite fallback.")
            database_url = 'sqlite:///./mpcim_thesis.db'
        
        # Connection pool settings
        pool_size = int(os.getenv('DATABASE_POOL_SIZE', '10'))
        max_overflow = int(os.getenv('DATABASE_MAX_OVERFLOW', '20'))
        pool_timeout = int(os.getenv('DATABASE_POOL_TIMEOUT', '30'))
        pool_recycle = int(os.getenv('DATABASE_POOL_RECYCLE', '3600'))
        
        # Create engine
        if database_url.startswith('sqlite'):
            # SQLite specific settings
            self._engine = create_engine(
                database_url,
                connect_args={'check_same_thread': False},
                echo=os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
            )
        else:
            # PostgreSQL settings
            self._engine = create_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_recycle=pool_recycle,
                pool_pre_ping=True,  # Verify connections before using
                echo=os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
            )
        
        # Create session factory
        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False
        )
        
        logger.info(f"Database engine initialized: {database_url.split('@')[0]}...")
    
    @property
    def engine(self):
        """Get database engine"""
        return self._engine
    
    @property
    def session_factory(self):
        """Get session factory"""
        return self._session_factory
    
    def create_tables(self):
        """Create all tables"""
        try:
            Base.metadata.create_all(bind=self._engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        try:
            Base.metadata.drop_all(bind=self._engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Error dropping tables: {e}")
            raise
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session with automatic cleanup.
        
        Usage:
            with db_manager.get_session() as session:
                # Use session here
                session.query(Employee).all()
        """
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise
        finally:
            session.close()
    
    def get_session_direct(self) -> Session:
        """
        Get session directly (manual management required).
        
        Usage:
            session = db_manager.get_session_direct()
            try:
                # Use session
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()
        """
        return self._session_factory()
    
    def health_check(self) -> bool:
        """Check database connection health"""
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def get_connection_info(self) -> dict:
        """Get connection information"""
        return {
            'url': str(self._engine.url).split('@')[0] + '@...',  # Hide credentials
            'pool_size': self._engine.pool.size() if hasattr(self._engine.pool, 'size') else 'N/A',
            'checked_in': self._engine.pool.checkedin() if hasattr(self._engine.pool, 'checkedin') else 'N/A',
            'checked_out': self._engine.pool.checkedout() if hasattr(self._engine.pool, 'checkedout') else 'N/A',
            'overflow': self._engine.pool.overflow() if hasattr(self._engine.pool, 'overflow') else 'N/A',
        }


# ============================================================================
# Global instance
# ============================================================================

db_manager = DatabaseManager()


# ============================================================================
# Dependency injection for FastAPI/Streamlit
# ============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI or Streamlit.
    
    Usage in FastAPI:
        @app.get("/employees")
        def get_employees(db: Session = Depends(get_db)):
            return db.query(Employee).all()
    
    Usage in Streamlit:
        from database.connection import get_db
        
        with next(get_db()) as session:
            employees = session.query(Employee).all()
    """
    with db_manager.get_session() as session:
        yield session


# ============================================================================
# Utility functions
# ============================================================================

def init_database():
    """Initialize database (create tables)"""
    logger.info("Initializing database...")
    db_manager.create_tables()
    logger.info("Database initialized successfully")


def reset_database():
    """Reset database (drop and recreate tables)"""
    logger.warning("Resetting database...")
    db_manager.drop_tables()
    db_manager.create_tables()
    logger.info("Database reset successfully")


def check_database_health() -> dict:
    """Check database health and return status"""
    is_healthy = db_manager.health_check()
    connection_info = db_manager.get_connection_info()
    
    return {
        'healthy': is_healthy,
        'connection_info': connection_info
    }


# ============================================================================
# Example usage
# ============================================================================

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize database
    init_database()
    
    # Health check
    health = check_database_health()
    print(f"Database health: {health}")
    
    # Example: Create and query
    from .models import Employee
    
    with db_manager.get_session() as session:
        # Create employee
        employee = Employee(
            employee_id='EMP001',
            name='John Doe',
            email='john@company.com',
            department='IT',
            performance_score=85.5,
            behavioral_score=90.0
        )
        session.add(employee)
        session.commit()
        
        print(f"Created employee: {employee}")
        
        # Query employees
        employees = session.query(Employee).all()
        print(f"Total employees: {len(employees)}")
