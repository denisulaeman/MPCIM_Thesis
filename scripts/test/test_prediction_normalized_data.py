"""
Test Prediction on Normalized Data
Check why predictions are all 0 (no promotions)
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

print('='*80)
print('TEST PREDICTION ON NORMALIZED DATA')
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

print(f'✅ Model loaded: {type(model).__name__}')
print(f'✅ Scaler loaded: {type(scaler).__name__}')
print()

# Load normalized data
print('2. LOADING NORMALIZED DATA')
print('-'*80)

df_normalized = pd.read_csv(data_dir / 'final' / 'sample_dataset_1000_balanced_normalized.csv')
print(f'✅ Loaded: {len(df_normalized):,} rows')
print()

# Check data ranges
print('3. DATA RANGES (NORMALIZED)')
print('-'*80)
print(f'performance_score: {df_normalized["performance_score"].min():.2f} - {df_normalized["performance_score"].max():.2f}')
print(f'behavior_avg: {df_normalized["behavior_avg"].min():.2f} - {df_normalized["behavior_avg"].max():.2f}')
print(f'tenure_years: {df_normalized["tenure_years"].min():.2f} - {df_normalized["tenure_years"].max():.2f}')
print()

# Load original (non-normalized) data for comparison
print('4. LOADING ORIGINAL DATA (NON-NORMALIZED)')
print('-'*80)

df_original = pd.read_csv(data_dir / 'final' / 'sample_dataset_1000_balanced.csv')
print(f'✅ Loaded: {len(df_original):,} rows')
print()

print('5. DATA RANGES (ORIGINAL)')
print('-'*80)
print(f'performance_score: {df_original["performance_score"].min():.2f} - {df_original["performance_score"].max():.2f}')
print(f'behavior_avg: {df_original["behavior_avg"].min():.2f} - {df_original["behavior_avg"].max():.2f}')
print(f'tenure_years: {df_original["tenure_years"].min():.2f} - {df_original["tenure_years"].max():.2f}')
print()

# Feature engineering function (same as app)
def engineer_features(df):
    """Apply feature engineering"""
    df = df.copy()
    
    # Fill NaN
    df['performance_score'].fillna(df['performance_score'].median(), inplace=True)
    df['behavior_avg'].fillna(df['behavior_avg'].median(), inplace=True)
    df['tenure_years'].fillna(df['tenure_years'].median(), inplace=True)
    
    # Combined score
    df['combined_score'] = (df['performance_score'] + df['behavior_avg']) / 2
    
    # Tenure categories
    df['tenure_category'] = pd.cut(df['tenure_years'], 
                                    bins=[0, 3, 7, 100], 
                                    labels=['Junior', 'Mid', 'Senior'])
    df['tenure_category_encoded'] = df['tenure_category'].map({'Junior': 0, 'Mid': 1, 'Senior': 2})
    df['tenure_category_encoded'].fillna(1, inplace=True)
    
    # Performance rating encoding
    if 'performance_rating' in df.columns:
        rating_map = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Very Good': 3, 'Excellent': 4}
        df['performance_rating_encoded'] = df['performance_rating'].map(rating_map)
        df['performance_rating_encoded'].fillna(2, inplace=True)
    else:
        df['performance_rating_encoded'] = 2
    
    # Score ratio
    df['perf_beh_ratio'] = df['performance_score'] / (df['behavior_avg'] + 0.1)
    
    # Score difference
    df['score_difference'] = df['performance_score'] - df['behavior_avg']
    
    # High performer
    df['high_performer'] = (df['performance_score'] > 85).astype(int)
    
    # Binary encodings
    df['gender_encoded'] = (df['gender'] == 'M').astype(int)
    df['is_permanent_encoded'] = (df['is_permanent'] == 't').astype(int) if df['is_permanent'].dtype == 'object' else df['is_permanent'].astype(int)
    
    # Marital status
    marital_map = {'Single': 0, 'Married': 1, 'Divorced': 2, 'Widowed': 3}
    df['marital_status_encoded'] = df['marital_status'].map(marital_map)
    df['marital_status_encoded'].fillna(0, inplace=True)
    
    # Performance level
    df['performance_level_encoded'] = pd.cut(df['performance_score'], 
                                             bins=[0, 60, 75, 85, 100],
                                             labels=[0, 1, 2, 3])
    df['performance_level_encoded'] = df['performance_level_encoded'].fillna(1).astype(int)
    
    # Behavioral level
    df['behavioral_level_encoded'] = pd.cut(df['behavior_avg'],
                                            bins=[0, 60, 75, 85, 100],
                                            labels=[0, 1, 2, 3])
    df['behavioral_level_encoded'] = df['behavioral_level_encoded'].fillna(1).astype(int)
    
    return df

# Test on NORMALIZED data
print('6. TESTING ON NORMALIZED DATA')
print('-'*80)

df_norm_feat = engineer_features(df_normalized)

# Feature columns
feature_cols = [
    'tenure_years', 'performance_score', 'behavior_avg', 'perf_beh_ratio',
    'combined_score', 'score_difference', 'high_performer', 'gender_encoded',
    'marital_status_encoded', 'is_permanent_encoded', 'tenure_category_encoded',
    'performance_level_encoded', 'behavioral_level_encoded', 'performance_rating_encoded'
]

X_norm = df_norm_feat[feature_cols].fillna(0)
X_norm_scaled = scaler.transform(X_norm)

predictions_norm = model.predict(X_norm_scaled)
probabilities_norm = model.predict_proba(X_norm_scaled)[:, 1]

print(f'Predictions (normalized data):')
print(f'  Total predicted promoted: {predictions_norm.sum()}')
print(f'  Promotion rate: {predictions_norm.mean():.2%}')
print(f'  Avg probability: {probabilities_norm.mean():.2%}')
print(f'  Max probability: {probabilities_norm.max():.2%}')
print(f'  Min probability: {probabilities_norm.min():.2%}')
print()

# Test on ORIGINAL data
print('7. TESTING ON ORIGINAL DATA')
print('-'*80)

df_orig_feat = engineer_features(df_original)
X_orig = df_orig_feat[feature_cols].fillna(0)
X_orig_scaled = scaler.transform(X_orig)

predictions_orig = model.predict(X_orig_scaled)
probabilities_orig = model.predict_proba(X_orig_scaled)[:, 1]

print(f'Predictions (original data):')
print(f'  Total predicted promoted: {predictions_orig.sum()}')
print(f'  Promotion rate: {predictions_orig.mean():.2%}')
print(f'  Avg probability: {probabilities_orig.mean():.2%}')
print(f'  Max probability: {probabilities_orig.max():.2%}')
print(f'  Min probability: {probabilities_orig.min():.2%}')
print()

# Compare features
print('8. FEATURE COMPARISON')
print('-'*80)

print('\nNormalized data (first employee):')
print(f'  performance_score: {df_norm_feat["performance_score"].iloc[0]:.2f}')
print(f'  behavior_avg: {df_norm_feat["behavior_avg"].iloc[0]:.2f}')
print(f'  combined_score: {df_norm_feat["combined_score"].iloc[0]:.2f}')
print(f'  high_performer: {df_norm_feat["high_performer"].iloc[0]}')
print(f'  performance_level_encoded: {df_norm_feat["performance_level_encoded"].iloc[0]}')

print('\nOriginal data (first employee):')
print(f'  performance_score: {df_orig_feat["performance_score"].iloc[0]:.2f}')
print(f'  behavior_avg: {df_orig_feat["behavior_avg"].iloc[0]:.2f}')
print(f'  combined_score: {df_orig_feat["combined_score"].iloc[0]:.2f}')
print(f'  high_performer: {df_orig_feat["high_performer"].iloc[0]}')
print(f'  performance_level_encoded: {df_orig_feat["performance_level_encoded"].iloc[0]}')

print()
print('='*80)
print('CONCLUSION')
print('='*80)
print()

if predictions_norm.sum() == 0:
    print('❌ PROBLEM FOUND:')
    print('   Normalized data produces 0 predictions!')
    print()
    print('💡 ROOT CAUSE:')
    print('   - Model was trained on ORIGINAL data (0-100 scale)')
    print('   - Normalized data uses different scale (28-88)')
    print('   - Features like high_performer (>85) fail on normalized data')
    print('   - performance_level_encoded bins [0,60,75,85,100] wrong for normalized')
    print()
    print('✅ SOLUTION:')
    print('   Use sample_dataset_1000_balanced.csv (NOT normalized version)')
    print('   Or: De-normalize the data before prediction')
else:
    print('✅ Predictions working on normalized data')

print()
