"""
Succession Planning System with Job Level Analysis
===================================================

Tujuan:
1. Identifikasi successor candidates untuk setiap posisi
2. Talent pool mapping per job level
3. Career path recommendations
4. Succession readiness dashboard

Author: Denis Ulaeman
Date: Dec 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import joblib
import warnings
warnings.filterwarnings('ignore')

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
FINAL_DIR = DATA_DIR / "final"
RESULTS_DIR = BASE_DIR / "results" / "succession_planning"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("SUCCESSION PLANNING SYSTEM")
print("="*80)

# ============================================================================
# 1. LOAD DATA & MODEL
# ============================================================================
print("\n[1] Loading data and trained model...")

# Load datasets
df_employees = pd.read_csv(RAW_DIR / "01_employee_master.csv")
df_job_levels = pd.read_csv(RAW_DIR / "ref_job_levels.csv")
df_job_positions = pd.read_csv(RAW_DIR / "ref_job_positions.csv")

try:
    df_integrated = pd.read_csv(FINAL_DIR / "integrated_full_dataset_with_job_level.csv")
    print(f"✓ Loaded enhanced dataset: {len(df_integrated)} records")
except FileNotFoundError:
    df_integrated = pd.read_csv(FINAL_DIR / "integrated_full_dataset.csv")
    print(f"✓ Loaded base dataset: {len(df_integrated)} records")

# Load trained model
model_dir = BASE_DIR / "results" / "promotion_prediction"
try:
    # Try to find the best model
    model_files = list(model_dir.glob("best_model_*.pkl"))
    if model_files:
        model = joblib.load(model_files[0])
        scaler = joblib.load(model_dir / "scaler.pkl")
        print(f"✓ Loaded trained model: {model_files[0].name}")
    else:
        model = None
        scaler = None
        print("⚠️  No trained model found. Run 02_promotion_prediction_model.py first")
except Exception as e:
    model = None
    scaler = None
    print(f"⚠️  Could not load model: {e}")

# ============================================================================
# 2. DEFINE SUCCESSION PLANNING FRAMEWORK
# ============================================================================
print("\n[2] Setting up succession planning framework...")

# Career progression paths
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

# Readiness criteria
READINESS_CRITERIA = {
    'Ready Now': {
        'performance_min': 85,
        'leadership_min': 80,
        'tenure_min': 2,
        'behavior_min': 85
    },
    'Ready 1-2 Years': {
        'performance_min': 75,
        'leadership_min': 70,
        'tenure_min': 1,
        'behavior_min': 75
    },
    'Ready 3+ Years': {
        'performance_min': 65,
        'leadership_min': 60,
        'tenure_min': 0,
        'behavior_min': 65
    }
}

print("✓ Career progression paths defined")
print("✓ Readiness criteria established")

# ============================================================================
# 3. CALCULATE SUCCESSION READINESS
# ============================================================================
print("\n[3] Calculating succession readiness scores...")

# Merge employee data with integrated dataset
df_succession = df_integrated.copy()

# Calculate composite succession readiness score
if all(col in df_succession.columns for col in ['performance_score', 'leadership_potential', 'behavior_avg']):
    df_succession['succession_readiness'] = (
        df_succession['performance_score'] * 0.35 +
        df_succession['leadership_potential'] * 0.35 +
        df_succession['behavior_avg'] * 0.20 +
        df_succession['holistic_score'] * 0.10
    )
    print("✓ Succession readiness score calculated")
else:
    print("⚠️  Missing required columns for readiness calculation")
    df_succession['succession_readiness'] = 0

# Categorize readiness level
def categorize_readiness(row):
    if (row['performance_score'] >= READINESS_CRITERIA['Ready Now']['performance_min'] and
        row['leadership_potential'] >= READINESS_CRITERIA['Ready Now']['leadership_min'] and
        row['tenure_years'] >= READINESS_CRITERIA['Ready Now']['tenure_min'] and
        row['behavior_avg'] >= READINESS_CRITERIA['Ready Now']['behavior_min']):
        return 'Ready Now'
    elif (row['performance_score'] >= READINESS_CRITERIA['Ready 1-2 Years']['performance_min'] and
          row['leadership_potential'] >= READINESS_CRITERIA['Ready 1-2 Years']['leadership_min'] and
          row['tenure_years'] >= READINESS_CRITERIA['Ready 1-2 Years']['tenure_min'] and
          row['behavior_avg'] >= READINESS_CRITERIA['Ready 1-2 Years']['behavior_min']):
        return 'Ready 1-2 Years'
    elif (row['performance_score'] >= READINESS_CRITERIA['Ready 3+ Years']['performance_min'] and
          row['leadership_potential'] >= READINESS_CRITERIA['Ready 3+ Years']['leadership_min'] and
          row['behavior_avg'] >= READINESS_CRITERIA['Ready 3+ Years']['behavior_min']):
        return 'Ready 3+ Years'
    else:
        return 'Not Ready'

if all(col in df_succession.columns for col in ['performance_score', 'leadership_potential', 'tenure_years', 'behavior_avg']):
    df_succession['readiness_category'] = df_succession.apply(categorize_readiness, axis=1)
    print("✓ Readiness categories assigned")
    
    print("\nReadiness Distribution:")
    print(df_succession['readiness_category'].value_counts())
else:
    df_succession['readiness_category'] = 'Unknown'

# ============================================================================
# 4. IDENTIFY SUCCESSOR CANDIDATES
# ============================================================================
print("\n[4] Identifying successor candidates...")

# For each job level, identify top candidates for promotion
successor_candidates = []

if 'level_name' in df_succession.columns:
    for current_level in df_succession['level_name'].unique():
        if pd.isna(current_level) or current_level not in PROMOTION_PATHS:
            continue
        
        # Get employees at this level
        level_employees = df_succession[df_succession['level_name'] == current_level].copy()
        
        if len(level_employees) == 0:
            continue
        
        # Get potential next levels
        next_levels = PROMOTION_PATHS.get(current_level, [])
        
        if not next_levels:
            continue
        
        # Rank by succession readiness
        level_employees = level_employees.sort_values('succession_readiness', ascending=False)
        
        # Top 3 candidates per level
        top_candidates = level_employees.head(min(3, len(level_employees)))
        
        for _, candidate in top_candidates.iterrows():
            successor_candidates.append({
                'employee_id': candidate.get('employee_id_hash', 'Unknown'),
                'name': candidate.get('name', 'Unknown'),
                'current_level': current_level,
                'target_levels': ', '.join(next_levels),
                'succession_readiness': candidate['succession_readiness'],
                'readiness_category': candidate['readiness_category'],
                'performance_score': candidate['performance_score'],
                'leadership_potential': candidate['leadership_potential'],
                'tenure_years': candidate['tenure_years']
            })
    
    df_successors = pd.DataFrame(successor_candidates)
    
    if len(df_successors) > 0:
        print(f"✓ Identified {len(df_successors)} successor candidates")
        
        # Save successor candidates
        df_successors.to_csv(RESULTS_DIR / "successor_candidates.csv", index=False)
        print(f"✓ Saved to: {RESULTS_DIR / 'successor_candidates.csv'}")
    else:
        print("⚠️  No successor candidates identified")
        df_successors = pd.DataFrame()
else:
    print("⚠️  level_name column not found")
    df_successors = pd.DataFrame()

# ============================================================================
# 5. TALENT POOL ANALYSIS
# ============================================================================
print("\n[5] Analyzing talent pools by job level...")

if 'level_name' in df_succession.columns:
    talent_pool = df_succession.groupby('level_name').agg({
        'employee_id_hash': 'count',
        'succession_readiness': ['mean', 'std'],
        'performance_score': 'mean',
        'leadership_potential': 'mean'
    }).round(2)
    
    talent_pool.columns = ['_'.join(col).strip('_') for col in talent_pool.columns]
    talent_pool = talent_pool.rename(columns={
        'employee_id_hash_count': 'total_employees',
        'succession_readiness_mean': 'avg_readiness',
        'succession_readiness_std': 'std_readiness',
        'performance_score_mean': 'avg_performance',
        'leadership_potential_mean': 'avg_leadership'
    })
    
    talent_pool = talent_pool.sort_values('avg_readiness', ascending=False)
    
    print("\nTalent Pool Summary by Job Level:")
    print("-" * 100)
    print(talent_pool.to_string())
    
    # Save talent pool analysis
    talent_pool.to_csv(RESULTS_DIR / "talent_pool_by_level.csv")
    print(f"\n✓ Saved to: {RESULTS_DIR / 'talent_pool_by_level.csv'}")
else:
    talent_pool = pd.DataFrame()

# ============================================================================
# 6. SUCCESSION GAP ANALYSIS
# ============================================================================
print("\n[6] Performing succession gap analysis...")

if 'level_name' in df_succession.columns and 'readiness_category' in df_succession.columns:
    # Count ready successors per level
    succession_gaps = df_succession.groupby(['level_name', 'readiness_category']).size().unstack(fill_value=0)
    
    # Calculate gap (positions with no ready successors)
    if 'Ready Now' in succession_gaps.columns:
        succession_gaps['has_ready_successor'] = succession_gaps['Ready Now'] > 0
        succession_gaps['succession_risk'] = succession_gaps['has_ready_successor'].map({True: 'Low', False: 'High'})
    else:
        succession_gaps['succession_risk'] = 'High'
    
    print("\nSuccession Gap Analysis:")
    print("-" * 80)
    print(succession_gaps.to_string())
    
    # Save gap analysis
    succession_gaps.to_csv(RESULTS_DIR / "succession_gaps.csv")
    print(f"\n✓ Saved to: {RESULTS_DIR / 'succession_gaps.csv'}")
    
    # Identify critical gaps
    if 'Ready Now' in succession_gaps.columns:
        critical_gaps = succession_gaps[succession_gaps['Ready Now'] == 0]
        if len(critical_gaps) > 0:
            print(f"\n⚠️  CRITICAL: {len(critical_gaps)} job levels have NO ready successors:")
            for level in critical_gaps.index:
                print(f"   - {level}")
else:
    succession_gaps = pd.DataFrame()

# ============================================================================
# 7. VISUALIZATIONS
# ============================================================================
print("\n[7] Creating visualizations...")

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Plot 1: Succession Readiness Distribution
if 'readiness_category' in df_succession.columns:
    ax1 = fig.add_subplot(gs[0, :2])
    readiness_counts = df_succession['readiness_category'].value_counts()
    colors_readiness = {'Ready Now': '#2ecc71', 'Ready 1-2 Years': '#f39c12', 
                       'Ready 3+ Years': '#e74c3c', 'Not Ready': '#95a5a6'}
    colors = [colors_readiness.get(cat, '#95a5a6') for cat in readiness_counts.index]
    ax1.bar(range(len(readiness_counts)), readiness_counts.values, color=colors, alpha=0.8)
    ax1.set_xticks(range(len(readiness_counts)))
    ax1.set_xticklabels(readiness_counts.index, rotation=45, ha='right')
    ax1.set_ylabel('Number of Employees', fontsize=11)
    ax1.set_title('Succession Readiness Distribution', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(readiness_counts.values):
        ax1.text(i, v + 5, str(v), ha='center', va='bottom', fontweight='bold')

# Plot 2: Readiness by Job Level (Heatmap)
if not succession_gaps.empty and 'readiness_category' in df_succession.columns:
    ax2 = fig.add_subplot(gs[0, 2])
    # Select only readiness columns
    readiness_cols = [col for col in succession_gaps.columns if col in ['Ready Now', 'Ready 1-2 Years', 'Ready 3+ Years', 'Not Ready']]
    if readiness_cols:
        heatmap_data = succession_gaps[readiness_cols].fillna(0)
        sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='RdYlGn', cbar_kws={'label': 'Count'}, ax=ax2)
        ax2.set_title('Readiness by Job Level', fontsize=12, fontweight='bold')
        ax2.set_xlabel('')
        ax2.set_ylabel('Job Level', fontsize=10)

# Plot 3: Top Successor Candidates
if not df_successors.empty:
    ax3 = fig.add_subplot(gs[1, :])
    top_successors = df_successors.nlargest(15, 'succession_readiness')
    y_pos = np.arange(len(top_successors))
    colors_bar = ['#2ecc71' if cat == 'Ready Now' else '#f39c12' if cat == 'Ready 1-2 Years' else '#e74c3c' 
                  for cat in top_successors['readiness_category']]
    ax3.barh(y_pos, top_successors['succession_readiness'], color=colors_bar, alpha=0.8)
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels([f"{row['name'][:20]}\n({row['current_level'][:15]})" 
                         for _, row in top_successors.iterrows()], fontsize=9)
    ax3.set_xlabel('Succession Readiness Score', fontsize=11)
    ax3.set_title('Top 15 Successor Candidates', fontsize=13, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3)
    ax3.invert_yaxis()
    
    # Add score labels
    for i, score in enumerate(top_successors['succession_readiness']):
        ax3.text(score + 0.5, i, f'{score:.1f}', va='center', fontsize=9)

# Plot 4: Talent Pool Strength by Level
if not talent_pool.empty:
    ax4 = fig.add_subplot(gs[2, 0])
    talent_sorted = talent_pool.sort_values('avg_readiness', ascending=True)
    ax4.barh(range(len(talent_sorted)), talent_sorted['avg_readiness'], color='steelblue', alpha=0.7)
    ax4.set_yticks(range(len(talent_sorted)))
    ax4.set_yticklabels(talent_sorted.index, fontsize=9)
    ax4.set_xlabel('Avg Readiness Score', fontsize=11)
    ax4.set_title('Talent Pool Strength', fontsize=12, fontweight='bold')
    ax4.grid(axis='x', alpha=0.3)

# Plot 5: Performance vs Leadership (Scatter)
if all(col in df_succession.columns for col in ['performance_score', 'leadership_potential', 'readiness_category']):
    ax5 = fig.add_subplot(gs[2, 1])
    for category in df_succession['readiness_category'].unique():
        subset = df_succession[df_succession['readiness_category'] == category]
        color = colors_readiness.get(category, '#95a5a6')
        ax5.scatter(subset['performance_score'], subset['leadership_potential'], 
                   label=category, alpha=0.6, s=50, color=color)
    ax5.set_xlabel('Performance Score', fontsize=11)
    ax5.set_ylabel('Leadership Potential', fontsize=11)
    ax5.set_title('Performance vs Leadership', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(alpha=0.3)

# Plot 6: Succession Risk by Level
if not succession_gaps.empty and 'succession_risk' in succession_gaps.columns:
    ax6 = fig.add_subplot(gs[2, 2])
    risk_counts = succession_gaps['succession_risk'].value_counts()
    colors_risk = {'Low': '#2ecc71', 'High': '#e74c3c'}
    colors_pie = [colors_risk.get(risk, '#95a5a6') for risk in risk_counts.index]
    wedges, texts, autotexts = ax6.pie(risk_counts.values, labels=risk_counts.index, 
                                        autopct='%1.1f%%', colors=colors_pie, startangle=90)
    ax6.set_title('Succession Risk Distribution', fontsize=12, fontweight='bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

plt.suptitle('Succession Planning Dashboard', fontsize=16, fontweight='bold', y=0.995)

viz_file = RESULTS_DIR / "succession_planning_dashboard.png"
plt.savefig(viz_file, dpi=300, bbox_inches='tight')
print(f"✓ Dashboard saved to: {viz_file}")

# ============================================================================
# 8. GENERATE SUCCESSION PLANNING REPORT
# ============================================================================
print("\n[8] Generating succession planning report...")

report_lines = []
report_lines.append("="*80)
report_lines.append("SUCCESSION PLANNING REPORT")
report_lines.append("="*80)
report_lines.append("")

# Executive Summary
report_lines.append("EXECUTIVE SUMMARY")
report_lines.append("-"*80)
report_lines.append(f"Total Employees Analyzed: {len(df_succession):,}")
if 'readiness_category' in df_succession.columns:
    ready_now = len(df_succession[df_succession['readiness_category'] == 'Ready Now'])
    ready_soon = len(df_succession[df_succession['readiness_category'] == 'Ready 1-2 Years'])
    report_lines.append(f"Ready Now: {ready_now:,} ({ready_now/len(df_succession)*100:.1f}%)")
    report_lines.append(f"Ready 1-2 Years: {ready_soon:,} ({ready_soon/len(df_succession)*100:.1f}%)")
report_lines.append("")

# Critical Gaps
if not succession_gaps.empty and 'Ready Now' in succession_gaps.columns:
    critical_gaps = succession_gaps[succession_gaps['Ready Now'] == 0]
    report_lines.append("CRITICAL SUCCESSION GAPS")
    report_lines.append("-"*80)
    if len(critical_gaps) > 0:
        report_lines.append(f"⚠️  {len(critical_gaps)} job levels have NO ready successors:")
        for level in critical_gaps.index:
            report_lines.append(f"   • {level}")
    else:
        report_lines.append("✓ All job levels have at least one ready successor")
    report_lines.append("")

# Top Successors
if not df_successors.empty:
    report_lines.append("TOP SUCCESSOR CANDIDATES")
    report_lines.append("-"*80)
    top_10 = df_successors.nlargest(10, 'succession_readiness')
    for idx, row in top_10.iterrows():
        report_lines.append(f"{idx+1}. {row['name']}")
        report_lines.append(f"   Current: {row['current_level']} → Target: {row['target_levels']}")
        report_lines.append(f"   Readiness: {row['succession_readiness']:.1f} ({row['readiness_category']})")
        report_lines.append("")

# Recommendations
report_lines.append("RECOMMENDATIONS")
report_lines.append("-"*80)
report_lines.append("1. Focus development programs on 'Ready 1-2 Years' candidates")
report_lines.append("2. Create retention plans for 'Ready Now' high-potential employees")
report_lines.append("3. Address critical succession gaps through external hiring or accelerated development")
report_lines.append("4. Implement mentoring programs pairing senior leaders with successors")
report_lines.append("5. Review and update succession plans quarterly")
report_lines.append("")

report_lines.append("="*80)

# Save report
report_file = RESULTS_DIR / "succession_planning_report.txt"
with open(report_file, 'w') as f:
    f.write('\n'.join(report_lines))

print(f"✓ Report saved to: {report_file}")

# Print report to console
print("\n" + '\n'.join(report_lines))

print("\n" + "="*80)
print("Succession planning analysis complete!")
print("="*80)
