"""
Test Random Forest Model
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

print('Testing Random Forest Model')
print('='*80)

repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data'
results_dir = repo_root / 'results' / 'advanced_models'

# Load RF model
model = joblib.load(results_dir / 'random_forest_model.pkl')
scaler = joblib.load(data_dir / 'processed' / 'scaler.pkl')

print(f'Model: {type(model).__name__}')
print()

# Load data
df = pd.read_csv(data_dir / 'final' / 'sample_dataset_100_balanced.csv')
print(f'Data: {len(df)} rows')
print()

# Feature engineering (simplified)
df['combined_score'] = (df['performance_score'] + df['behavior_avg']) / 2
df['perf_beh_ratio'] = df['performance_score'] / (df['behavior_avg'] + 0.1)
df['score_difference'] = df['performance_score'] - df['behavior_avg']
df['high_performer'] = (df['performance_score'] > 85).astype(int)
df['gender_encoded'] = (df['gender'] == 'M').astype(int)
df['is_permanent_encoded'] = (df['is_permanent'] == 't').astype(int)
df['marital_status_encoded'] = df['marital_status'].map({'single': 0, 'married': 1, 'divorced': 2, 'widow': 3}).fillna(0)

df['tenure_category_encoded'] = pd.cut(df['tenure_years'], bins=[0, 3, 7, 100], labels=[0, 1, 2]).fillna(1).astype(int)
df['performance_level_encoded'] = pd.cut(df['performance_score'], bins=[0, 60, 75, 85, 200], labels=[0, 1, 2, 3]).fillna(1).astype(int)
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

# Predict
predictions = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)[:, 1]

print(f'Predictions: {predictions.sum()} promoted ({predictions.mean():.1%})')
print(f'Probabilities: {probabilities.min():.4f} - {probabilities.max():.4f} (avg: {probabilities.mean():.4f})')
print()

# Top 10
df['probability'] = probabilities
top_10 = df.nlargest(10, 'probability')
print('Top 10:')
for idx, row in top_10.iterrows():
    print(f"  {row.get('name', 'N/A'):20s} | {row['probability']:.2%} | Perf: {row['performance_score']:.1f} | Beh: {row['behavior_avg']:.1f}")
print()

if probabilities.max() > 0.5:
    print(f'✅ SUCCESS! Found {(probabilities >= 0.5).sum()} candidates with probability ≥ 50%')
else:
    print(f'❌ Still all < 50%. Max: {probabilities.max():.4f}')
