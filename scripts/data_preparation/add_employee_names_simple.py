"""
Add Employee Names to Dataset (Simple Version)
Generates realistic Indonesian names for all employees
No database connection required
"""

import pandas as pd
from pathlib import Path

print('='*80)
print('ADD EMPLOYEE NAMES TO DATASET (SIMPLE VERSION)')
print('='*80)
print()

# Paths
repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data' / 'final'

# Indonesian names for realistic dummy data
INDONESIAN_FIRST_NAMES = [
    'Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fitri', 'Gita', 'Hadi',
    'Indra', 'Joko', 'Kartika', 'Lina', 'Made', 'Nita', 'Omar', 'Putri',
    'Rudi', 'Sari', 'Tono', 'Umar', 'Vina', 'Wati', 'Yanto', 'Zaki',
    'Agus', 'Bayu', 'Candra', 'Dian', 'Erna', 'Fajar', 'Gilang', 'Hendra',
    'Ika', 'Johan', 'Kiki', 'Lestari', 'Mega', 'Novi', 'Oki', 'Pramono',
    'Qori', 'Rina', 'Sinta', 'Tari', 'Umi', 'Vera', 'Wawan', 'Yudi', 'Zahra',
    'Aditya', 'Bella', 'Cahya', 'Dimas', 'Elsa', 'Faisal', 'Gina', 'Haris',
    'Intan', 'Jaya', 'Karina', 'Lukman', 'Maya', 'Nanda', 'Olivia', 'Putra',
    'Qonita', 'Reza', 'Siska', 'Taufik', 'Ulfa', 'Vino', 'Wulan', 'Yoga', 'Zainal'
]

INDONESIAN_LAST_NAMES = [
    'Pratama', 'Wijaya', 'Santoso', 'Kusuma', 'Permana', 'Saputra', 'Wibowo',
    'Nugroho', 'Setiawan', 'Hidayat', 'Kurniawan', 'Firmansyah', 'Ramadhan',
    'Hakim', 'Susanto', 'Prasetyo', 'Gunawan', 'Sutanto', 'Maulana', 'Irawan',
    'Budiman', 'Suryanto', 'Hartono', 'Darmawan', 'Purnomo', 'Suharto',
    'Wahyudi', 'Hermawan', 'Yulianto', 'Cahyono', 'Sugiarto', 'Rachman',
    'Iskandar', 'Mahendra', 'Adiputra', 'Nugraha', 'Sasmita', 'Kusumah',
    'Wicaksono', 'Prabowo', 'Sanjaya', 'Utomo', 'Harahap', 'Siregar',
    'Nasution', 'Lubis', 'Situmorang', 'Simbolon', 'Tampubolon', 'Sinaga'
]

