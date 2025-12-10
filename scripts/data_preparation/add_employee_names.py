"""
Add Employee Names to Dataset
Retrieves actual employee names from source database and adds them to the CSV files
"""

import pandas as pd
import psycopg2
from pathlib import Path
import os
from dotenv import load_dotenv
import hashlib

# Load environment variables
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(env_path)

print('='*80)
print('ADD EMPLOYEE NAMES TO DATASET')
print('='*80)
print()

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('SOURCE_DB_HOST', 'localhost'),
    'port': os.getenv('SOURCE_DB_PORT', '5433'),
    'database': os.getenv('SOURCE_DB_DATABASE', 'db_digispace_cna_augustus_182025'),
    'user': os.getenv('SOURCE_DB_USER', 'postgres'),
    'password': os.getenv('SOURCE_DB_PASSWORD', '')
}

# Paths
repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data' / 'final'

print('1. CONNECTING TO DATABASE')
print('-'*80)

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print(f'✅ Connected to database: {DB_CONFIG["database"]}')
    print()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    print()
    print('💡 Tip: Menggunakan nama dummy sebagai fallback')
    conn = None
    cursor = None

# ============================================================================
# 2. LOAD EXISTING DATASETS
# ============================================================================

print('2. LOADING EXISTING DATASETS')
print('-'*80)

datasets = {
    'integrated_performance_behavioral.csv': None,
    'integrated_full_dataset.csv': None
}

for filename in datasets.keys():
    filepath = data_dir / filename
    if filepath.exists():
        datasets[filename] = pd.read_csv(filepath)
        print(f'✅ Loaded: {filename} ({len(datasets[filename]):,} rows)')
    else:
        print(f'⚠️  Not found: {filename}')

print()

# ============================================================================
# 3. GET EMPLOYEE NAMES FROM DATABASE
# ============================================================================

print('3. RETRIEVING EMPLOYEE NAMES')
print('-'*80)

employee_names = {}

