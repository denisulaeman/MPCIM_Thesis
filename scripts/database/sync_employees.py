"""
MPCIM Thesis - Sync Employee Data
Author: Deni Sulaeman
Date: November 22, 2025

Synchronize employee data from source database to thesis database.
"""

import sys
from pathlib import Path
import logging
from datetime import datetime

# Add app directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'app'))

from database.data_sync import data_sync
from database import db_manager, EmployeeRepository

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print('='*80)
print('MPCIM THESIS - EMPLOYEE DATA SYNC')
print('='*80)
print()

# ============================================================================
# CONFIGURATION
# ============================================================================

# TODO: Update these based on your source database schema
SOURCE_TABLE = 'employees'  # Change to your actual table name

# TODO: Update column mapping
COLUMN_MAPPING = {
    # Source column -> Thesis column
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
    'collaboration_score': 'collaboration_score',
    'leadership_score': 'leadership_score',
    'has_promotion': 'has_promotion',
}

# Optional filters
WHERE_CLAUSE = None  # e.g., "status = 'active' AND deleted_at IS NULL"
LIMIT = None  # None = sync all data

print('SYNC CONFIGURATION:')
print('-'*80)
print(f'Source Table: {SOURCE_TABLE}')
print(f'Column Mapping: {len(COLUMN_MAPPING)} columns')
print(f'Where Clause: {WHERE_CLAUSE or "None (all data)"}')
print(f'Limit: {LIMIT or "None (all data)"}')
print()

# ============================================================================
# CONFIRMATION
# ============================================================================

print('⚠️  WARNING: This will sync data to thesis database!')
print()
response = input('Continue? (yes/no): ')

if response.lower() not in ['yes', 'y']:
    print('Sync cancelled.')
    sys.exit(0)

print()

# ============================================================================
# SYNC DATA
# ============================================================================

print('STARTING SYNC...')
print('-'*80)
print()

start_time = datetime.now()

result = data_sync.sync_employees(
    source_table=SOURCE_TABLE,
    column_mapping=COLUMN_MAPPING,
    where_clause=WHERE_CLAUSE,
    limit=LIMIT,
    dry_run=False  # Actually insert data
)

end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

# ============================================================================
# RESULTS
# ============================================================================

print()
print('='*80)
print('SYNC RESULTS')
print('='*80)
print()

if result['success']:
    print('✅ Sync completed successfully!')
    print()
    
    stats = result['stats']
    print('Statistics:')
    print(f'  Total rows from source: {stats["total_source"]:,}')
    print(f'  Created (new):          {stats["created"]:,}')
    print(f'  Updated (existing):     {stats["updated"]:,}')
    print(f'  Skipped:                {stats["skipped"]:,}')
    print(f'  Errors:                 {stats["errors"]:,}')
    print()
    print(f'Duration: {duration:.2f} seconds')
    print()
    
    if stats['errors'] > 0:
        print('⚠️  Some errors occurred:')
        for error in stats.get('error_details', [])[:5]:
            print(f'  - {error["error"]}')
        if len(stats.get('error_details', [])) > 5:
            print(f'  ... and {len(stats["error_details"]) - 5} more errors')
        print()
    
    # Verify sync
    print('VERIFYING SYNC...')
    print('-'*80)
    
    with db_manager.get_session() as session:
        employee_stats = EmployeeRepository.get_statistics(session)
        
        print(f'✅ Thesis database now has:')
        print(f'   Total employees:        {employee_stats["total_employees"]:,}')
        print(f'   Promoted:               {employee_stats["promoted_count"]:,} ({employee_stats["promotion_rate"]:.2f}%)')
        print(f'   With Quick Assessment:  {employee_stats["with_quick_assessment"]:,}')
        print(f'   Avg Performance Score:  {employee_stats["avg_performance_score"]:.2f}')
        print(f'   Avg Behavioral Score:   {employee_stats["avg_behavioral_score"]:.2f}')
    
    print()
    print('='*80)
    print('NEXT STEPS:')
    print('='*80)
    print()
    print('1. Verify data in thesis database')
    print('2. Update Streamlit app to use database instead of CSV')
    print('3. Setup scheduled sync (cron job or task scheduler)')
    print('4. Test prediction logging')
    print()
    print('To schedule regular syncs:')
    print('  # Linux/Mac (crontab)')
    print('  0 2 * * * cd /path/to/project && python scripts/database/sync_employees.py')
    print()
    print('  # Windows (Task Scheduler)')
    print('  Create task to run this script daily')
    print()
    
else:
    print('❌ Sync failed!')
    print()
    print(f'Error: {result.get("error")}')
    print()
    
    if result.get('stats'):
        stats = result['stats']
        print('Partial statistics:')
        print(f'  Processed: {stats["created"] + stats["updated"] + stats["errors"]}')
        print(f'  Errors: {stats["errors"]}')
        print()
    
    print('Troubleshooting:')
    print('  1. Check database connections')
    print('  2. Verify table and column names')
    print('  3. Check logs for detailed error messages')
    print('  4. Run dry run first: python scripts/database/test_data_sync.py')
    print()

print('='*80)
print('SYNC COMPLETE')
print('='*80)
