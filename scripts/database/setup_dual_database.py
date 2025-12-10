"""
MPCIM Thesis - Setup Dual Database
Author: Deni Sulaeman
Date: November 22, 2025

Setup and test dual database connection:
1. Source DB (DigiSpace CNA) - Read only
2. Thesis DB (MPCIM) - Read/Write
"""

import sys
from pathlib import Path
import logging

# Add app directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'app'))

from database.dual_connection import dual_db, test_connections
from database.data_sync import data_sync, discover_schema
from database import init_database

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print('='*80)
print('MPCIM THESIS - DUAL DATABASE SETUP')
print('='*80)
print()

# ============================================================================
# STEP 1: TEST CONNECTIONS
# ============================================================================

print('STEP 1: TESTING DATABASE CONNECTIONS')
print('='*80)
print()

test_connections()

status = dual_db.get_connection_status()

if not status['source_db']['connected']:
    print('❌ SOURCE DATABASE NOT CONNECTED!')
    print()
    print('Please check:')
    print('  1. PostgreSQL is running on port 5433')
    print('  2. Database "db_digispace_cna_augustus_182025" exists')
    print('  3. Credentials in .env are correct')
    print('  4. You have read permissions')
    print()
    print('To start PostgreSQL:')
    print('  brew services start postgresql@14')
    print()
    sys.exit(1)

if not status['thesis_db']['connected']:
    print('⚠️  THESIS DATABASE NOT CONNECTED')
    print('   Will create new database...')
    print()

# ============================================================================
# STEP 2: CREATE THESIS DATABASE
# ============================================================================

print('STEP 2: INITIALIZING THESIS DATABASE')
print('='*80)
print()

try:
    # First, create the database if it doesn't exist
    print('Creating database "mpcim_thesis" if not exists...')
    
    # You might need to run this manually:
    # psql -U postgres -c "CREATE DATABASE mpcim_thesis;"
    
    # Initialize tables
    print('Creating tables...')
    init_database()
    print('✅ Thesis database initialized')
    print()
    
except Exception as e:
    print(f'❌ Error initializing thesis database: {e}')
    print()
    print('Please create the database manually:')
    print('  psql -U postgres -c "CREATE DATABASE mpcim_thesis;"')
    print()
    sys.exit(1)

# ============================================================================
# STEP 3: DISCOVER SOURCE DATABASE SCHEMA
# ============================================================================

print('STEP 3: DISCOVERING SOURCE DATABASE SCHEMA')
print('='*80)
print()

schema_info = discover_schema()

if not schema_info['success']:
    print(f'❌ Error discovering schema: {schema_info.get("error")}')
    sys.exit(1)

print(f'✅ Found {schema_info["table_count"]} tables in source database')
print()

# Show tables with employee-related data
print('Available tables:')
print('-'*80)

employee_related = []
for table_name, info in schema_info['tables'].items():
    row_count = info['row_count']
    col_count = len(info['columns'])
    
    # Check if table might contain employee data
    columns = [c['name'].lower() for c in info['columns']]
    is_employee_related = any(keyword in ' '.join(columns) 
                             for keyword in ['employee', 'staff', 'karyawan', 
                                           'performance', 'behavioral', 'promotion'])
    
    if is_employee_related or 'employee' in table_name.lower():
        employee_related.append(table_name)
        print(f'  ⭐ {table_name:40} {row_count:>8} rows, {col_count:>3} columns')
    else:
        print(f'     {table_name:40} {row_count:>8} rows, {col_count:>3} columns')

print()

if employee_related:
    print(f'📊 Found {len(employee_related)} employee-related tables:')
    for table in employee_related:
        print(f'   - {table}')
    print()
    
    # Show detailed info for first employee table
    if employee_related:
        first_table = employee_related[0]
        print(f'Detailed info for "{first_table}":')
        print('-'*80)
        
        table_info = schema_info['tables'][first_table]
        print(f'Columns ({len(table_info["columns"])}):')
        for col in table_info['columns'][:20]:  # Show first 20 columns
            nullable = '(nullable)' if col['nullable'] else '(required)'
            print(f'  - {col["name"]:30} {col["type"]:20} {nullable}')
        
        if len(table_info['columns']) > 20:
            print(f'  ... and {len(table_info["columns"]) - 20} more columns')
        print()

# ============================================================================
# STEP 4: SAMPLE DATA FROM SOURCE
# ============================================================================

print('STEP 4: SAMPLING DATA FROM SOURCE DATABASE')
print('='*80)
print()

if employee_related:
    sample_table = employee_related[0]
    print(f'Getting sample data from "{sample_table}"...')
    
    try:
        sample_data = data_sync.get_source_data(
            sample_table,
            limit=5
        )
        
        if sample_data:
            print(f'✅ Retrieved {len(sample_data)} sample rows')
            print()
            print('Sample row (first row):')
            print('-'*80)
            for key, value in list(sample_data[0].items())[:10]:
                print(f'  {key:30} = {value}')
            print()
        else:
            print('⚠️  No data found in table')
            print()
    except Exception as e:
        print(f'❌ Error getting sample data: {e}')
        print()

# ============================================================================
# STEP 5: RECOMMENDATIONS
# ============================================================================

print('STEP 5: NEXT STEPS & RECOMMENDATIONS')
print('='*80)
print()

print('✅ Setup Complete!')
print()
print('📋 Next Steps:')
print()

if employee_related:
    print('1. IDENTIFY YOUR EMPLOYEE TABLE:')
    print(f'   We found these potential tables: {", ".join(employee_related)}')
    print()
    print('2. CREATE COLUMN MAPPING:')
    print('   Edit app/database/data_sync.py and update source_table_mapping')
    print('   Map your source columns to thesis Employee model')
    print()
    print('   Example:')
    print('   ```python')
    print('   source_table_mapping = {')
    print(f'       "{employee_related[0]}": {{')
    print('           "id": "employee_id",')
    print('           "nama": "name",')
    print('           "email": "email",')
    print('           "department": "department",')
    print('           # ... add more mappings')
    print('       }')
    print('   }')
    print('   ```')
    print()
    print('3. TEST SYNC (DRY RUN):')
    print('   python scripts/database/test_data_sync.py')
    print()
    print('4. SYNC DATA:')
    print('   python scripts/database/sync_employees.py')
    print()
else:
    print('⚠️  No employee-related tables found automatically.')
    print()
    print('Please:')
    print('1. Review the table list above')
    print('2. Identify which table contains employee data')
    print('3. Check the column names in that table')
    print('4. Create column mapping in data_sync.py')
    print()

print('5. INTEGRATE WITH STREAMLIT:')
print('   - Update pages to read from thesis database')
print('   - Log predictions to database')
print('   - Show real-time statistics')
print()

print('='*80)
print('SETUP COMPLETE!')
print('='*80)