if conn and cursor:
    try:
        # Query to get employee names
        # Adjust table and column names based on your actual database schema
        query = """
        SELECT 
            id,
            name,
            email
        FROM employees
        ORDER BY id
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f'✅ Retrieved {len(results):,} employee records from database')
        
        # Create mapping: employee_id_hash -> name
        for emp_id, name, email in results:
            # Create hash (same method as in export script)
            emp_hash = hashlib.md5(str(emp_id).encode()).hexdigest()
            employee_names[emp_hash] = name if name else f"Employee {emp_id}"
        
        print(f'✅ Created {len(employee_names):,} employee name mappings')
        print()
        
    except Exception as e:
        print(f'⚠️  Database query failed: {e}')
        print('💡 Will use generated names instead')
        print()
        conn = None
else:
    print('⚠️  No database connection - will generate names')
    print()

# ============================================================================
# 4. ADD NAMES TO DATASETS
# ============================================================================

print('4. ADDING NAMES TO DATASETS')
print('-'*80)

# Indonesian first names for realistic dummy names
INDONESIAN_FIRST_NAMES = [
    'Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fitri', 'Gita', 'Hadi',
    'Indra', 'Joko', 'Kartika', 'Lina', 'Made', 'Nita', 'Omar', 'Putri',
    'Rudi', 'Sari', 'Tono', 'Umar', 'Vina', 'Wati', 'Yanto', 'Zaki',
    'Agus', 'Bayu', 'Candra', 'Dian', 'Erna', 'Fajar', 'Gilang', 'Hendra',
    'Ika', 'Johan', 'Kiki', 'Lestari', 'Mega', 'Novi', 'Oki', 'Pramono',
    'Qori', 'Rina', 'Sinta', 'Tari', 'Umi', 'Vera', 'Wawan', 'Yudi', 'Zahra'
]

INDONESIAN_LAST_NAMES = [
    'Pratama', 'Wijaya', 'Santoso', 'Kusuma', 'Permana', 'Saputra', 'Wibowo',
    'Nugroho', 'Setiawan', 'Hidayat', 'Kurniawan', 'Firmansyah', 'Ramadhan',
    'Hakim', 'Susanto', 'Prasetyo', 'Gunawan', 'Sutanto', 'Maulana', 'Irawan',
    'Budiman', 'Suryanto', 'Hartono', 'Darmawan', 'Purnomo', 'Suharto',
    'Wahyudi', 'Hermawan', 'Yulianto', 'Cahyono', 'Sugiarto', 'Rachman',
    'Iskandar', 'Mahendra', 'Adiputra', 'Nugraha', 'Sasmita', 'Kusumah'
]

def generate_indonesian_name(employee_hash):
    """Generate realistic Indonesian name from hash"""
    # Use hash to deterministically select names
    hash_int = int(employee_hash[:8], 16)
    first_idx = hash_int % len(INDONESIAN_FIRST_NAMES)
    last_idx = (hash_int // 100) % len(INDONESIAN_LAST_NAMES)
    
    first_name = INDONESIAN_FIRST_NAMES[first_idx]
    last_name = INDONESIAN_LAST_NAMES[last_idx]
    
    return f"{first_name} {last_name}"

for filename, df in datasets.items():
    if df is None:
        continue
    
    print(f'\nProcessing: {filename}')
    print('-'*40)
    
    # Add name column
    if 'name' not in df.columns:
        if employee_names:
            # Use actual names from database
            df['name'] = df['employee_id_hash'].map(employee_names)
            
            # Fill missing with generated names
            missing_mask = df['name'].isna()
            if missing_mask.any():
                df.loc[missing_mask, 'name'] = df.loc[missing_mask, 'employee_id_hash'].apply(
                    generate_indonesian_name
                )
                print(f'  ✅ Added {(~missing_mask).sum():,} actual names from database')
                print(f'  ✅ Generated {missing_mask.sum():,} names for missing records')
        else:
            # Generate all names
            df['name'] = df['employee_id_hash'].apply(generate_indonesian_name)
            print(f'  ✅ Generated {len(df):,} Indonesian names')
        
        # Reorder columns to put name after employee_id_hash
        cols = df.columns.tolist()
        if 'employee_id_hash' in cols:
            hash_idx = cols.index('employee_id_hash')
            cols.insert(hash_idx + 1, cols.pop(cols.index('name')))
            df = df[cols]
        
        # Save updated dataset
        output_path = data_dir / filename
        df.to_csv(output_path, index=False)
        print(f'  ✅ Saved: {output_path}')
        
        # Show sample
        print(f'\n  Sample names:')
        for i, row in df.head(5).iterrows():
            print(f'    - {row["name"]} (ID: {row["employee_id_hash"][:16]}...)')
    else:
        print(f'  ℹ️  Name column already exists')

print()

# ============================================================================
# 5. CREATE NAME MAPPING FILE
# ============================================================================

print('5. CREATING NAME MAPPING FILE')
print('-'*80)

# Create a mapping file for reference
if datasets['integrated_performance_behavioral.csv'] is not None:
    df = datasets['integrated_performance_behavioral.csv']
    
    mapping_df = df[['employee_id_hash', 'name']].copy()
    mapping_df = mapping_df.sort_values('name')
    
    mapping_path = data_dir / 'employee_name_mapping.csv'
    mapping_df.to_csv(mapping_path, index=False)
    
    print(f'✅ Created name mapping file: {mapping_path}')
    print(f'   Total mappings: {len(mapping_df):,}')
    print()

# ============================================================================
# 6. STATISTICS
# ============================================================================

print('6. STATISTICS')
print('-'*80)

for filename, df in datasets.items():
    if df is not None and 'name' in df.columns:
        print(f'\n{filename}:')
        print(f'  Total employees: {len(df):,}')
        print(f'  Unique names: {df["name"].nunique():,}')
        print(f'  Sample names:')
        for name in df['name'].head(10):
            print(f'    - {name}')

print()

# Close database connection
if conn:
    cursor.close()
    conn.close()
    print('✅ Database connection closed')

print()
print('='*80)
print('EMPLOYEE NAMES ADDED SUCCESSFULLY!')
print('='*80)
print()
print('Next steps:')
print('1. Refresh Streamlit app (browser)')
print('2. Navigate to: 👥 Promotion Candidates')
print('3. Employee names should now display!')
print()
print('Note: Names are deterministic - same hash always generates same name')
print('      This ensures consistency across sessions.')
print()
