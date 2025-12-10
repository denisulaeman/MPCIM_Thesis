"""
MPCIM Thesis - Migrate CSV Data to Database
Author: Deni Sulaeman
Date: November 22, 2025

Migrate existing CSV data to PostgreSQL/SQLite database.
"""

import sys
from pathlib import Path
import pandas as pd
from tqdm import tqdm

# Add app directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'app'))

from database import (
    db_manager,
    init_database,
    EmployeeRepository,
    ModelPerformanceRepository
)

print('='*80)
print('MPCIM THESIS - CSV TO DATABASE MIGRATION')
print('='*80)
print()

# ============================================================================
# 1. INITIALIZE DATABASE
# ============================================================================

print('1. INITIALIZING DATABASE')
print('-'*80)

try:
    init_database()
    print('✅ Database initialized')
except Exception as e:
    print(f'❌ Error initializing database: {e}')
    sys.exit(1)

# Check health
health = db_manager.health_check()
if not health:
    print('❌ Database health check failed')
    sys.exit(1)

print('✅ Database health check passed')
print()

# ============================================================================
# 2. LOAD CSV DATA
# ============================================================================

print('2. LOADING CSV DATA')
print('-'*80)

repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data' / 'final'

csv_file = data_dir / 'integrated_performance_behavioral.csv'

if not csv_file.exists():
    print(f'❌ CSV file not found: {csv_file}')
    sys.exit(1)

df = pd.read_csv(csv_file)
print(f'✅ Loaded {len(df):,} records from CSV')
print(f'   Columns: {list(df.columns)}')
print()

# ============================================================================
# 3. MIGRATE EMPLOYEES
# ============================================================================

print('3. MIGRATING EMPLOYEES TO DATABASE')
print('-'*80)

# Column mapping
column_mapping = {
    'NIK': 'employee_id',
    'Nama': 'name',
    'Gender': 'gender',
    'Status Pernikahan': 'marital_status',
    'Status Karyawan': 'is_permanent',
    'Performance Score': 'performance_score',
    'Performance Rating': 'performance_rating',
    'Behavioral Score': 'behavioral_score',
    'Collaboration Score': 'collaboration_score',
    'Leadership Score': 'leadership_score',
    'Tenure (Years)': 'tenure_years',
    'Has Promotion': 'has_promotion',
    # Quick Assessment columns (if available)
    'Psychological Score': 'psychological_score',
    'Drive Score': 'drive_score',
    'Mental Strength Score': 'mental_strength_score',
    'Adaptability Score': 'adaptability_score',
}

# Check which columns exist
available_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
print(f'Available columns: {len(available_columns)}/{len(column_mapping)}')
print()

migrated_count = 0
skipped_count = 0
error_count = 0

with db_manager.get_session() as session:
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Migrating"):
        try:
            # Prepare employee data
            employee_data = {}
            
            for csv_col, db_col in available_columns.items():
                value = row[csv_col]
                
                # Handle NaN values
                if pd.isna(value):
                    value = None
                
                # Type conversions
                if db_col == 'is_permanent':
                    value = str(value).lower() in ['permanent', 'true', '1', 'yes']
                elif db_col == 'has_promotion':
                    value = bool(value) if not pd.isna(value) else False
                elif db_col in ['performance_score', 'behavioral_score', 'tenure_years',
                               'psychological_score', 'drive_score', 'mental_strength_score',
                               'adaptability_score', 'collaboration_score', 'leadership_score']:
                    value = float(value) if not pd.isna(value) else None
                
                employee_data[db_col] = value
            
            # Check if employee_id exists
            if not employee_data.get('employee_id'):
                skipped_count += 1
                continue
            
            # Check if employee already exists
            existing = EmployeeRepository.get_by_id(
                session, 
                str(employee_data['employee_id'])
            )
            
            if existing:
                # Update existing
                EmployeeRepository.update(
                    session,
                    str(employee_data['employee_id']),
                    **employee_data
                )
            else:
                # Create new
                # Check if has Quick Assessment data
                has_qa = any([
                    employee_data.get('psychological_score'),
                    employee_data.get('drive_score'),
                    employee_data.get('mental_strength_score'),
                    employee_data.get('adaptability_score')
                ])
                employee_data['has_quick_assessment'] = has_qa
                
                EmployeeRepository.create(session, **employee_data)
            
            migrated_count += 1
            
        except Exception as e:
            error_count += 1
            print(f'\n❌ Error migrating row {idx}: {e}')
            continue

print()
print(f'✅ Migration complete!')
print(f'   Migrated: {migrated_count}')
print(f'   Skipped: {skipped_count}')
print(f'   Errors: {error_count}')
print()

# ============================================================================
# 4. VERIFY MIGRATION
# ============================================================================

print('4. VERIFYING MIGRATION')
print('-'*80)

with db_manager.get_session() as session:
    stats = EmployeeRepository.get_statistics(session)
    
    print(f'📊 Database Statistics:')
    print(f'   Total employees: {stats["total_employees"]}')
    print(f'   Promoted: {stats["promoted_count"]} ({stats["promotion_rate"]:.2f}%)')
    print(f'   With Quick Assessment: {stats["with_quick_assessment"]}')
    print(f'   Avg Performance Score: {stats["avg_performance_score"]:.2f}')
    print(f'   Avg Behavioral Score: {stats["avg_behavioral_score"]:.2f}')

print()

# ============================================================================
# 5. MIGRATE MODEL PERFORMANCE (OPTIONAL)
# ============================================================================

print('5. MIGRATING MODEL PERFORMANCE DATA')
print('-'*80)

results_dir = repo_root / 'results' / 'advanced_models'
comparison_file = results_dir / 'model_comparison.csv'

if comparison_file.exists():
    comparison_df = pd.read_csv(comparison_file)
    
    with db_manager.get_session() as session:
        for _, row in comparison_df.iterrows():
            try:
                ModelPerformanceRepository.create(
                    session,
                    model_name=row['Model'],
                    accuracy=row['Accuracy'],
                    precision_score=row['Precision'],
                    recall=row['Recall'],
                    f1_score=row['F1-Score'],
                    roc_auc=row['ROC-AUC'],
                    notes='Migrated from CSV'
                )
            except Exception as e:
                print(f'⚠️  Error migrating model performance: {e}')
    
    print(f'✅ Migrated {len(comparison_df)} model performance records')
else:
    print('ℹ️  No model performance data found')

print()

# ============================================================================
# COMPLETION
# ============================================================================

print('='*80)
print('✅ MIGRATION COMPLETE!')
print('='*80)
print()
print('Next steps:')
print('  1. Verify data in database')
print('  2. Update Streamlit app to use database')
print('  3. Test prediction logging')
print('  4. Setup backup strategy')
print()
print('Database connection info:')
conn_info = db_manager.get_connection_info()
for key, value in conn_info.items():
    print(f'  {key}: {value}')
