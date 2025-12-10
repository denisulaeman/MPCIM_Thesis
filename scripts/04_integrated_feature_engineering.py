"""
Integrated Feature Engineering - Maksimalkan SEMUA Fitur
=========================================================

Script ini mengintegrasikan SEMUA fitur yang sudah dibuat:
1. Job Level features
2. Skills & Proficiency features
3. Knowledge Graph features
4. Performance & Behavioral features
5. Skill Gap Analysis
6. Career Path Readiness

Tujuan: Maksimalkan penggunaan semua data untuk prediksi promosi

Author: Denis Ulaeman
Date: Dec 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
FINAL_DIR = DATA_DIR / "final"
KG_DIR = DATA_DIR / "knowledge_graph"
RESULTS_DIR = BASE_DIR / "results" / "integrated_features"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("INTEGRATED FEATURE ENGINEERING")
print("Maksimalkan SEMUA Fitur untuk Prediksi Promosi")
print("="*80)

# ============================================================================
# 1. LOAD ALL DATA SOURCES
# ============================================================================
print("\n[1] Loading all data sources...")

# Core data
df_employees = pd.read_csv(RAW_DIR / "01_employee_master.csv")
df_job_levels = pd.read_csv(RAW_DIR / "ref_job_levels.csv")
df_job_positions = pd.read_csv(RAW_DIR / "ref_job_positions.csv")

# Performance data
try:
    df_integrated = pd.read_csv(FINAL_DIR / "integrated_full_dataset_with_job_level.csv")
    print(f"✓ Loaded enhanced dataset: {len(df_integrated)} records")
except FileNotFoundError:
    df_integrated = pd.read_csv(FINAL_DIR / "integrated_full_dataset.csv")
    print(f"✓ Loaded base dataset: {len(df_integrated)} records")

# Knowledge Graph data
df_skills = pd.read_csv(KG_DIR / "skills.csv")
df_employee_skills = pd.read_csv(KG_DIR / "employee_skills.csv")
df_job_skill_req = pd.read_csv(KG_DIR / "job_skill_requirements.csv")

print(f"✓ Skills: {len(df_skills)} skills")
print(f"✓ Employee Skills: {len(df_employee_skills)} records")
print(f"✓ Job Skill Requirements: {len(df_job_skill_req)} requirements")

# ============================================================================
# 2. SKILL-BASED FEATURES
# ============================================================================
print("\n[2] Creating skill-based features...")

# 2.1 Employee Skill Statistics
employee_skill_stats = df_employee_skills.groupby('employee_id').agg({
    'skill_id': 'count',
    'proficiency': ['mean', 'max', 'min', 'std']
}).reset_index()

employee_skill_stats.columns = ['employee_id', 'skill_count', 'skill_avg_proficiency', 
                                 'skill_max_proficiency', 'skill_min_proficiency', 'skill_std_proficiency']

# Fill NaN std with 0 (for employees with only 1 skill)
employee_skill_stats['skill_std_proficiency'] = employee_skill_stats['skill_std_proficiency'].fillna(0)

print(f"✓ Created skill statistics for {len(employee_skill_stats)} employees")

# 2.2 Skill Category Breakdown
# Merge with skill details
df_emp_skills_detail = df_employee_skills.merge(df_skills, on='skill_id', how='left')

# Count skills by category per employee
skill_by_category = df_emp_skills_detail.groupby(['employee_id', 'category']).agg({
    'skill_id': 'count',
    'proficiency': 'mean'
}).reset_index()

# Pivot to get category counts as columns
skill_category_pivot = skill_by_category.pivot_table(
    index='employee_id',
    columns='category',
    values='skill_id',
    fill_value=0
).reset_index()

# Rename columns
skill_category_pivot.columns = ['employee_id'] + [f'skill_count_{col.lower().replace(" ", "_")}' 
                                                    for col in skill_category_pivot.columns[1:]]

print(f"✓ Created skill category breakdown")

# 2.3 High-Value Skills (importance >= 4)
high_value_skills = df_skills[df_skills['importance'] >= 4]['skill_id'].tolist()

employee_high_value_skills = df_employee_skills[
    df_employee_skills['skill_id'].isin(high_value_skills)
].groupby('employee_id').agg({
    'skill_id': 'count',
    'proficiency': 'mean'
}).reset_index()

employee_high_value_skills.columns = ['employee_id', 'high_value_skill_count', 'high_value_skill_avg_proficiency']

print(f"✓ Identified high-value skills (importance ≥4): {len(high_value_skills)} skills")

# ============================================================================
# 3. SKILL GAP ANALYSIS (Job Level Requirements)
# ============================================================================
print("\n[3] Performing skill gap analysis...")

# Map job_id to job_level_id
# Assuming job_id format is L001, L002, etc. corresponding to job_level_id
df_job_skill_req['job_level_id'] = df_job_skill_req['job_id'].str.replace('L', '').astype(int)

# For each employee, calculate skill gap vs their current job level requirements
skill_gaps = []

for emp_id in df_integrated['employee_id_hash'].unique():
    # Get employee's job level
    emp_data = df_integrated[df_integrated['employee_id_hash'] == emp_id].iloc[0]
    
    if 'job_level_id' not in emp_data or pd.isna(emp_data.get('job_level_id')):
        continue
    
    job_level_id = int(emp_data['job_level_id'])
    
    # Get required skills for this job level
    required_skills = df_job_skill_req[df_job_skill_req['job_level_id'] == job_level_id]
    
    if len(required_skills) == 0:
        continue
    
    # Get employee's skills
    emp_skills = df_employee_skills[df_employee_skills['employee_id'] == emp_id]
    
    # Calculate gaps
    total_required = len(required_skills)
    skills_met = 0
    skills_exceeded = 0
    avg_gap = 0
    
    for _, req in required_skills.iterrows():
        emp_skill = emp_skills[emp_skills['skill_id'] == req['skill_id']]
        
        if len(emp_skill) > 0:
            emp_proficiency = emp_skill.iloc[0]['proficiency']
            required_proficiency = req['min_proficiency']
            
            if emp_proficiency >= required_proficiency:
                skills_met += 1
                if emp_proficiency > required_proficiency:
                    skills_exceeded += 1
            
            avg_gap += (emp_proficiency - required_proficiency)
        else:
            # Skill not possessed
            avg_gap -= req['min_proficiency']
    
    skill_gaps.append({
        'employee_id': emp_id,
        'required_skills_count': total_required,
        'skills_met': skills_met,
        'skills_exceeded': skills_exceeded,
        'skill_gap_ratio': skills_met / total_required if total_required > 0 else 0,
        'skill_exceed_ratio': skills_exceeded / total_required if total_required > 0 else 0,
        'avg_skill_gap': avg_gap / total_required if total_required > 0 else 0
    })

df_skill_gaps = pd.DataFrame(skill_gaps)
print(f"✓ Calculated skill gaps for {len(df_skill_gaps)} employees")

# ============================================================================
# 4. NEXT LEVEL READINESS (Career Path)
# ============================================================================
print("\n[4] Calculating next level readiness...")

# Define promotion paths (from previous script)
PROMOTION_PATHS = {
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
    'Komisaris': [],
    'Temporary Position (PJS)': []
}

# Map level names to IDs
level_name_to_id = dict(zip(df_job_levels['level_name'], df_job_levels['job_level_id']))

next_level_readiness = []

for emp_id in df_integrated['employee_id_hash'].unique():
    emp_data = df_integrated[df_integrated['employee_id_hash'] == emp_id].iloc[0]
    
    if 'level_name' not in emp_data or pd.isna(emp_data.get('level_name')):
        continue
    
    current_level = emp_data['level_name']
    next_levels = PROMOTION_PATHS.get(current_level, [])
    
    if not next_levels:
        # Top level or no path
        next_level_readiness.append({
            'employee_id': emp_id,
            'has_next_level': False,
            'next_level_skill_readiness': 0,
            'next_level_skill_gap': 0
        })
        continue
    
    # Check readiness for first next level
    next_level = next_levels[0]
    next_level_id = level_name_to_id.get(next_level)
    
    if next_level_id is None:
        continue
    
    # Get required skills for next level
    next_level_skills = df_job_skill_req[df_job_skill_req['job_level_id'] == next_level_id]
    
    if len(next_level_skills) == 0:
        continue
    
    # Get employee's skills
    emp_skills = df_employee_skills[df_employee_skills['employee_id'] == emp_id]
    
    # Calculate readiness
    total_required = len(next_level_skills)
    skills_ready = 0
    total_gap = 0
    
    for _, req in next_level_skills.iterrows():
        emp_skill = emp_skills[emp_skills['skill_id'] == req['skill_id']]
        
        if len(emp_skill) > 0:
            emp_proficiency = emp_skill.iloc[0]['proficiency']
            required_proficiency = req['min_proficiency']
            
            if emp_proficiency >= required_proficiency:
                skills_ready += 1
            
            total_gap += max(0, required_proficiency - emp_proficiency)
        else:
            total_gap += req['min_proficiency']
    
    next_level_readiness.append({
        'employee_id': emp_id,
        'has_next_level': True,
        'next_level_name': next_level,
        'next_level_skill_readiness': skills_ready / total_required if total_required > 0 else 0,
        'next_level_skill_gap': total_gap / total_required if total_required > 0 else 0
    })

df_next_level_readiness = pd.DataFrame(next_level_readiness)
print(f"✓ Calculated next level readiness for {len(df_next_level_readiness)} employees")

# ============================================================================
# 5. INTEGRATE ALL FEATURES
# ============================================================================
print("\n[5] Integrating all features...")

# Start with base dataset
df_final = df_integrated.copy()

# Merge skill statistics
df_final = df_final.merge(employee_skill_stats, left_on='employee_id_hash', right_on='employee_id', how='left')

# Merge skill category breakdown
df_final = df_final.merge(skill_category_pivot, left_on='employee_id_hash', right_on='employee_id', how='left')

# Merge high-value skills
df_final = df_final.merge(employee_high_value_skills, left_on='employee_id_hash', right_on='employee_id', how='left')

# Merge skill gaps
df_final = df_final.merge(df_skill_gaps, left_on='employee_id_hash', right_on='employee_id', how='left')

# Merge next level readiness
df_final = df_final.merge(df_next_level_readiness, left_on='employee_id_hash', right_on='employee_id', how='left')

# Drop duplicate employee_id columns
cols_to_drop = [col for col in df_final.columns if col.startswith('employee_id') and col != 'employee_id_hash']
df_final = df_final.drop(columns=cols_to_drop)

# Fill NaN values for skill features with 0
skill_feature_cols = [col for col in df_final.columns if 'skill' in col.lower()]
df_final[skill_feature_cols] = df_final[skill_feature_cols].fillna(0)

print(f"✓ Integrated dataset: {len(df_final)} records, {len(df_final.columns)} features")

# ============================================================================
# 6. CREATE ADVANCED COMPOSITE FEATURES
# ============================================================================
print("\n[6] Creating advanced composite features...")

# 6.1 Skill-Performance Alignment
if 'skill_avg_proficiency' in df_final.columns and 'performance_score' in df_final.columns:
    df_final['skill_performance_alignment'] = (
        df_final['skill_avg_proficiency'] / 5 * 100 - df_final['performance_score']
    ).abs()
    print("✓ Created skill_performance_alignment")

# 6.2 Promotion Readiness Score (Enhanced with skills)
if all(col in df_final.columns for col in ['performance_score', 'leadership_potential', 'behavior_avg', 
                                             'skill_gap_ratio', 'next_level_skill_readiness']):
    df_final['promotion_readiness_enhanced'] = (
        df_final['performance_score'] * 0.25 +
        df_final['leadership_potential'] * 0.25 +
        df_final['behavior_avg'] * 0.15 +
        df_final['holistic_score'] * 0.10 +
        df_final['skill_gap_ratio'] * 100 * 0.15 +
        df_final['next_level_skill_readiness'] * 100 * 0.10
    )
    print("✓ Created promotion_readiness_enhanced (includes skill factors)")

# 6.3 Skill Diversity Index (Shannon Entropy)
if 'skill_count' in df_final.columns:
    # Normalize skill count
    max_skills = df_final['skill_count'].max()
    df_final['skill_diversity_index'] = df_final['skill_count'] / max_skills if max_skills > 0 else 0
    print("✓ Created skill_diversity_index")

# 6.4 Technical Competency Score
technical_cols = [col for col in df_final.columns if 'skill_count_technical' in col]
if technical_cols:
    df_final['technical_competency_score'] = df_final[technical_cols].sum(axis=1)
    print("✓ Created technical_competency_score")

# 6.5 Leadership Competency Score
leadership_cols = [col for col in df_final.columns if 'skill_count_leadership' in col]
if leadership_cols:
    df_final['leadership_competency_score'] = df_final[leadership_cols].sum(axis=1)
    print("✓ Created leadership_competency_score")

# 6.6 Career Progression Potential
if all(col in df_final.columns for col in ['tenure_years', 'skill_gap_ratio', 'performance_score']):
    df_final['career_progression_potential'] = (
        (df_final['performance_score'] / 100) * 0.4 +
        df_final['skill_gap_ratio'] * 0.3 +
        (1 / (1 + np.exp(-0.2 * (df_final['tenure_years'] - 3)))) * 0.3  # Sigmoid for tenure
    )
    print("✓ Created career_progression_potential")

# ============================================================================
# 7. FEATURE SUMMARY & STATISTICS
# ============================================================================
print("\n[7] Generating feature summary...")

# List all new features created
new_features = [
    'skill_count', 'skill_avg_proficiency', 'skill_max_proficiency', 'skill_min_proficiency',
    'skill_std_proficiency', 'high_value_skill_count', 'high_value_skill_avg_proficiency',
    'required_skills_count', 'skills_met', 'skills_exceeded', 'skill_gap_ratio',
    'skill_exceed_ratio', 'avg_skill_gap', 'next_level_skill_readiness', 'next_level_skill_gap',
    'skill_performance_alignment', 'promotion_readiness_enhanced', 'skill_diversity_index',
    'technical_competency_score', 'leadership_competency_score', 'career_progression_potential'
]

# Filter to only existing features
existing_new_features = [f for f in new_features if f in df_final.columns]

print(f"\n{'='*80}")
print(f"FEATURE SUMMARY")
print(f"{'='*80}")
print(f"\nTotal Features: {len(df_final.columns)}")
print(f"New Features Created: {len(existing_new_features)}")
print(f"\nNew Feature List:")
for i, feature in enumerate(existing_new_features, 1):
    print(f"  {i:2d}. {feature}")

# Feature statistics
feature_stats = df_final[existing_new_features].describe().T
feature_stats['missing'] = df_final[existing_new_features].isnull().sum()
feature_stats['missing_pct'] = (feature_stats['missing'] / len(df_final) * 100).round(2)

print(f"\n{'='*80}")
print(f"FEATURE STATISTICS")
print(f"{'='*80}")
print(feature_stats[['mean', 'std', 'min', 'max', 'missing_pct']].to_string())

# Save feature statistics
feature_stats.to_csv(RESULTS_DIR / "feature_statistics.csv")
print(f"\n✓ Feature statistics saved to: {RESULTS_DIR / 'feature_statistics.csv'}")

# ============================================================================
# 8. SAVE INTEGRATED DATASET
# ============================================================================
print("\n[8] Saving integrated dataset...")

output_file = FINAL_DIR / "integrated_full_dataset_with_all_features.csv"
df_final.to_csv(output_file, index=False)
print(f"✓ Saved to: {output_file}")
print(f"  Records: {len(df_final):,}")
print(f"  Features: {len(df_final.columns)}")

# Save feature list
feature_list = pd.DataFrame({
    'feature_name': df_final.columns,
    'data_type': df_final.dtypes.values,
    'non_null_count': df_final.count().values,
    'null_count': df_final.isnull().sum().values
})
feature_list.to_csv(RESULTS_DIR / "feature_list.csv", index=False)
print(f"✓ Feature list saved to: {RESULTS_DIR / 'feature_list.csv'}")

# ============================================================================
# 9. VISUALIZATIONS
# ============================================================================
print("\n[9] Creating visualizations...")

fig = plt.figure(figsize=(18, 14))
gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)

# Plot 1: Skill Count Distribution
ax1 = fig.add_subplot(gs[0, 0])
if 'skill_count' in df_final.columns:
    ax1.hist(df_final['skill_count'].dropna(), bins=30, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Number of Skills', fontsize=10)
    ax1.set_ylabel('Frequency', fontsize=10)
    ax1.set_title('Skill Count Distribution', fontsize=11, fontweight='bold')
    ax1.axvline(df_final['skill_count'].mean(), color='red', linestyle='--', 
                label=f'Mean: {df_final["skill_count"].mean():.1f}')
    ax1.legend()
    ax1.grid(alpha=0.3)

# Plot 2: Skill Gap Ratio Distribution
ax2 = fig.add_subplot(gs[0, 1])
if 'skill_gap_ratio' in df_final.columns:
    ax2.hist(df_final['skill_gap_ratio'].dropna(), bins=30, color='coral', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Skill Gap Ratio', fontsize=10)
    ax2.set_ylabel('Frequency', fontsize=10)
    ax2.set_title('Skill Gap Ratio Distribution', fontsize=11, fontweight='bold')
    ax2.axvline(df_final['skill_gap_ratio'].mean(), color='red', linestyle='--',
                label=f'Mean: {df_final["skill_gap_ratio"].mean():.2f}')
    ax2.legend()
    ax2.grid(alpha=0.3)

# Plot 3: Next Level Readiness
ax3 = fig.add_subplot(gs[0, 2])
if 'next_level_skill_readiness' in df_final.columns:
    ax3.hist(df_final['next_level_skill_readiness'].dropna(), bins=30, color='green', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Next Level Skill Readiness', fontsize=10)
    ax3.set_ylabel('Frequency', fontsize=10)
    ax3.set_title('Next Level Skill Readiness', fontsize=11, fontweight='bold')
    ax3.axvline(df_final['next_level_skill_readiness'].mean(), color='red', linestyle='--',
                label=f'Mean: {df_final["next_level_skill_readiness"].mean():.2f}')
    ax3.legend()
    ax3.grid(alpha=0.3)

# Plot 4: Skill Proficiency vs Performance
ax4 = fig.add_subplot(gs[1, 0])
if 'skill_avg_proficiency' in df_final.columns and 'performance_score' in df_final.columns:
    scatter = ax4.scatter(df_final['skill_avg_proficiency'], df_final['performance_score'],
                         alpha=0.5, s=30, c=df_final.get('has_promotion', 0), cmap='RdYlGn')
    ax4.set_xlabel('Average Skill Proficiency', fontsize=10)
    ax4.set_ylabel('Performance Score', fontsize=10)
    ax4.set_title('Skill Proficiency vs Performance', fontsize=11, fontweight='bold')
    ax4.grid(alpha=0.3)
    plt.colorbar(scatter, ax=ax4, label='Has Promotion')

# Plot 5: Skill Gap by Job Level
ax5 = fig.add_subplot(gs[1, 1])
if 'skill_gap_ratio' in df_final.columns and 'level_name' in df_final.columns:
    level_skill_gap = df_final.groupby('level_name')['skill_gap_ratio'].mean().sort_values()
    ax5.barh(range(len(level_skill_gap)), level_skill_gap.values, color='purple', alpha=0.7)
    ax5.set_yticks(range(len(level_skill_gap)))
    ax5.set_yticklabels(level_skill_gap.index, fontsize=8)
    ax5.set_xlabel('Average Skill Gap Ratio', fontsize=10)
    ax5.set_title('Skill Gap by Job Level', fontsize=11, fontweight='bold')
    ax5.grid(axis='x', alpha=0.3)

# Plot 6: High-Value Skills Distribution
ax6 = fig.add_subplot(gs[1, 2])
if 'high_value_skill_count' in df_final.columns:
    ax6.hist(df_final['high_value_skill_count'].dropna(), bins=20, color='gold', alpha=0.7, edgecolor='black')
    ax6.set_xlabel('High-Value Skill Count', fontsize=10)
    ax6.set_ylabel('Frequency', fontsize=10)
    ax6.set_title('High-Value Skills Distribution', fontsize=11, fontweight='bold')
    ax6.grid(alpha=0.3)

# Plot 7: Promotion Readiness Comparison
ax7 = fig.add_subplot(gs[2, :2])
if 'promotion_readiness_score' in df_final.columns and 'promotion_readiness_enhanced' in df_final.columns:
    x = np.arange(len(df_final))
    ax7.scatter(x[::10], df_final['promotion_readiness_score'].iloc[::10], 
               alpha=0.5, s=20, label='Original', color='blue')
    ax7.scatter(x[::10], df_final['promotion_readiness_enhanced'].iloc[::10], 
               alpha=0.5, s=20, label='Enhanced (with skills)', color='red')
    ax7.set_xlabel('Employee Index (sampled)', fontsize=10)
    ax7.set_ylabel('Promotion Readiness Score', fontsize=10)
    ax7.set_title('Promotion Readiness: Original vs Enhanced', fontsize=11, fontweight='bold')
    ax7.legend()
    ax7.grid(alpha=0.3)

# Plot 8: Career Progression Potential
ax8 = fig.add_subplot(gs[2, 2])
if 'career_progression_potential' in df_final.columns:
    ax8.hist(df_final['career_progression_potential'].dropna(), bins=30, 
            color='teal', alpha=0.7, edgecolor='black')
    ax8.set_xlabel('Career Progression Potential', fontsize=10)
    ax8.set_ylabel('Frequency', fontsize=10)
    ax8.set_title('Career Progression Potential', fontsize=11, fontweight='bold')
    ax8.grid(alpha=0.3)

# Plot 9: Feature Correlation Heatmap (Top Features)
ax9 = fig.add_subplot(gs[3, :])
key_features = ['performance_score', 'leadership_potential', 'skill_count', 
                'skill_gap_ratio', 'next_level_skill_readiness', 
                'promotion_readiness_enhanced', 'career_progression_potential']
existing_key_features = [f for f in key_features if f in df_final.columns]

if len(existing_key_features) > 2:
    corr_matrix = df_final[existing_key_features].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax9)
    ax9.set_title('Feature Correlation Matrix (Key Features)', fontsize=11, fontweight='bold')

plt.suptitle('Integrated Feature Engineering - Comprehensive Analysis', 
             fontsize=14, fontweight='bold', y=0.995)

viz_file = RESULTS_DIR / "integrated_features_analysis.png"
plt.savefig(viz_file, dpi=300, bbox_inches='tight')
print(f"✓ Visualization saved to: {viz_file}")

plt.close()

# ============================================================================
# 10. SUMMARY REPORT
# ============================================================================
print("\n" + "="*80)
print("INTEGRATED FEATURE ENGINEERING - SUMMARY")
print("="*80)

print(f"\n📊 Dataset:")
print(f"   • Total Records: {len(df_final):,}")
print(f"   • Total Features: {len(df_final.columns)}")
print(f"   • New Features: {len(existing_new_features)}")

print(f"\n🎯 Feature Categories:")
print(f"   • Skill Statistics: {len([f for f in existing_new_features if 'skill' in f and 'gap' not in f and 'readiness' not in f])}")
print(f"   • Skill Gap Analysis: {len([f for f in existing_new_features if 'gap' in f])}")
print(f"   • Career Readiness: {len([f for f in existing_new_features if 'readiness' in f or 'progression' in f])}")
print(f"   • Composite Features: {len([f for f in existing_new_features if 'alignment' in f or 'diversity' in f or 'competency' in f])}")

if 'skill_count' in df_final.columns:
    print(f"\n📈 Skill Statistics:")
    print(f"   • Average Skills per Employee: {df_final['skill_count'].mean():.1f}")
    print(f"   • Max Skills: {df_final['skill_count'].max():.0f}")
    print(f"   • Employees with 0 skills: {(df_final['skill_count'] == 0).sum()}")

if 'skill_gap_ratio' in df_final.columns:
    print(f"\n🎯 Skill Gap Analysis:")
    print(f"   • Average Skill Gap Ratio: {df_final['skill_gap_ratio'].mean():.2f}")
    print(f"   • Employees meeting all requirements: {(df_final['skill_gap_ratio'] >= 1.0).sum()}")
    print(f"   • Employees with skill gaps: {(df_final['skill_gap_ratio'] < 1.0).sum()}")

if 'next_level_skill_readiness' in df_final.columns:
    print(f"\n🚀 Next Level Readiness:")
    print(f"   • Average Readiness: {df_final['next_level_skill_readiness'].mean():.2f}")
    print(f"   • Ready for promotion (≥0.8): {(df_final['next_level_skill_readiness'] >= 0.8).sum()}")
    print(f"   • Need development (<0.5): {(df_final['next_level_skill_readiness'] < 0.5).sum()}")

print(f"\n✅ Key Improvements:")
print(f"   1. Skill-based features added for granular talent assessment")
print(f"   2. Skill gap analysis enables targeted development plans")
print(f"   3. Next level readiness predicts promotion success probability")
print(f"   4. Enhanced promotion readiness score includes skill factors")
print(f"   5. Career progression potential combines multiple dimensions")

print(f"\n💡 Recommendations:")
print(f"   1. Use 'promotion_readiness_enhanced' as primary target variable")
print(f"   2. Segment employees by 'skill_gap_ratio' for development programs")
print(f"   3. Prioritize 'next_level_skill_readiness' for succession planning")
print(f"   4. Monitor 'career_progression_potential' for retention strategies")
print(f"   5. Use skill category features for role-specific predictions")

print("\n" + "="*80)
print("Feature engineering complete! All features maximized.")
print("="*80)
