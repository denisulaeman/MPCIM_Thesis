"""
MPCIM Thesis - Test Data Sync (Dry Run)
Author: Deni Sulaeman
Date: November 22, 2025

Test data synchronization without actually inserting data.
"""

import sys
from pathlib import Path
import logging

# Add app directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'app'))

from database.data_sync import data_sync

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

print('='*80)
print('MPCIM THESIS - DATA SYNC TEST (DRY RUN)')
print('='*80)
print()

# ============================================================================
# CONFIGURATION
# ============================================================================

# TODO: Update these based on your source database schema
SOURCE_TABLE = 'employees'  # Change this to your actual table name

# TODO: Update column mapping based on your source table
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
    # Add Quick Assessment columns if available
    # 'psychological_score': 'psychological_score',
    # 'drive_score': 'drive_score',
}

# Optional: Filter data
WHERE_CLAUSE = None  # e.g., "status = 'active'"
LIMIT = 10  # Test with small number first

print('CONFIGURATION:')
print('-'*80)
print(f'Source Table: {SOURCE_TABLE}')
print(f'Column Mapping: {len(COLUMN_MAPPING)} columns')
print(f'Where Clause: {WHERE_CLAUSE or "None"}')
print(f'Limit: {LIMIT}')
print()

# ============================================================================
# DRY RUN SYNC
# ============================================================================

print('RUNNING DRY RUN SYNC...')
print('-'*80)
print()

result = data_sync.sync_employees(
    source_table=SOURCE_TABLE,
    column_mapping=COLUMN_MAPPING,
    where_clause=WHERE_CLAUSE,
    limit=LIMIT,
    dry_run=True  # Don't actually insert data
)

# ============================================================================
# RESULTS
# ============================================================================

print('='*80)
print('DRY RUN RESULTS')
print('='*80)
print()

if result['success']:
    print('✅ Dry run successful!')
    print()
    
    stats = result['stats']
    print('Statistics:')
    print(f'  Total rows from source: {stats["total_source"]}')
    print()
    
    if result.get('sample_data'):
        print('Sample Data (first 3 rows):')
        print('-'*80)
        
        for i, row in enumerate(result['sample_data'][:3], 1):
            print(f'\nRow {i}:')
            for key, value in list(row.items())[:8]:  # Show first 8 columns
                print(f'  {key:25} = {value}')
            if len(row) > 8:
                print(f'  ... and {len(row) - 8} more columns')
        print()
    
    print('='*80)
    print('NEXT STEPS:')
    print('='*80)
    print()
    print('1. Review the sample data above')
    print('2. Verify column mapping is correct')
    print('3. If everything looks good, run actual sync:')
    print()
    print('   python scripts/database/sync_employees.py')
    print()
    print('4. Or customize the sync in sync_employees.py')
    print()
    
else:
    print('❌ Dry run failed!')
    print()
    print(f'Error: {result.get("error")}')
    print()
    print('Possible issues:')
    print('  1. Source table name is incorrect')
    print('  2. Column names in mapping are wrong')
    print('  3. Source database connection failed')
    print('  4. Permissions issue')
    print()
    print('To debug:')
    print('  1. Run: python scripts/database/setup_dual_database.py')
    print('  2. Check the table list and column names')
    print('  3. Update SOURCE_TABLE and COLUMN_MAPPING in this script')
    print()
