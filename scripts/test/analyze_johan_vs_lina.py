"""
Analyze why Johan Budiman has higher probability than Lina Nasution
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

print('='*80)
print('ANALYZE: Johan Budiman vs Lina Nasution')
print('='*80)
print()

# Paths
repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data'
results_dir = repo_root / 'results' / 'advanced_models'

# Load model and data
model = joblib.load(results_dir / 'random_forest_model.pkl')
scaler = joblib.load(data_dir / 'processed' / 'scaler.pkl')
df = pd.read_csv(data_dir / 'final' / 'sample_dataset_100_balanced.csv')

# Feature engineering
df['combined_score'] = (df['performance_score'] + df['behavior_avg']) / 2
df['perf_beh_ratio'] = df['performance_score'] / (df['behavior_avg'] + 0.1)
df['score_difference'] = df['performance_score'] - df['behavior_avg']
df['high_performer'] = (df['performance_score'] > 85).astype(int)
df['gender_encoded'] = (df['gender'] == 'M').astype(int)
df['is_permanent_encoded'] = (df['is_permanent'] == 't').astype(int)
df['marital_status_encoded'] = df['marital_status'].map({'single': 0, 'married': 1, 'divorced': 2, 'widow': 3}).fillna(0)
df['tenure_category_encoded'] = pd.cut(df['tenure_years'], bins=[0, 3, 7, 100], labels=[0, 1, 2]).fillna(1).astype(int)
df['performance_level_encoded'] = pd.cut(df['performance_score'], bins=[0, 60, 75, 85, 300], labels=[0, 1, 2, 3]).fillna(1).astype(int)
df['behavioral_level_encoded'] = pd.cut(df['behavior_avg'], bins=[0, 60, 75, 85, 100], labels=[0, 1, 2, 3]).fillna(1).astype(int)

rating_map = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Very Good': 3, 'Excellent': 4, 
              'Need Improvement': 0, 'Average': 1}
df['performance_rating_encoded'] = df['performance_rating'].map(rating_map).fillna(2)

# Features
feature_cols = [
    'tenure_years', 'performance_score', 'behavior_avg', 'perf_beh_ratio',
    'combined_score', 'score_difference', 'high_performer', 'gender_encoded',
    'marital_status_encoded', 'is_permanent_encoded', 'tenure_category_encoded',
    'performance_level_encoded', 'behavioral_level_encoded', 'performance_rating_encoded'
]

X = df[feature_cols].fillna(0)
X_scaled = scaler.transform(X)
probabilities = model.predict_proba(X_scaled)[:, 1]
df['probability'] = probabilities

# Find Johan and Lina
johan = df[df['name'].str.contains('Johan Budiman', case=False, na=False)]
lina = df[df['name'].str.contains('Lina Nasution', case=False, na=False)]

if len(johan) == 0 or len(lina) == 0:
    print("❌ Could not find both employees")
    print(f"Johan found: {len(johan)}")
    print(f"Lina found: {len(lina)}")
    print("\nAvailable names:")
    print(df['name'].head(20).tolist())
else:
    johan = johan.iloc[0]
    lina = lina.iloc[0]
    
    print('1. BASIC COMPARISON')
    print('-'*80)
    print(f"{'Metric':<30} {'Johan Budiman':<20} {'Lina Nasution':<20} {'Winner':<10}")
    print('-'*80)
    winner = 'Johan' if johan['probability'] > lina['probability'] else 'Lina'
    print(f"{'Probability':<30} {johan['probability']:.4f} ({johan['probability']:.1%}) {lina['probability']:.4f} ({lina['probability']:.1%}) {winner:<10}")
    print(f"{'Performance Score':<30} {johan['performance_score']:<20.1f} {lina['performance_score']:<20.1f} {'Lina':<10}")
    print(f"{'Behavior Score':<30} {johan['behavior_avg']:<20.1f} {lina['behavior_avg']:<20.1f} {'Lina':<10}")
    print(f"{'Combined Score':<30} {johan['combined_score']:<20.1f} {lina['combined_score']:<20.1f} {'Lina':<10}")
    print(f"{'Tenure Years':<30} {johan['tenure_years']:<20.1f} {lina['tenure_years']:<20.1f} {'Tie':<10}")
    print()
    
    print('2. DERIVED FEATURES (KEY DIFFERENCES)')
    print('-'*80)
    print(f"{'Feature':<30} {'Johan':<20} {'Lina':<20} {'Impact':<10}")
    print('-'*80)
    print(f"{'score_difference':<30} {johan['score_difference']:<20.2f} {lina['score_difference']:<20.2f} {'Johan better' if abs(johan['score_difference']) < abs(lina['score_difference']) else 'Lina better':<10}")
    print(f"{'perf_beh_ratio':<30} {johan['perf_beh_ratio']:<20.3f} {lina['perf_beh_ratio']:<20.3f} {'Johan better' if abs(johan['perf_beh_ratio'] - 1) < abs(lina['perf_beh_ratio'] - 1) else 'Lina better':<10}")
    print(f"{'high_performer (>85)':<30} {johan['high_performer']:<20} {lina['high_performer']:<20} {'-':<10}")
    print(f"{'performance_level':<30} {johan['performance_level_encoded']:<20} {lina['performance_level_encoded']:<20} {'-':<10}")
    print(f"{'behavioral_level':<30} {johan['behavioral_level_encoded']:<20} {lina['behavioral_level_encoded']:<20} {'-':<10}")
    print()
    
    print('3. CATEGORICAL FEATURES')
    print('-'*80)
    print(f"{'Feature':<30} {'Johan':<20} {'Lina':<20}")
    print('-'*80)
    print(f"{'gender_encoded':<30} {johan['gender_encoded']:<20} {lina['gender_encoded']:<20}")
    print(f"{'marital_status_encoded':<30} {johan['marital_status_encoded']:<20} {lina['marital_status_encoded']:<20}")
    print(f"{'is_permanent_encoded':<30} {johan['is_permanent_encoded']:<20} {lina['is_permanent_encoded']:<20}")
    print(f"{'tenure_category':<30} {johan['tenure_category_encoded']:<20} {lina['tenure_category_encoded']:<20}")
    print(f"{'performance_rating':<30} {johan['performance_rating_encoded']:<20} {lina['performance_rating_encoded']:<20}")
    print()
    
    print('4. FEATURE IMPORTANCE ANALYSIS')
    print('-'*80)
    
    # Get feature importances
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("Top 10 Most Important Features:")
    for idx, row in feature_importance.head(10).iterrows():
        print(f"  {row['feature']:<30} {row['importance']:.4f}")
    print()
    
    print('5. SCALED FEATURE VALUES')
    print('-'*80)
    johan_idx = df[df['name'].str.contains('Johan Budiman', case=False, na=False)].index[0]
    lina_idx = df[df['name'].str.contains('Lina Nasution', case=False, na=False)].index[0]
    
    johan_scaled = X_scaled[johan_idx]
    lina_scaled = X_scaled[lina_idx]
    
    print(f"{'Feature':<30} {'Johan (scaled)':<20} {'Lina (scaled)':<20} {'Diff':<10}")
    print('-'*80)
    for i, feat in enumerate(feature_cols):
        diff = johan_scaled[i] - lina_scaled[i]
        print(f"{feat:<30} {johan_scaled[i]:<20.3f} {lina_scaled[i]:<20.3f} {diff:<10.3f}")
    print()
    
    print('='*80)
    print('CONCLUSION')
    print('='*80)
    print()
    
    # Analyze key differences
    if abs(johan['score_difference']) < abs(lina['score_difference']):
        print("✅ KEY FACTOR 1: Balance")
        print(f"   Johan has better balance (diff: {johan['score_difference']:.1f})")
        print(f"   Lina has larger gap (diff: {lina['score_difference']:.1f})")
        print(f"   Model prefers balanced profiles!")
        print()
    
    if johan['performance_level_encoded'] < lina['performance_level_encoded']:
        print("✅ KEY FACTOR 2: Optimal Range")
        print(f"   Johan in level {johan['performance_level_encoded']} (75-85 range)")
        print(f"   Lina in level {lina['performance_level_encoded']} (85+ range)")
        print(f"   Model may prefer 'proven promotion zone' over 'overqualified'")
        print()
    
    print("💡 HYPOTHESIS:")
    print("   Random Forest model learned from historical data that:")
    print("   1. Balanced employees (small perf-beh gap) get promoted more")
    print("   2. Moderate-high performers (75-85) have better promotion rate")
    print("   3. Very high performers (>90) may be kept in current role")
    print("   4. Other factors (gender, status, etc.) also contribute")
    print()
    print(f"   Result: Johan {johan['probability']:.1%} > Lina {lina['probability']:.1%}")
    print(f"   Difference: {(johan['probability'] - lina['probability'])*100:.2f} percentage points")
