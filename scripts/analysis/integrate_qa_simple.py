"""
Simple Quick Assessment Integration
====================================
Menggunakan sample_dataset_1000_balanced.csv yang sudah memiliki
data psychological sebagai dataset utama untuk training.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import shutil

print("=" * 80)
print("QUICK ASSESSMENT INTEGRATION - SIMPLE APPROACH")
print("=" * 80)
print()

# Setup paths
repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / "data"
final_dir = data_dir / "final"

# Load dataset yang sudah ada psychological data
print("1. Loading dataset with psychological data...")
source_file = final_dir / "sample_dataset_1000_balanced.csv"
df = pd.read_csv(source_file)

print(f"   ✓ Loaded: {df.shape}")
print(f"   ✓ Columns: {len(df.columns)}")
print()

# Verify psychological columns exist
print("2. Verifying psychological columns...")
psychological_cols = [
    'psychological_score',
    'drive_score',
    'mental_strength_score',
    'adaptability_score',
    'collaboration_score',
    'has_quick_assessment',
    'holistic_score',
    'score_alignment',
    'leadership_potential'
]

missing_cols = [col for col in psychological_cols if col not in df.columns]
if missing_cols:
    print(f"   ❌ Missing columns: {missing_cols}")
    exit(1)
else:
    print(f"   ✅ All psychological columns present!")
    for col in psychological_cols:
        print(f"      - {col}: {df[col].notna().sum()}/{len(df)} non-null")
print()

# Statistics
print("3. Psychological Data Statistics:")
print(df[psychological_cols].describe())
print()

# Save as integrated_full_dataset.csv
print("4. Saving as integrated_full_dataset.csv...")
output_file = final_dir / "integrated_full_dataset.csv"
df.to_csv(output_file, index=False)
print(f"   ✓ Saved to: {output_file}")
print()

# Summary
print("=" * 80)
print("INTEGRATION COMPLETE!")
print("=" * 80)
print(f"Dataset: {len(df)} records with {len(df.columns)} features")
print()
print("Psychological Features:")
for col in psychological_cols:
    mean_val = df[col].mean()
    print(f"  - {col}: mean={mean_val:.2f}")
print()
print("Promotion Distribution:")
print(df.groupby('has_promotion').size())
print()
print("Ready for feature engineering and model training!")
print()