def generate_indonesian_name(employee_hash):
    """Generate realistic Indonesian name from hash (deterministic)"""
    # Use hash to deterministically select names
    hash_int = int(employee_hash[:8], 16)
    first_idx = hash_int % len(INDONESIAN_FIRST_NAMES)
    last_idx = (hash_int // 100) % len(INDONESIAN_LAST_NAMES)
    
    first_name = INDONESIAN_FIRST_NAMES[first_idx]
    last_name = INDONESIAN_LAST_NAMES[last_idx]
    
    return f"{first_name} {last_name}"

# ============================================================================
# PROCESS DATASETS
# ============================================================================

print('1. LOADING DATASETS')
print('-'*80)

datasets_to_process = [
    'integrated_performance_behavioral.csv',
    'integrated_full_dataset.csv'
]

processed_count = 0

for filename in datasets_to_process:
    filepath = data_dir / filename
    
    if not filepath.exists():
        print(f'⚠️  Not found: {filename}')
        continue
    
    print(f'\n📂 Processing: {filename}')
    print('-'*40)
    
    # Load dataset
    df = pd.read_csv(filepath)
    print(f'  ✅ Loaded: {len(df):,} rows')
    
    # Check if name column exists
    if 'name' in df.columns:
        print(f'  ℹ️  Name column already exists')
        
        # Check if names need updating (if they're still "Employee XXXXX" format)
        sample_name = df['name'].iloc[0]
        if sample_name.startswith('Employee ') and len(sample_name.split()) == 2:
            print(f'  🔄 Updating generic names to Indonesian names...')
            df['name'] = df['employee_id_hash'].apply(generate_indonesian_name)
            needs_save = True
        else:
            print(f'  ✅ Names look good: "{sample_name}"')
            needs_save = False
    else:
        print(f'  ➕ Adding name column...')
        df['name'] = df['employee_id_hash'].apply(generate_indonesian_name)
        needs_save = True
        
        # Reorder columns to put name after employee_id_hash
        cols = df.columns.tolist()
        if 'employee_id_hash' in cols:
            hash_idx = cols.index('employee_id_hash')
            cols.insert(hash_idx + 1, cols.pop(cols.index('name')))
            df = df[cols]
    
    # Save if needed
    if needs_save:
        df.to_csv(filepath, index=False)
        print(f'  💾 Saved: {filepath}')
        processed_count += 1
    
    # Show sample names
    print(f'\n  📋 Sample names:')
    for i, row in df.head(10).iterrows():
        emp_id_short = row['employee_id_hash'][:12]
        print(f'    {i+1:2d}. {row["name"]:<25} (ID: {emp_id_short}...)')
    
    print(f'\n  📊 Statistics:')
    print(f'    - Total employees: {len(df):,}')
    print(f'    - Unique names: {df["name"].nunique():,}')
    
    # Check for duplicate names
    duplicates = df['name'].value_counts()
    duplicates = duplicates[duplicates > 1]
    if len(duplicates) > 0:
        print(f'    - Duplicate names: {len(duplicates):,} (this is normal with {len(df):,} employees)')
        print(f'      Top duplicates:')
        for name, count in duplicates.head(3).items():
            print(f'        • {name}: {count} employees')

print()
print('='*80)

if processed_count > 0:
    print(f'✅ SUCCESS! Updated {processed_count} dataset(s) with Indonesian names')
else:
    print('✅ All datasets already have names')

print('='*80)
print()

# ============================================================================
# CREATE NAME MAPPING FILE
# ============================================================================

print('2. CREATING NAME MAPPING FILE')
print('-'*80)

main_dataset = data_dir / 'integrated_performance_behavioral.csv'
if main_dataset.exists():
    df = pd.read_csv(main_dataset)
    
    if 'name' in df.columns:
        mapping_df = df[['employee_id_hash', 'name']].copy()
        mapping_df = mapping_df.sort_values('name')
        
        mapping_path = data_dir / 'employee_name_mapping.csv'
        mapping_df.to_csv(mapping_path, index=False)
        
        print(f'✅ Created: {mapping_path}')
        print(f'   Total mappings: {len(mapping_df):,}')
        print()

# ============================================================================
# NEXT STEPS
# ============================================================================

print('='*80)
print('🎉 EMPLOYEE NAMES READY!')
print('='*80)
print()
print('📝 What was done:')
print('  ✅ Generated realistic Indonesian names')
print('  ✅ Names are deterministic (same hash = same name)')
print('  ✅ Updated all dataset files')
print('  ✅ Created name mapping file')
print()
print('🚀 Next steps:')
print('  1. Refresh your Streamlit app (browser)')
print('  2. Navigate to: 👥 Promotion Candidates')
print('  3. You should now see names like:')
print('     • Andi Pratama')
print('     • Dewi Kusuma')
print('     • Budi Wijaya')
print('     • etc.')
print()
print('💡 Notes:')
print('  • Names are generated from employee_id_hash')
print('  • Same employee always gets same name')
print('  • Names are realistic Indonesian names')
print('  • Some duplicate names are normal (like real companies)')
print()
print('📂 Files updated:')
for filename in datasets_to_process:
    filepath = data_dir / filename
    if filepath.exists():
        print(f'  ✅ {filename}')
print()
