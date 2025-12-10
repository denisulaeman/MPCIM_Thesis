"""
Job Level Analysis for Promotion Prediction & Succession Planning
==================================================================

Tujuan:
1. Analisis distribusi karyawan per job level
2. Identifikasi promotion paths
3. Feature engineering untuk model prediksi
4. Setup untuk succession planning

Author: Denis Ulaeman
Date: Dec 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
FINAL_DIR = DATA_DIR / "final"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Visualization settings
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("JOB LEVEL ANALYSIS FOR PROMOTION PREDICTION")
print("="*80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1] Loading data...")

# Load reference data
df_job_levels = pd.read_csv(RAW_DIR / "ref_job_levels.csv")
df_job_positions = pd.read_csv(RAW_DIR / "ref_job_positions.csv")

# Load employee data
df_employees = pd.read_csv(RAW_DIR / "01_employee_master.csv")

# Load integrated dataset
df_integrated = pd.read_csv(FINAL_DIR / "integrated_full_dataset.csv")

print(f"✓ Job Levels: {len(df_job_levels)} levels")
print(f"✓ Job Positions: {len(df_job_positions)} positions")
print(f"✓ Employees: {len(df_employees)} employees")
print(f"✓ Integrated Dataset: {len(df_integrated)} records")

# ============================================================================
# 2. JOB LEVEL HIERARCHY ANALYSIS
# ============================================================================
print("\n[2] Analyzing job level hierarchy...")

# Display job level structure
print("\nJob Level Structure:")
print("-" * 60)
df_job_levels_sorted = df_job_levels.sort_values(['group_job_level', 'job_level_id'])
for _, row in df_job_levels_sorted.iterrows():
    group_name = {0: "Support", 1: "Staff/Officer", 2: "Management"}[row['group_job_level']]
    print(f"  Group {row['group_job_level']} ({group_name:15s}) | {row['level_name']}")

# ============================================================================
# 3. EMPLOYEE DISTRIBUTION PER JOB LEVEL
# ============================================================================
print("\n[3] Analyzing employee distribution per job level...")

# Merge employee with job level info
df_emp_with_level = df_employees.merge(
    df_job_levels[['job_level_id', 'level_name', 'group_job_level']], 
    on='job_level_id', 
    how='left'
)

# Count employees per level
level_distribution = df_emp_with_level.groupby(['group_job_level', 'level_name']).agg({
    'employee_id': 'count'
}).rename(columns={'employee_id': 'count'}).reset_index()

level_distribution['percentage'] = (level_distribution['count'] / level_distribution['count'].sum() * 100).round(2)
level_distribution = level_distribution.sort_values('count', ascending=False)

print("\nEmployee Distribution by Job Level:")
print("-" * 80)
print(f"{'Job Level':<30} {'Group':<10} {'Count':<10} {'Percentage':<10}")
print("-" * 80)
for _, row in level_distribution.iterrows():
    group_name = {0: "Support", 1: "Staff", 2: "Management"}[row['group_job_level']]
    print(f"{row['level_name']:<30} {group_name:<10} {row['count']:<10} {row['percentage']:<10.2f}%")
print("-" * 80)
print(f"{'TOTAL':<30} {'':<10} {level_distribution['count'].sum():<10} {100.00:<10.2f}%")

# Check for imbalanced levels
min_threshold = 20  # minimum 20 employees per level
low_count_levels = level_distribution[level_distribution['count'] < min_threshold]

if len(low_count_levels) > 0:
    print(f"\n⚠️  WARNING: {len(low_count_levels)} job levels have <{min_threshold} employees:")
    for _, row in low_count_levels.iterrows():
        print(f"   - {row['level_name']}: {row['count']} employees ({row['percentage']:.2f}%)")
    print("\n   Recommendation: Consider merging these levels with similar levels")
else:
    print(f"\n✓ All job levels have ≥{min_threshold} employees - good for ML!")

# ============================================================================
# 4. PROMOTION ANALYSIS
# ============================================================================
print("\n[4] Analyzing promotion patterns...")

# Merge with promotion history
df_promotions = pd.read_csv(RAW_DIR / "06_promotion_history.csv")

# Count promotions per level
promotion_stats = df_emp_with_level.merge(
    df_promotions.groupby('employee_id')['promotion_id'].count().reset_index().rename(columns={'promotion_id': 'promotion_count'}),
    on='employee_id',
    how='left'
)
promotion_stats['promotion_count'] = promotion_stats['promotion_count'].fillna(0)

# Calculate promotion rate per level
promo_by_level = promotion_stats.groupby('level_name').agg({
    'employee_id': 'count',
    'promotion_count': lambda x: (x > 0).sum()
}).rename(columns={'employee_id': 'total_employees', 'promotion_count': 'promoted_employees'})

promo_by_level['promotion_rate'] = (promo_by_level['promoted_employees'] / promo_by_level['total_employees'] * 100).round(2)
promo_by_level = promo_by_level.sort_values('promotion_rate', ascending=False)

print("\nPromotion Rate by Job Level:")
print("-" * 80)
print(f"{'Job Level':<30} {'Total':<10} {'Promoted':<10} {'Rate':<10}")
print("-" * 80)
for level, row in promo_by_level.iterrows():
    print(f"{level:<30} {row['total_employees']:<10} {row['promoted_employees']:<10} {row['promotion_rate']:<10.2f}%")

# ============================================================================
# 5. SUCCESSION PLANNING FRAMEWORK
# ============================================================================
print("\n[5] Building succession planning framework...")

# Define promotion paths (typical career progression)
promotion_paths = {
    'Non Staff': ['Staff', 'Officer'],
    'Non Pangkat': ['Staff', 'Officer'],
    'Junior Officer': ['Officer', 'Staff'],
    'Officer': ['Assistent Manager', 'Manager'],
    'Staff': ['Assistent Manager', 'Manager'],
    'Assistent Manager': ['Manager', 'Senior Manager'],
    'Manager': ['Senior Manager', 'General Manager'],
    'Senior Manager': ['General Manager', 'Direktur'],
    'General Manager': ['Direktur', 'Direktur Utama'],
    'Direktur': ['Direktur Utama', 'Komisaris'],
    'Direktur Utama': ['Komisaris'],
    'Komisaris': [],  # Top level
    'Temporary Position (PJS)': []  # Special case
}

print("\nCareer Progression Paths:")
print("-" * 60)
for current_level, next_levels in promotion_paths.items():
    if next_levels:
        print(f"  {current_level:<25} → {', '.join(next_levels)}")
    else:
        print(f"  {current_level:<25} → (Top Level)")

# ============================================================================
# 6. FEATURE ENGINEERING FOR PROMOTION PREDICTION
# ============================================================================
print("\n[6] Creating features for promotion prediction...")

# Merge integrated dataset with job level info
df_model = df_integrated.copy()

# Add job level info if not present
if 'job_level_id' not in df_model.columns:
    # Try to get from employee master
    df_model = df_model.merge(
        df_employees[['employee_id_hash', 'job_level_id']],
        left_on='employee_id_hash',
        right_on='employee_id_hash',
        how='left'
    )

if 'job_level_id' in df_model.columns:
    df_model = df_model.merge(
        df_job_levels[['job_level_id', 'level_name', 'group_job_level']],
        on='job_level_id',
        how='left'
    )
    
    # Create job level features
    print("\nJob Level Features Created:")
    print("  ✓ level_name: Categorical job level")
    print("  ✓ group_job_level: Hierarchical group (0=Support, 1=Staff, 2=Management)")
    
    # Create promotion readiness score
    # Higher score = more ready for promotion
    df_model['promotion_readiness_score'] = (
        df_model['performance_score'] * 0.3 +
        df_model['behavior_avg'] * 0.2 +
        df_model['leadership_potential'] * 0.3 +
        df_model['holistic_score'] * 0.2
    )
    
    # Create level-specific features
    df_model['is_management'] = (df_model['group_job_level'] == 2).astype(int)
    df_model['is_staff'] = (df_model['group_job_level'] == 1).astype(int)
    df_model['is_support'] = (df_model['group_job_level'] == 0).astype(int)
    
    # Tenure in current level (proxy - using overall tenure)
    df_model['tenure_level_ratio'] = df_model['tenure_years'] / (df_model['group_job_level'] + 1)
    
    print("  ✓ promotion_readiness_score: Composite score for promotion readiness")
    print("  ✓ is_management/is_staff/is_support: Binary level indicators")
    print("  ✓ tenure_level_ratio: Tenure adjusted by level")
    
    # Save enhanced dataset
    output_file = FINAL_DIR / "integrated_full_dataset_with_job_level.csv"
    df_model.to_csv(output_file, index=False)
    print(f"\n✓ Enhanced dataset saved to: {output_file}")
else:
    print("\n⚠️  Warning: job_level_id not found in dataset")
    print("   Please ensure employee_master.csv has job_level_id column")

# ============================================================================
# 7. VISUALIZATIONS
# ============================================================================
print("\n[7] Creating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Job Level Analysis for Promotion Prediction', fontsize=16, fontweight='bold')

# Plot 1: Employee distribution by job level
ax1 = axes[0, 0]
level_dist_plot = level_distribution.sort_values('count', ascending=True)
ax1.barh(level_dist_plot['level_name'], level_dist_plot['count'], color='steelblue')
ax1.set_xlabel('Number of Employees', fontsize=11)
ax1.set_ylabel('Job Level', fontsize=11)
ax1.set_title('Employee Distribution by Job Level', fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Add count labels
for i, (idx, row) in enumerate(level_dist_plot.iterrows()):
    ax1.text(row['count'] + 5, i, f"{int(row['count'])} ({row['percentage']:.1f}%)", 
             va='center', fontsize=9)

# Plot 2: Promotion rate by job level
ax2 = axes[0, 1]
promo_plot = promo_by_level.sort_values('promotion_rate', ascending=True)
colors = ['#d62728' if x < 10 else '#ff7f0e' if x < 20 else '#2ca02c' for x in promo_plot['promotion_rate']]
ax2.barh(promo_plot.index, promo_plot['promotion_rate'], color=colors)
ax2.set_xlabel('Promotion Rate (%)', fontsize=11)
ax2.set_ylabel('Job Level', fontsize=11)
ax2.set_title('Promotion Rate by Job Level', fontsize=12, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

# Add rate labels
for i, (level, row) in enumerate(promo_plot.iterrows()):
    ax2.text(row['promotion_rate'] + 0.5, i, f"{row['promotion_rate']:.1f}%", 
             va='center', fontsize=9)

# Plot 3: Distribution by group level
ax3 = axes[1, 0]
group_dist = level_distribution.groupby('group_job_level')['count'].sum()
group_labels = {0: 'Support', 1: 'Staff/Officer', 2: 'Management'}
group_names = [group_labels[i] for i in group_dist.index]
colors_pie = ['#ff9999', '#66b3ff', '#99ff99']
wedges, texts, autotexts = ax3.pie(group_dist.values, labels=group_names, autopct='%1.1f%%',
                                     colors=colors_pie, startangle=90)
ax3.set_title('Employee Distribution by Group Level', fontsize=12, fontweight='bold')

# Make percentage text bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

# Plot 4: Promotion readiness by level (if data available)
ax4 = axes[1, 1]
if 'promotion_readiness_score' in df_model.columns and 'level_name' in df_model.columns:
    readiness_by_level = df_model.groupby('level_name')['promotion_readiness_score'].mean().sort_values(ascending=True)
    ax4.barh(readiness_by_level.index, readiness_by_level.values, color='coral')
    ax4.set_xlabel('Average Promotion Readiness Score', fontsize=11)
    ax4.set_ylabel('Job Level', fontsize=11)
    ax4.set_title('Average Promotion Readiness by Job Level', fontsize=12, fontweight='bold')
    ax4.grid(axis='x', alpha=0.3)
    
    # Add score labels
    for i, (level, score) in enumerate(readiness_by_level.items()):
        ax4.text(score + 0.5, i, f"{score:.1f}", va='center', fontsize=9)
else:
    ax4.text(0.5, 0.5, 'Promotion Readiness Score\nNot Available\n\n(Run feature engineering first)', 
             ha='center', va='center', fontsize=12, transform=ax4.transAxes)
    ax4.set_xticks([])
    ax4.set_yticks([])

plt.tight_layout()
viz_file = RESULTS_DIR / "job_level_analysis.png"
plt.savefig(viz_file, dpi=300, bbox_inches='tight')
print(f"✓ Visualization saved to: {viz_file}")

# ============================================================================
# 8. SUMMARY REPORT
# ============================================================================
print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80)

print(f"\n📊 Dataset Overview:")
print(f"   • Total Employees: {len(df_employees):,}")
print(f"   • Job Levels: {len(df_job_levels)}")
print(f"   • Job Positions: {len(df_job_positions):,}")

print(f"\n📈 Job Level Distribution:")
print(f"   • Support Level (Group 0): {level_distribution[level_distribution['group_job_level']==0]['count'].sum():,} employees")
print(f"   • Staff Level (Group 1): {level_distribution[level_distribution['group_job_level']==1]['count'].sum():,} employees")
print(f"   • Management Level (Group 2): {level_distribution[level_distribution['group_job_level']==2]['count'].sum():,} employees")

print(f"\n🎯 Promotion Statistics:")
total_promoted = promotion_stats['promotion_count'].gt(0).sum()
overall_promo_rate = (total_promoted / len(promotion_stats) * 100)
print(f"   • Total Promoted: {total_promoted:,} employees")
print(f"   • Overall Promotion Rate: {overall_promo_rate:.2f}%")
print(f"   • Highest Promotion Rate: {promo_by_level['promotion_rate'].max():.2f}% ({promo_by_level['promotion_rate'].idxmax()})")
print(f"   • Lowest Promotion Rate: {promo_by_level['promotion_rate'].min():.2f}% ({promo_by_level['promotion_rate'].idxmin()})")

print(f"\n✅ Recommendations for ML Model:")
print(f"   1. Use job level as categorical feature (12 levels)")
print(f"   2. Use group_job_level as ordinal feature (0-2)")
print(f"   3. Create promotion_readiness_score as target proxy")
print(f"   4. Consider level-specific models for better accuracy")
print(f"   5. Use promotion paths for succession planning rules")

print("\n" + "="*80)
print("Analysis complete! Check results folder for visualizations.")
print("="*80)
