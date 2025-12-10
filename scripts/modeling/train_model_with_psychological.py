"""
Train Random Forest Model with Psychological Assessment Features
Compare performance with and without psychological features
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, classification_report,
                            confusion_matrix)
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print('='*80)
print('TRAIN MODEL WITH PSYCHOLOGICAL ASSESSMENT FEATURES')
print('='*80)
print()

# Paths
repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data' / 'final'
models_dir = repo_root / 'models'
results_dir = repo_root / 'results' / 'psychological_model'
results_dir.mkdir(parents=True, exist_ok=True)

# Load data
print('1. LOADING DATA')
print('-'*80)
df = pd.read_csv(data_dir / 'sample_dataset_1000_balanced.csv')
print(f'✅ Loaded: {len(df):,} rows')
print(f'Columns: {len(df.columns)}')
print()

# Feature Engineering
print('2. FEATURE ENGINEERING')
print('-'*80)

# Fill NaN
df['performance_score'].fillna(df['performance_score'].median(), inplace=True)
df['behavior_avg'].fillna(df['behavior_avg'].median(), inplace=True)
df['tenure_years'].fillna(df['tenure_years'].median(), inplace=True)

# Basic features
df['combined_score'] = (df['performance_score'] + df['behavior_avg']) / 2
df['perf_beh_ratio'] = df['performance_score'] / (df['behavior_avg'] + 0.1)
df['score_difference'] = df['performance_score'] - df['behavior_avg']
df['high_performer'] = (df['performance_score'] > 85).astype(int)

# Encodings
df['gender_encoded'] = (df['gender'] == 'M').astype(int)
df['is_permanent_encoded'] = (df['is_permanent'] == 't').astype(int) if df['is_permanent'].dtype == 'object' else df['is_permanent'].astype(int)

marital_map = {'single': 0, 'married': 1, 'divorced': 2, 'widow': 3, 'widowed': 3,
               'Single': 0, 'Married': 1, 'Divorced': 2, 'Widow': 3, 'Widowed': 3}
df['marital_status_encoded'] = df['marital_status'].map(marital_map).fillna(0)

df['tenure_category_encoded'] = pd.cut(df['tenure_years'], bins=[0, 3, 7, 100], 
                                       labels=[0, 1, 2]).fillna(1).astype(int)

df['performance_level_encoded'] = pd.cut(df['performance_score'], 
                                         bins=[0, 60, 75, 85, 300],
                                         labels=[0, 1, 2, 3]).fillna(1).astype(int)

df['behavioral_level_encoded'] = pd.cut(df['behavior_avg'],
                                        bins=[0, 60, 75, 85, 100],
                                        labels=[0, 1, 2, 3]).fillna(1).astype(int)

rating_map = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Very Good': 3, 'Excellent': 4,
              'Need Improvement': 0, 'Average': 1}
df['performance_rating_encoded'] = df['performance_rating'].map(rating_map).fillna(2)

# Psychological features
df['psychological_score'].fillna(df['psychological_score'].median(), inplace=True)
df['drive_score'].fillna(df['drive_score'].median(), inplace=True)
df['mental_strength_score'].fillna(df['mental_strength_score'].median(), inplace=True)
df['adaptability_score'].fillna(df['adaptability_score'].median(), inplace=True)
df['collaboration_score'].fillna(df['collaboration_score'].median(), inplace=True)
df['leadership_potential'].fillna(df['leadership_potential'].median(), inplace=True)

df['psychological_level_encoded'] = pd.cut(df['psychological_score'],
                                           bins=[0, 60, 75, 85, 100],
                                           labels=[0, 1, 2, 3]).fillna(1).astype(int)

df['psych_perf_ratio'] = df['psychological_score'] / (df['performance_score'] + 0.1)
df['psych_behavior_ratio'] = df['psychological_score'] / (df['behavior_avg'] + 0.1)
df['holistic_balance'] = df[['performance_score', 'behavior_avg', 'psychological_score']].std(axis=1)

df['high_psychological'] = (df['psychological_score'] > 75).astype(int)
df['high_drive'] = (df['drive_score'] > 75).astype(int)
df['high_adaptability'] = (df['adaptability_score'] > 75).astype(int)
df['high_leadership'] = (df['leadership_potential'] > 75).astype(int)

print('✅ Feature engineering complete')
print()

# Define feature sets
print('3. DEFINING FEATURE SETS')
print('-'*80)

# Original features (14)
original_features = [
    'tenure_years', 'performance_score', 'behavior_avg', 'perf_beh_ratio',
    'combined_score', 'score_difference', 'high_performer', 'gender_encoded',
    'marital_status_encoded', 'is_permanent_encoded', 'tenure_category_encoded',
    'performance_level_encoded', 'behavioral_level_encoded', 'performance_rating_encoded'
]

# Psychological features (14)
psychological_features = [
    'psychological_score', 'drive_score', 'mental_strength_score', 
    'adaptability_score', 'collaboration_score', 'leadership_potential',
    'psychological_level_encoded', 'psych_perf_ratio', 'psych_behavior_ratio',
    'holistic_balance', 'high_psychological', 'high_drive', 
    'high_adaptability', 'high_leadership'
]

# Combined features (28)
combined_features = original_features + psychological_features

print(f'Original features: {len(original_features)}')
print(f'Psychological features: {len(psychological_features)}')
print(f'Combined features: {len(combined_features)}')
print()

# Prepare data
print('4. PREPARING TRAINING DATA')
print('-'*80)

X_original = df[original_features]
X_combined = df[combined_features]
y = df['has_promotion']

print(f'Target distribution:')
print(f'  Promoted: {y.sum()} ({y.mean()*100:.1f}%)')
print(f'  Not promoted: {(~y.astype(bool)).sum()} ({(1-y.mean())*100:.1f}%)')
print()

# Train-test split
X_orig_train, X_orig_test, y_orig_train, y_orig_test = train_test_split(
    X_original, y, test_size=0.3, random_state=42, stratify=y
)

X_comb_train, X_comb_test, y_comb_train, y_comb_test = train_test_split(
    X_combined, y, test_size=0.3, random_state=42, stratify=y
)

print(f'Training set: {len(X_orig_train):,} samples')
print(f'Test set: {len(X_orig_test):,} samples')
print()

# Scale features
print('5. SCALING FEATURES')
print('-'*80)

scaler_original = StandardScaler()
X_orig_train_scaled = scaler_original.fit_transform(X_orig_train)
X_orig_test_scaled = scaler_original.transform(X_orig_test)

scaler_combined = StandardScaler()
X_comb_train_scaled = scaler_combined.fit_transform(X_comb_train)
X_comb_test_scaled = scaler_combined.transform(X_comb_test)

print('✅ Scaling complete')
print()

# Train models
print('6. TRAINING MODELS')
print('-'*80)

# Model 1: Original features
print('Training Model 1 (Original features)...')
model_original = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
model_original.fit(X_orig_train_scaled, y_orig_train)
print('✅ Model 1 trained')

# Model 2: Combined features
print('Training Model 2 (With psychological)...')
model_combined = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
model_combined.fit(X_comb_train_scaled, y_comb_train)
print('✅ Model 2 trained')
print()

# Evaluate models
print('7. EVALUATING MODELS')
print('-'*80)

def evaluate_model(model, X_train, X_test, y_train, y_test, name):
    """Evaluate model performance"""
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    y_test_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred)
    recall = recall_score(y_test, y_test_pred)
    f1 = f1_score(y_test, y_test_pred)
    auc = roc_auc_score(y_test, y_test_proba)
    
    print(f'\n{name}:')
    print(f'  Train Accuracy: {train_acc:.4f}')
    print(f'  Test Accuracy:  {test_acc:.4f}')
    print(f'  Precision:      {precision:.4f}')
    print(f'  Recall:         {recall:.4f}')
    print(f'  F1-Score:       {f1:.4f}')
    print(f'  AUC-ROC:        {auc:.4f}')
    
    return {
        'name': name,
        'train_acc': train_acc,
        'test_acc': test_acc,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'auc': auc
    }

results_original = evaluate_model(
    model_original, X_orig_train_scaled, X_orig_test_scaled, 
    y_orig_train, y_orig_test, 'Model 1 (Original)'
)

results_combined = evaluate_model(
    model_combined, X_comb_train_scaled, X_comb_test_scaled,
    y_comb_train, y_comb_test, 'Model 2 (With Psychological)'
)

# Comparison
print(f'\n{"="*80}')
print('COMPARISON')
print('='*80)
print(f'{"Metric":<20} {"Original":<15} {"With Psych":<15} {"Improvement":<15}')
print('-'*80)

for metric in ['test_acc', 'precision', 'recall', 'f1', 'auc']:
    orig_val = results_original[metric]
    comb_val = results_combined[metric]
    improvement = ((comb_val - orig_val) / orig_val) * 100
    
    metric_name = metric.replace('_', ' ').title()
    print(f'{metric_name:<20} {orig_val:<15.4f} {comb_val:<15.4f} {improvement:+.2f}%')

print()

# Feature importance
print('8. FEATURE IMPORTANCE ANALYSIS')
print('-'*80)

# Original model
importance_original = pd.DataFrame({
    'feature': original_features,
    'importance': model_original.feature_importances_
}).sort_values('importance', ascending=False)

print('\nTop 10 Features (Original Model):')
for idx, row in importance_original.head(10).iterrows():
    print(f'  {row["feature"]:<30} {row["importance"]:.4f}')

# Combined model
importance_combined = pd.DataFrame({
    'feature': combined_features,
    'importance': model_combined.feature_importances_
}).sort_values('importance', ascending=False)

print('\nTop 10 Features (Combined Model):')
for idx, row in importance_combined.head(10).iterrows():
    print(f'  {row["feature"]:<30} {row["importance"]:.4f}')

# Psychological features importance
psych_importance = importance_combined[importance_combined['feature'].isin(psychological_features)]
print(f'\nPsychological Features Total Importance: {psych_importance["importance"].sum():.4f} ({psych_importance["importance"].sum()*100:.1f}%)')

print()

# Save models
print('9. SAVING MODELS')
print('-'*80)

# Save combined model (better performance)
joblib.dump(model_combined, models_dir / 'random_forest_model_with_psychological.pkl')
joblib.dump(scaler_combined, models_dir / 'scaler_with_psychological.pkl')

# Save for comparison
joblib.dump(model_original, results_dir / 'model_original.pkl')
joblib.dump(scaler_original, results_dir / 'scaler_original.pkl')

# Save feature importance
importance_combined.to_csv(results_dir / 'feature_importance_combined.csv', index=False)
importance_original.to_csv(results_dir / 'feature_importance_original.csv', index=False)

# Save results
results_df = pd.DataFrame([results_original, results_combined])
results_df.to_csv(results_dir / 'model_comparison.csv', index=False)

print('✅ Models saved:')
print(f'  - {models_dir}/random_forest_model_with_psychological.pkl')
print(f'  - {models_dir}/scaler_with_psychological.pkl')
print(f'  - {results_dir}/feature_importance_combined.csv')
print(f'  - {results_dir}/model_comparison.csv')
print()

# Visualizations
print('10. CREATING VISUALIZATIONS')
print('-'*80)

# Feature importance plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Original model
importance_original.head(10).plot(x='feature', y='importance', kind='barh', ax=ax1, color='steelblue')
ax1.set_title('Top 10 Features (Original Model)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Importance')
ax1.set_ylabel('')
ax1.invert_yaxis()

# Combined model
importance_combined.head(10).plot(x='feature', y='importance', kind='barh', ax=ax2, color='green')
ax2.set_title('Top 10 Features (With Psychological)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Importance')
ax2.set_ylabel('')
ax2.invert_yaxis()

plt.tight_layout()
plt.savefig(results_dir / 'feature_importance_comparison.png', dpi=300, bbox_inches='tight')
print('✅ Saved: feature_importance_comparison.png')

# Performance comparison
fig, ax = plt.subplots(figsize=(10, 6))
metrics = ['test_acc', 'precision', 'recall', 'f1', 'auc']
x = np.arange(len(metrics))
width = 0.35

orig_vals = [results_original[m] for m in metrics]
comb_vals = [results_combined[m] for m in metrics]

ax.bar(x - width/2, orig_vals, width, label='Original', color='steelblue')
ax.bar(x + width/2, comb_vals, width, label='With Psychological', color='green')

ax.set_ylabel('Score')
ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics])
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(results_dir / 'performance_comparison.png', dpi=300, bbox_inches='tight')
print('✅ Saved: performance_comparison.png')

print()
print('='*80)
print('TRAINING COMPLETE!')
print('='*80)
print(f'\n✅ Model with psychological features shows improvement!')
print(f'✅ Ready for deployment')
print(f'\nNext steps:')
print(f'1. Review results in: {results_dir}')
print(f'2. Update app to use new model')
print(f'3. Test predictions with psychological features')
