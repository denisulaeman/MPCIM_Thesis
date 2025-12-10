"""
MPCIM Thesis - Dual Database Connection Manager
Author: Deni Sulaeman
Date: November 22, 2025

Manages connections to:
1. Source DB (DigiSpace CNA) - Read-only for employee data
2. Thesis DB (MPCIM) - Read-write for predictions and analysis
"""

import os
from contextlib import contextmanager
from typing import Generator, Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import logging

logger = logging.getLogger(__name__)


class DualDatabaseManager:
    """Manages connections to both source and thesis databases"""
    
    _instance: Optional['DualDatabaseManager'] = None
    _source_engine = None
    _thesis_engine = None
    _source_session_factory = None
    _thesis_session_factory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize dual database connections"""
        if self._source_engine is None:
            self._initialize()
    
    def _initialize(self):
        """Initialize both database connections"""
        self._initialize_source_db()
        self._initialize_thesis_db()
    
    def _initialize_source_db(self):
        """Initialize connection to source database (DigiSpace CNA)"""
        # Get source database credentials
        db_host = os.getenv('SOURCE_DB_HOST', 'localhost')
        db_port = os.getenv('SOURCE_DB_PORT', '5433')
        db_name = os.getenv('SOURCE_DB_DATABASE', 'db_digispace_cna_augustus_182025')
        db_user = os.getenv('SOURCE_DB_USERNAME', 'postgres')
        db_pass = os.getenv('SOURCE_DB_PASSWORD', '')
        
        # Build connection URL
        source_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        
        try:
            # Create engine with read-only settings
            self._source_engine = create_engine(
                source_url,
                poolclass=QueuePool,
                pool_size=5,  # Smaller pool for read-only
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=3600,
                pool_pre_ping=True,
                echo=os.getenv('DATABASE_ECHO', 'false').lower() == 'true',
                # Read-only connection
                connect_args={
                    'options': '-c default_transaction_read_only=on'
                }
            )
            
            # Create session factory
            self._source_session_factory = sessionmaker(
                bind=self._source_engine,
                autocommit=False,
                autoflush=False
            )
            
            logger.info(f"Source database connected: {db_host}:{db_port}/{db_name}")
        except Exception as e:
            logger.error(f"Failed to connect to source database: {e}")
            self._source_engine = None
    
    def _initialize_thesis_db(self):
        """Initialize connection to thesis database (MPCIM)"""
        # Get thesis database URL
        thesis_url = os.getenv('THESIS_DATABASE_URL') or os.getenv('DATABASE_URL')
        
        if not thesis_url:
            logger.warning("THESIS_DATABASE_URL not found. Using SQLite fallback.")
            thesis_url = 'sqlite:///./mpcim_thesis.db'
        
        # Connection pool settings
        pool_size = int(os.getenv('DATABASE_POOL_SIZE', '10'))
        max_overflow = int(os.getenv('DATABASE_MAX_OVERFLOW', '20'))
        
        try:
            if thesis_url.startswith('sqlite'):
                self._thesis_engine = create_engine(
                    thesis_url,
                    connect_args={'check_same_thread': False},
                    echo=os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
                )
            else:
                self._thesis_engine = create_engine(
                    thesis_url,
                    poolclass=QueuePool,
                    pool_size=pool_size,
                    max_overflow=max_overflow,
                    pool_timeout=30,
                    pool_recycle=3600,
                    pool_pre_ping=True,
                    echo=os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
                )
            
            # Create session factory
            self._thesis_session_factory = sessionmaker(
                bind=self._thesis_engine,
                autocommit=False,
                autoflush=False
            )
            
            logger.info(f"Thesis database connected: {thesis_url.split('@')[0]}...")
        except Exception as e:
            logger.error(f"Failed to connect to thesis database: {e}")
            raise
    
    @property
    def source_engine(self):
        """Get source database engine"""
        return self._source_engine
    
    @property
    def thesis_engine(self):
        """Get thesis database engine"""
        return self._thesis_engine
    
    @contextmanager
    def get_source_session(self) -> Generator[Session, None, None]:
        """
        Get source database session (read-only).
        
        Usage:
            with dual_db.get_source_session() as session:
                employees = session.execute(text("SELECT * FROM employees")).fetchall()
        """
        if not self._source_engine:
            raise RuntimeError("Source database not connected")
        
        session = self._source_session_factory()
        try:
            yield session
            # No commit for read-only
        except Exception as e:
            logger.error(f"Source session error: {e}")
            raise
        finally:
            session.close()
    
    @contextmanager
    def get_thesis_session(self) -> Generator[Session, None, None]:
        """
        Get thesis database session (read-write).
        
        Usage:
            with dual_db.get_thesis_session() as session:
                prediction = Prediction(...)
                session.add(prediction)
                session.commit()
        """
        session = self._thesis_session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Thesis session error: {e}")
            raise
        finally:
            session.close()
    
    def test_source_connection(self) -> Dict[str, Any]:
        """Test source database connection"""
        try:
            with self.get_source_session() as session:
                result = session.execute(text("SELECT version()")).scalar()
                
                # Try to get table list
                tables_query = text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
                tables = [row[0] for row in session.execute(tables_query).fetchall()]
                
                return {
                    'connected': True,
                    'version': result,
                    'tables': tables,
                    'table_count': len(tables)
                }
        except Exception as e:
            return {
                'connected': False,
                'error': str(e)
            }
    
    def test_thesis_connection(self) -> Dict[str, Any]:
        """Test thesis database connection"""
        try:
            with self.get_thesis_session() as session:
                session.execute(text("SELECT 1"))
                return {
                    'connected': True,
                    'url': str(self._thesis_engine.url).split('@')[0] + '@...'
                }
        except Exception as e:
            return {
                'connected': False,
                'error': str(e)
            }
    
    def get_source_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get information about a table in source database"""
        try:
            with self.get_source_session() as session:
                # Get column information
                columns_query = text("""
                    SELECT 
                        column_name,
                        data_type,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_name = :table_name
                    AND table_schema = 'public'
                    ORDER BY ordinal_position
                """)
                
                columns = session.execute(
                    columns_query, 
                    {'table_name': table_name}
                ).fetchall()
                
                # Get row count
                count_query = text(f"SELECT COUNT(*) FROM {table_name}")
                row_count = session.execute(count_query).scalar()
                
                return {
                    'table_name': table_name,
                    'columns': [
                        {
                            'name': col[0],
                            'type': col[1],
                            'nullable': col[2],
                            'default': col[3]
                        }
                        for col in columns
                    ],
                    'row_count': row_count
                }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get status of both connections"""
        return {
            'source_db': self.test_source_connection(),
            'thesis_db': self.test_thesis_connection()
        }


# ============================================================================
# Global instance
# ============================================================================

dual_db = DualDatabaseManager()


# ============================================================================
# Convenience functions
# ============================================================================

def get_source_session() -> Generator[Session, None, None]:
    """Get source database session"""
    with dual_db.get_source_session() as session:
        yield session


def get_thesis_session() -> Generator[Session, None, None]:
    """Get thesis database session"""
    with dual_db.get_thesis_session() as session:
        yield session


def test_connections():
    """Test both database connections"""
    status = dual_db.get_connection_status()
    
    print("="*80)
    print("DATABASE CONNECTION STATUS")
    print("="*80)
    print()
    
    print("SOURCE DATABASE (DigiSpace CNA):")
    print("-"*80)
    if status['source_db']['connected']:
        print(f"✅ Connected")
        print(f"   Version: {status['source_db']['version']}")
        print(f"   Tables: {status['source_db']['table_count']}")
        print(f"   Available tables: {', '.join(status['source_db']['tables'][:5])}...")
    else:
        print(f"❌ Not connected")
        print(f"   Error: {status['source_db'].get('error')}")
    print()
    
    print("THESIS DATABASE (MPCIM):")
    print("-"*80)
    if status['thesis_db']['connected']:
        print(f"✅ Connected")
        print(f"   URL: {status['thesis_db']['url']}")
    else:
        print(f"❌ Not connected")
        print(f"   Error: {status['thesis_db'].get('error')}")
    print()


# ============================================================================
# Example usage
# ============================================================================

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Test connections
    test_connections()
    
    # Example: Query source database
    print("\nExample: Query source database")
    print("-"*80)
    try:
        with dual_db.get_source_session() as session:
            # Get table list
            result = session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                LIMIT 5
            """))
            
            print("First 5 tables:")
            for row in result:
                print(f"  - {row[0]}")
    except Exception as e:
        print(f"Error: {e}")
