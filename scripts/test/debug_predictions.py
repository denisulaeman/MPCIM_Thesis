"""
Debug Predictions - Why All 0%?
Check model, features, and data
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

print('='*80)
print('DEBUG PREDICTIONS - WHY ALL 0%?')
print('='*80)
print()

# Paths
repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data'
models_dir = repo_root / 'models'

# Load model and scaler
print('1. LOADING MODEL & SCALER')
print('-'*80)

model_path = models_dir / 'neural_network_model.pkl'
scaler_path = data_dir / 'processed' / 'scaler.pkl'

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

print(f'✅ Model: {type(model).__name__}')
print(f'✅ Scaler: {type(scaler).__name__}')
print()

# Load data
print('2. LOADING DATA')
print('-'*80)

df = pd.read_csv(data_dir / 'final' / 'sample_dataset_1000_balanced.csv')
print(f'✅ Loaded: {len(df):,} rows')
print(f'Columns: {df.columns.tolist()[:5]}...')
print()

# Check actual promotions in data
print('3. ACTUAL PROMOTIONS IN DATA')
print('-'*80)
if 'has_promotion' in df.columns:
    actual_promoted = df['has_promotion'].sum()
    actual_rate = df['has_promotion'].mean()
    print(f'Actual promoted: {actual_promoted} ({actual_rate:.1%})')
    print(f'Not promoted: {len(df) - actual_promoted} ({1-actual_rate:.1%})')
else:
    print('⚠️  No has_promotion column')
print()

# Check data ranges
print('4. DATA RANGES')
print('-'*80)
print(f'performance_score: {df["performance_score"].min():.1f} - {df["performance_score"].max():.1f}')
print(f'behavior_avg: {df["behavior_avg"].min():.1f} - {df["behavior_avg"].max():.1f}')
print(f'tenure_years: {df["tenure_years"].min():.0f} - {df["tenure_years"].max():.0f}')
print()

# Feature engineering (same as app)
print('5. FEATURE ENGINEERING')
print('-'*80)

df_feat = df.copy()

# Fill NaN
df_feat['performance_score'].fillna(df_feat['performance_score'].median(), inplace=True)
df_feat['behavior_avg'].fillna(df_feat['behavior_avg'].median(), inplace=True)
df_feat['tenure_years'].fillna(df_feat['tenure_years'].median(), inplace=True)

# Combined score
df_feat['combined_score'] = (df_feat['performance_score'] + df_feat['behavior_avg']) / 2

# Tenure categories
df_feat['tenure_category'] = pd.cut(df_feat['tenure_years'], 
                                bins=[0, 3, 7, 100], 
                                labels=['Junior', 'Mid', 'Senior'])
df_feat['tenure_category_encoded'] = df_feat['tenure_category'].map({'Junior': 0, 'Mid': 1, 'Senior': 2})
df_feat['tenure_category_encoded'].fillna(1, inplace=True)

# Performance rating encoding
if 'performance_rating' in df_feat.columns:
    rating_map = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Very Good': 3, 'Excellent': 4, 
                  'Need Improvement': 0, 'Average': 1}
    df_feat['performance_rating_encoded'] = df_feat['performance_rating'].map(rating_map)
    df_feat['performance_rating_encoded'].fillna(2, inplace=True)
else:
    df_feat['performance_rating_encoded'] = 2

# Score ratio
df_feat['perf_beh_ratio'] = df_feat['performance_score'] / (df_feat['behavior_avg'] + 0.1)

# Score difference
df_feat['score_difference'] = df_feat['performance_score'] - df_feat['behavior_avg']

# High performer
df_feat['high_performer'] = (df_feat['performance_score'] > 85).astype(int)

# Binary encodings
df_feat['gender_encoded'] = (df_feat['gender'] == 'M').astype(int)
df_feat['is_permanent_encoded'] = (df_feat['is_permanent'] == 't').astype(int) if df_feat['is_permanent'].dtype == 'object' else df_feat['is_permanent'].astype(int)

# Marital status
marital_map = {'single': 0, 'married': 1, 'divorced': 2, 'widow': 3, 'widowed': 3,
               'Single': 0, 'Married': 1, 'Divorced': 2, 'Widow': 3, 'Widowed': 3}
df_feat['marital_status_encoded'] = df_feat['marital_status'].map(marital_map)
df_feat['marital_status_encoded'].fillna(0, inplace=True)

# Performance level
df_feat['performance_level_encoded'] = pd.cut(df_feat['performance_score'], 
                                         bins=[0, 60, 75, 85, 100],
                                         labels=[0, 1, 2, 3])
df_feat['performance_level_encoded'] = df_feat['performance_level_encoded'].fillna(1).astype(int)

# Behavioral level
df_feat['behavioral_level_encoded'] = pd.cut(df_feat['behavior_avg'],
                                        bins=[0, 60, 75, 85, 100],
                                        labels=[0, 1, 2, 3])
df_feat['behavioral_level_encoded'] = df_feat['behavioral_level_encoded'].fillna(1).astype(int)

print('✅ Features engineered')
print()

# Check feature stats
print('6. FEATURE STATISTICS')
print('-'*80)
print(f'high_performer: {df_feat["high_performer"].sum()} employees ({df_feat["high_performer"].mean():.1%})')
print(f'combined_score: {df_feat["combined_score"].mean():.1f} (avg)')
print(f'performance_level_encoded: {df_feat["performance_level_encoded"].value_counts().to_dict()}')
print(f'behavioral_level_encoded: {df_feat["behavioral_level_encoded"].value_counts().to_dict()}')
print()

# Prepare features
print('7. PREPARING FEATURES FOR PREDICTION')
print('-'*80)

feature_cols = [
    'tenure_years', 'performance_score', 'behavior_avg', 'perf_beh_ratio',
    'combined_score', 'score_difference', 'high_performer', 'gender_encoded',
    'marital_status_encoded', 'is_permanent_encoded', 'tenure_category_encoded',
    'performance_level_encoded', 'behavioral_level_encoded', 'performance_rating_encoded'
]

X = df_feat[feature_cols].fillna(0)
print(f'✅ Feature matrix: {X.shape}')
print(f'Feature columns: {feature_cols}')
print()

# Check for NaN or inf
print('8. DATA QUALITY CHECK')
print('-'*80)
print(f'NaN values: {X.isna().sum().sum()}')
X_numeric = X.select_dtypes(include=[np.number])
print(f'Inf values: {np.isinf(X_numeric.values).sum()}')
print()

# Sample features
print('9. SAMPLE FEATURES (First 3 employees)')
print('-'*80)
print(X.head(3).to_string())
print()

# Scale features
print('10. SCALING FEATURES')
print('-'*80)
X_scaled = scaler.transform(X)
print(f'✅ Scaled: {X_scaled.shape}')
print(f'Scaled range: {X_scaled.min():.2f} to {X_scaled.max():.2f}')
print()

# Predict
print('11. MAKING PREDICTIONS')
print('-'*80)
predictions = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)[:, 1]

print(f'Predictions: {predictions.sum()} promoted ({predictions.mean():.1%})')
print(f'Probabilities:')
print(f'  Min: {probabilities.min():.4f}')
print(f'  Max: {probabilities.max():.4f}')
print(f'  Mean: {probabilities.mean():.4f}')
print(f'  Median: {np.median(probabilities):.4f}')
print()

# Distribution
print('12. PROBABILITY DISTRIBUTION')
print('-'*80)
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
hist, _ = np.histogram(probabilities, bins=bins)
for i, (low, high) in enumerate(zip(bins[:-1], bins[1:])):
    count = hist[i]
    pct = count / len(probabilities) * 100
    bar = '█' * int(pct / 2)
    print(f'{low:.1f}-{high:.1f}: {count:4d} ({pct:5.1f}%) {bar}')
print()

# Top candidates
print('13. TOP 10 CANDIDATES')
print('-'*80)
df_feat['probability'] = probabilities
top_10 = df_feat.nlargest(10, 'probability')
for idx, row in top_10.iterrows():
    print(f"{row.get('name', 'N/A'):20s} | Prob: {row['probability']:.4f} | "
          f"Perf: {row['performance_score']:.1f} | Beh: {row['behavior_avg']:.1f} | "
          f"High: {row['high_performer']}")
print()

print('='*80)
print('CONCLUSION')
print('='*80)

if probabilities.max() < 0.5:
    print('❌ PROBLEM: All probabilities < 50%')
    print()
    print('Possible causes:')
    print('1. Model was trained on different data distribution')
    print('2. Feature engineering mismatch')
    print('3. Model is too conservative')
    print('4. Data quality issues')
    print()
    print('Recommendations:')
    print('1. Check training data distribution')
    print('2. Retrain model with current data')
    print('3. Lower threshold to 10-20%')
    print('4. Check feature importance')
else:
    print(f'✅ Found {(probabilities >= 0.5).sum()} candidates with probability ≥ 50%')

print()
