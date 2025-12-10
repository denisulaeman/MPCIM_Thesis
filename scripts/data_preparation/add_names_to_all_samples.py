"""
Add Names to ALL Sample Files
Including sample_dataset_100_balanced.csv
"""

import pandas as pd
from pathlib import Path

print('='*80)
print('ADD NAMES TO ALL SAMPLE FILES')
print('='*80)
print()

# Paths
repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data' / 'final'

# Indonesian names
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
    hash_int = int(employee_hash[:8], 16)
    first_idx = hash_int % len(INDONESIAN_FIRST_NAMES)
    last_idx = (hash_int // 100) % len(INDONESIAN_LAST_NAMES)
    
    first_name = INDONESIAN_FIRST_NAMES[first_idx]
    last_name = INDONESIAN_LAST_NAMES[last_idx]
    
    return f"{first_name} {last_name}"

# Process ALL sample files
sample_files = [
    'sample_dataset_100_balanced.csv',
    'sample_dataset_100.csv',
    'sample_dataset_1000_balanced.csv',
    'sample_dataset_1000_balanced_normalized.csv',
    'integrated_performance_behavioral.csv',
    'integrated_full_dataset.csv'
]

processed = 0

for filename in sample_files:
    filepath = data_dir / filename
    
    if not filepath.exists():
        print(f'⚠️  Not found: {filename}')
        continue
    
    print(f'\n📂 Processing: {filename}')
    print('-'*40)
    
    # Load
    df = pd.read_csv(filepath)
    print(f'  ✅ Loaded: {len(df):,} rows')
    
    # Check/add name column
    if 'name' not in df.columns:
        print(f'  ➕ Adding name column...')
        df['name'] = df['employee_id_hash'].apply(generate_indonesian_name)
        
        # Reorder columns
        cols = df.columns.tolist()
        if 'employee_id_hash' in cols:
            hash_idx = cols.index('employee_id_hash')
            cols.insert(hash_idx + 1, cols.pop(cols.index('name')))
            df = df[cols]
        
        # Save
        df.to_csv(filepath, index=False)
        print(f'  💾 Saved with names')
        processed += 1
    else:
        # Check if names need updating
        sample_name = df['name'].iloc[0]
        if sample_name.startswith('Employee ') and len(sample_name.split()) == 2:
            print(f'  🔄 Updating generic names...')
            df['name'] = df['employee_id_hash'].apply(generate_indonesian_name)
            df.to_csv(filepath, index=False)
            print(f'  💾 Updated with Indonesian names')
            processed += 1
        else:
            print(f'  ✅ Names already good: "{sample_name}"')
    
    # Show samples
    print(f'\n  📋 Sample names:')
    for i, row in df.head(5).iterrows():
        print(f'    {i+1}. {row["name"]:<25} (ID: {row["employee_id_hash"][:12]}...)')

print()
print('='*80)
if processed > 0:
    print(f'✅ SUCCESS! Updated {processed} file(s) with Indonesian names')
else:
    print('✅ All files already have names')
print('='*80)
print()
print('🚀 Next: Refresh Streamlit and test!')
print()
