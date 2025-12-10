"""
MPCIM Thesis - Data Synchronization Service
Author: Deni Sulaeman
Date: November 22, 2025

Synchronizes employee data from source database (DigiSpace CNA)
to thesis database (MPCIM).
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import text
from datetime import datetime
import logging
from .dual_connection import dual_db
from .repositories import EmployeeRepository

logger = logging.getLogger(__name__)


class DataSyncService:
    """Service for synchronizing data between databases"""
    
    def __init__(self):
        self.source_table_mapping = {
            # Map source table columns to thesis Employee model
            # Adjust these based on actual source database schema
            'employees': {
                'id': 'employee_id',
                'name': 'name',
                'email': 'email',
                'department': 'department',
                'position': 'position',
                'gender': 'gender',
                'marital_status': 'marital_status',
                'age': 'age',
                'tenure_years': 'tenure_years',
                'performance_score': 'performance_score',
                'performance_rating': 'performance_rating',
                'behavioral_score': 'behavioral_score',
                'has_promotion': 'has_promotion',
            }
        }
    
    def discover_source_schema(self) -> Dict[str, Any]:
        """
        Discover schema of source database.
        Helps identify which tables and columns are available.
        """
        try:
            with dual_db.get_source_session() as session:
                # Get all tables
                tables_query = text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                """)
                
                tables = [row[0] for row in session.execute(tables_query).fetchall()]
                
                schema_info = {}
                
                # For each table, get columns
                for table in tables:
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
                        {'table_name': table}
                    ).fetchall()
                    
                    # Get sample row count
                    try:
                        count_query = text(f'SELECT COUNT(*) FROM "{table}"')
                        row_count = session.execute(count_query).scalar()
                    except:
                        row_count = 0
                    
                    schema_info[table] = {
                        'columns': [
                            {
                                'name': col[0],
                                'type': col[1],
                                'nullable': col[2] == 'YES',
                                'default': col[3]
                            }
                            for col in columns
                        ],
                        'row_count': row_count
                    }
                
                return {
                    'success': True,
                    'tables': schema_info,
                    'table_count': len(tables)
                }
                
        except Exception as e:
            logger.error(f"Error discovering schema: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_source_data(
        self, 
        table_name: str, 
        columns: Optional[List[str]] = None,
        where_clause: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get data from source database table.
        
        Args:
            table_name: Name of source table
            columns: List of columns to select (None = all)
            where_clause: SQL WHERE clause (without WHERE keyword)
            limit: Maximum number of rows
        
        Returns:
            List of dictionaries with row data
        """
        try:
            with dual_db.get_source_session() as session:
                # Build query
                col_list = ', '.join(columns) if columns else '*'
                query = f'SELECT {col_list} FROM "{table_name}"'
                
                if where_clause:
                    query += f' WHERE {where_clause}'
                
                if limit:
                    query += f' LIMIT {limit}'
                
                # Execute query
                result = session.execute(text(query))
                
                # Convert to list of dicts
                rows = []
                for row in result:
                    rows.append(dict(row._mapping))
                
                return rows
                
        except Exception as e:
            logger.error(f"Error getting source data: {e}")
            return []
    
    def sync_employees(
        self,
        source_table: str = 'employees',
        column_mapping: Optional[Dict[str, str]] = None,
        where_clause: Optional[str] = None,
        limit: Optional[int] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Sync employee data from source to thesis database.
        
        Args:
            source_table: Name of source table
            column_mapping: Dict mapping source columns to thesis columns
            where_clause: Filter for source data
            limit: Maximum number of rows to sync
            dry_run: If True, don't actually insert data
        
        Returns:
            Dictionary with sync statistics
        """
        logger.info(f"Starting employee sync from {source_table}")
        
        # Use default mapping if not provided
        if column_mapping is None:
            column_mapping = self.source_table_mapping.get(source_table, {})
        
        if not column_mapping:
            return {
                'success': False,
                'error': f'No column mapping found for table {source_table}'
            }
        
        stats = {
            'total_source': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0,
            'error_details': []
        }
        
        try:
            # Get source data
            source_columns = list(column_mapping.keys())
            source_data = self.get_source_data(
                source_table,
                columns=source_columns,
                where_clause=where_clause,
                limit=limit
            )
            
            stats['total_source'] = len(source_data)
            logger.info(f"Retrieved {len(source_data)} rows from source")
            
            if dry_run:
                logger.info("DRY RUN - No data will be inserted")
                return {
                    'success': True,
                    'dry_run': True,
                    'stats': stats,
                    'sample_data': source_data[:5] if source_data else []
                }
            
            # Sync to thesis database
            with dual_db.get_thesis_session() as session:
                for row in source_data:
                    try:
                        # Map columns
                        employee_data = {}
                        for source_col, thesis_col in column_mapping.items():
                            if source_col in row:
                                value = row[source_col]
                                
                                # Type conversions
                                if thesis_col == 'employee_id':
                                    value = str(value)
                                elif thesis_col in ['performance_score', 'behavioral_score', 
                                                   'tenure_years']:
                                    value = float(value) if value is not None else None
                                elif thesis_col == 'has_promotion':
                                    value = bool(value) if value is not None else False
                                
                                employee_data[thesis_col] = value
                        
                        # Check if employee_id exists
                        if not employee_data.get('employee_id'):
                            stats['skipped'] += 1
                            continue
                        
                        # Check if employee already exists
                        existing = EmployeeRepository.get_by_id(
                            session,
                            employee_data['employee_id']
                        )
                        
                        if existing:
                            # Update existing
                            EmployeeRepository.update(
                                session,
                                employee_data['employee_id'],
                                **employee_data
                            )
                            stats['updated'] += 1
                        else:
                            # Create new
                            EmployeeRepository.create(session, **employee_data)
                            stats['created'] += 1
                        
                    except Exception as e:
                        stats['errors'] += 1
                        stats['error_details'].append({
                            'row': row,
                            'error': str(e)
                        })
                        logger.error(f"Error syncing row: {e}")
                        continue
            
            logger.info(f"Sync complete: {stats['created']} created, "
                       f"{stats['updated']} updated, {stats['errors']} errors")
            
            return {
                'success': True,
                'stats': stats
            }
            
        except Exception as e:
            logger.error(f"Error during sync: {e}")
            return {
                'success': False,
                'error': str(e),
                'stats': stats
            }
    
    def sync_with_custom_query(
        self,
        query: str,
        column_mapping: Dict[str, str],
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Sync data using custom SQL query.
        
        Args:
            query: Custom SQL query to get source data
            column_mapping: Dict mapping query columns to thesis columns
            dry_run: If True, don't actually insert data
        
        Returns:
            Dictionary with sync statistics
        """
        logger.info("Starting custom query sync")
        
        stats = {
            'total_source': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0
        }
        
        try:
            # Execute custom query on source
            with dual_db.get_source_session() as source_session:
                result = source_session.execute(text(query))
                source_data = [dict(row._mapping) for row in result]
            
            stats['total_source'] = len(source_data)
            logger.info(f"Retrieved {len(source_data)} rows from custom query")
            
            if dry_run:
                return {
                    'success': True,
                    'dry_run': True,
                    'stats': stats,
                    'sample_data': source_data[:5] if source_data else []
                }
            
            # Sync to thesis database
            with dual_db.get_thesis_session() as thesis_session:
                for row in source_data:
                    try:
                        # Map columns
                        employee_data = {}
                        for source_col, thesis_col in column_mapping.items():
                            if source_col in row:
                                employee_data[thesis_col] = row[source_col]
                        
                        if not employee_data.get('employee_id'):
                            stats['skipped'] += 1
                            continue
                        
                        # Check if exists
                        existing = EmployeeRepository.get_by_id(
                            thesis_session,
                            str(employee_data['employee_id'])
                        )
                        
                        if existing:
                            EmployeeRepository.update(
                                thesis_session,
                                str(employee_data['employee_id']),
                                **employee_data
                            )
                            stats['updated'] += 1
                        else:
                            EmployeeRepository.create(thesis_session, **employee_data)
                            stats['created'] += 1
                        
                    except Exception as e:
                        stats['errors'] += 1
                        logger.error(f"Error syncing row: {e}")
                        continue
            
            return {
                'success': True,
                'stats': stats
            }
            
        except Exception as e:
            logger.error(f"Error during custom sync: {e}")
            return {
                'success': False,
                'error': str(e),
                'stats': stats
            }


# ============================================================================
# Global instance
# ============================================================================

data_sync = DataSyncService()


# ============================================================================
# Convenience functions
# ============================================================================

def discover_schema() -> Dict[str, Any]:
    """Discover source database schema"""
    return data_sync.discover_source_schema()


def sync_employees(**kwargs) -> Dict[str, Any]:
    """Sync employee data"""
    return data_sync.sync_employees(**kwargs)


# ============================================================================
# Example usage
# ============================================================================

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("="*80)
    print("DATA SYNC SERVICE - EXAMPLE")
    print("="*80)
    print()
    
    # 1. Discover schema
    print("1. Discovering source database schema...")
    print("-"*80)
    schema = discover_schema()
    
    if schema['success']:
        print(f"✅ Found {schema['table_count']} tables")
        print("\nTables:")
        for table_name, info in list(schema['tables'].items())[:5]:
            print(f"  - {table_name} ({info['row_count']} rows)")
            print(f"    Columns: {', '.join([c['name'] for c in info['columns'][:5]])}...")
    else:
        print(f"❌ Error: {schema.get('error')}")
    
    print()
    
    # 2. Dry run sync
    print("2. Testing sync (dry run)...")
    print("-"*80)
    result = sync_employees(
        source_table='employees',
        limit=10,
        dry_run=True
    )
    
    if result['success']:
        print(f"✅ Dry run successful")
        print(f"   Would sync {result['stats']['total_source']} rows")
        if result.get('sample_data'):
            print(f"\n   Sample data:")
            for row in result['sample_data'][:2]:
                print(f"   {row}")
    else:
        print(f"❌ Error: {result.get('error')}")
