"""
Promotion Prediction Model with Job Level Features
===================================================

Tujuan:
1. Build ML model untuk prediksi promosi
2. Menggunakan job level sebagai fitur utama
3. Feature importance analysis
4. Model evaluation dan interpretasi

Target: has_promotion (binary classification)
Features: performance, behavior, tenure, job_level, dll

Author: Denis Ulaeman
Date: Dec 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix, roc_auc_score, 
                             roc_curve, precision_recall_curve, f1_score)
import warnings
warnings.filterwarnings('ignore')

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
FINAL_DIR = DATA_DIR / "final"
RESULTS_DIR = BASE_DIR / "results" / "promotion_prediction"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("PROMOTION PREDICTION MODEL WITH JOB LEVEL")
print("="*80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1] Loading data...")

# Try to load enhanced dataset with job level
try:
    df = pd.read_csv(FINAL_DIR / "integrated_full_dataset_with_job_level.csv")
    print(f"✓ Loaded enhanced dataset: {len(df)} records")
except FileNotFoundError:
    print("⚠️  Enhanced dataset not found. Loading base dataset...")
    df = pd.read_csv(FINAL_DIR / "integrated_full_dataset.csv")
    print(f"✓ Loaded base dataset: {len(df)} records")
    print("   Note: Run 01_job_level_analysis.py first for enhanced features")

# Check target variable
if 'has_promotion' not in df.columns:
    print("\n⚠️  WARNING: 'has_promotion' column not found!")
    print("   Creating dummy target for demonstration...")
    # Create synthetic target based on performance and leadership
    df['has_promotion'] = (
        (df['performance_score'] > df['performance_score'].quantile(0.7)) &
        (df['leadership_potential'] > df['leadership_potential'].quantile(0.6))
    ).astype(int)

print(f"\nTarget Distribution:")
print(df['has_promotion'].value_counts())
print(f"Promotion Rate: {df['has_promotion'].mean()*100:.2f}%")

# ============================================================================
# 2. FEATURE ENGINEERING
# ============================================================================
print("\n[2] Feature engineering...")

# Select features for modeling
feature_cols = [
    'tenure_years',
    'performance_score',
    'behavior_avg',
    'psychological_score',
    'drive_score',
    'mental_strength_score',
    'adaptability_score',
    'collaboration_score',
    'holistic_score',
    'leadership_potential',
    'score_alignment'
]

# Add job level features if available
if 'group_job_level' in df.columns:
    feature_cols.append('group_job_level')
    print("✓ Added group_job_level (0=Support, 1=Staff, 2=Management)")

if 'is_management' in df.columns:
    feature_cols.extend(['is_management', 'is_staff', 'is_support'])
    print("✓ Added job level binary indicators")

if 'promotion_readiness_score' in df.columns:
    feature_cols.append('promotion_readiness_score')
    print("✓ Added promotion_readiness_score")

if 'tenure_level_ratio' in df.columns:
    feature_cols.append('tenure_level_ratio')
    print("✓ Added tenure_level_ratio")

# Encode categorical job level if available
if 'level_name' in df.columns:
    le_level = LabelEncoder()
    df['level_name_encoded'] = le_level.fit_transform(df['level_name'].fillna('Unknown'))
    feature_cols.append('level_name_encoded')
    print(f"✓ Encoded level_name: {len(le_level.classes_)} unique levels")
    
    # Save encoder mapping
    level_mapping = pd.DataFrame({
        'level_name': le_level.classes_,
        'encoded_value': range(len(le_level.classes_))
    })
    level_mapping.to_csv(RESULTS_DIR / "job_level_encoding.csv", index=False)

# Encode gender
if 'gender' in df.columns:
    df['gender_encoded'] = df['gender'].map({'O': 0, 'P': 1}).fillna(0)
    feature_cols.append('gender_encoded')
    print("✓ Encoded gender")

# Create interaction features
df['performance_x_leadership'] = df['performance_score'] * df['leadership_potential']
df['behavior_x_tenure'] = df['behavior_avg'] * df['tenure_years']
feature_cols.extend(['performance_x_leadership', 'behavior_x_tenure'])
print("✓ Created interaction features")

# Remove rows with missing values in key features
df_clean = df[feature_cols + ['has_promotion']].dropna()
print(f"\n✓ Clean dataset: {len(df_clean)} records ({len(df_clean)/len(df)*100:.1f}% of original)")

# ============================================================================
# 3. PREPARE TRAIN/TEST SPLIT
# ============================================================================
print("\n[3] Preparing train/test split...")

X = df_clean[feature_cols]
y = df_clean['has_promotion']

# Stratified split to maintain class balance
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✓ Training set: {len(X_train)} samples")
print(f"✓ Test set: {len(X_test)} samples")
print(f"\nClass distribution in train set:")
print(y_train.value_counts(normalize=True))

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert back to DataFrame for feature names
X_train_scaled = pd.DataFrame(X_train_scaled, columns=feature_cols, index=X_train.index)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=feature_cols, index=X_test.index)

print("✓ Features scaled using StandardScaler")

# ============================================================================
# 4. TRAIN MULTIPLE MODELS
# ============================================================================
print("\n[4] Training models...")

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced'),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', max_depth=10),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5, learning_rate=0.1)
}

results = {}
predictions = {}

for name, model in models.items():
    print(f"\n  Training {name}...")
    
    # Train model
    if name == 'Logistic Regression':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Cross-validation
    if name == 'Logistic Regression':
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
    else:
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
    
    # Calculate metrics
    auc = roc_auc_score(y_test, y_pred_proba)
    f1 = f1_score(y_test, y_pred)
    
    results[name] = {
        'model': model,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'auc': auc,
        'f1': f1,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }
    
    print(f"    ✓ AUC-ROC: {auc:.4f}")
    print(f"    ✓ F1-Score: {f1:.4f}")
    print(f"    ✓ CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# ============================================================================
# 5. MODEL COMPARISON
# ============================================================================
print("\n[5] Model comparison...")

comparison_df = pd.DataFrame({
    'Model': list(results.keys()),
    'AUC-ROC': [results[m]['auc'] for m in results.keys()],
    'F1-Score': [results[m]['f1'] for m in results.keys()],
    'CV AUC Mean': [results[m]['cv_mean'] for m in results.keys()],
    'CV AUC Std': [results[m]['cv_std'] for m in results.keys()]
}).sort_values('AUC-ROC', ascending=False)

print("\n" + "="*80)
print("MODEL PERFORMANCE COMPARISON")
print("="*80)
print(comparison_df.to_string(index=False))
print("="*80)

# Save comparison
comparison_df.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)

# Select best model
best_model_name = comparison_df.iloc[0]['Model']
best_model = results[best_model_name]['model']
print(f"\n🏆 Best Model: {best_model_name} (AUC: {comparison_df.iloc[0]['AUC-ROC']:.4f})")

# ============================================================================
# 6. FEATURE IMPORTANCE ANALYSIS
# ============================================================================
print("\n[6] Analyzing feature importance...")

# Get feature importance from best tree-based model
if best_model_name in ['Random Forest', 'Gradient Boosting']:
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
else:
    # Use Random Forest for feature importance
    rf_model = results['Random Forest']['model']
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print("-" * 60)
for idx, row in feature_importance.head(10).iterrows():
    print(f"  {row['feature']:<35} {row['importance']:.4f}")

# Save feature importance
feature_importance.to_csv(RESULTS_DIR / "feature_importance.csv", index=False)

# ============================================================================
# 7. DETAILED EVALUATION OF BEST MODEL
# ============================================================================
print("\n[7] Detailed evaluation of best model...")

y_pred_best = results[best_model_name]['y_pred']
y_pred_proba_best = results[best_model_name]['y_pred_proba']

# Classification report
print("\nClassification Report:")
print("-" * 60)
print(classification_report(y_test, y_pred_best, target_names=['No Promotion', 'Promotion']))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred_best)
print("\nConfusion Matrix:")
print(cm)

# Save predictions
predictions_df = pd.DataFrame({
    'actual': y_test.values,
    'predicted': y_pred_best,
    'probability': y_pred_proba_best
})
predictions_df.to_csv(RESULTS_DIR / "predictions.csv", index=False)

# ============================================================================
# 8. VISUALIZATIONS
# ============================================================================
print("\n[8] Creating visualizations...")

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Plot 1: Model Comparison
ax1 = fig.add_subplot(gs[0, :])
x_pos = np.arange(len(comparison_df))
ax1.bar(x_pos, comparison_df['AUC-ROC'], alpha=0.7, label='AUC-ROC', color='steelblue')
ax1.bar(x_pos + 0.25, comparison_df['F1-Score'], alpha=0.7, label='F1-Score', color='coral')
ax1.set_xlabel('Model', fontsize=11)
ax1.set_ylabel('Score', fontsize=11)
ax1.set_title('Model Performance Comparison', fontsize=13, fontweight='bold')
ax1.set_xticks(x_pos + 0.125)
ax1.set_xticklabels(comparison_df['Model'])
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Add value labels
for i, (auc, f1) in enumerate(zip(comparison_df['AUC-ROC'], comparison_df['F1-Score'])):
    ax1.text(i, auc + 0.01, f'{auc:.3f}', ha='center', va='bottom', fontsize=9)
    ax1.text(i + 0.25, f1 + 0.01, f'{f1:.3f}', ha='center', va='bottom', fontsize=9)

# Plot 2: Feature Importance
ax2 = fig.add_subplot(gs[1, :2])
top_features = feature_importance.head(15)
ax2.barh(range(len(top_features)), top_features['importance'], color='forestgreen', alpha=0.7)
ax2.set_yticks(range(len(top_features)))
ax2.set_yticklabels(top_features['feature'])
ax2.set_xlabel('Importance', fontsize=11)
ax2.set_title('Top 15 Feature Importance', fontsize=13, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)
ax2.invert_yaxis()

# Plot 3: ROC Curve
ax3 = fig.add_subplot(gs[1, 2])
for name, result in results.items():
    fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
    ax3.plot(fpr, tpr, label=f"{name} (AUC={result['auc']:.3f})", linewidth=2)
ax3.plot([0, 1], [0, 1], 'k--', label='Random', linewidth=1)
ax3.set_xlabel('False Positive Rate', fontsize=11)
ax3.set_ylabel('True Positive Rate', fontsize=11)
ax3.set_title('ROC Curves', fontsize=13, fontweight='bold')
ax3.legend(fontsize=9)
ax3.grid(alpha=0.3)

# Plot 4: Confusion Matrix
ax4 = fig.add_subplot(gs[2, 0])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax4,
            xticklabels=['No Promo', 'Promo'], yticklabels=['No Promo', 'Promo'])
ax4.set_xlabel('Predicted', fontsize=11)
ax4.set_ylabel('Actual', fontsize=11)
ax4.set_title(f'Confusion Matrix\n({best_model_name})', fontsize=12, fontweight='bold')

# Plot 5: Precision-Recall Curve
ax5 = fig.add_subplot(gs[2, 1])
precision, recall, _ = precision_recall_curve(y_test, y_pred_proba_best)
ax5.plot(recall, precision, linewidth=2, color='purple')
ax5.set_xlabel('Recall', fontsize=11)
ax5.set_ylabel('Precision', fontsize=11)
ax5.set_title(f'Precision-Recall Curve\n({best_model_name})', fontsize=12, fontweight='bold')
ax5.grid(alpha=0.3)

# Plot 6: Prediction Distribution
ax6 = fig.add_subplot(gs[2, 2])
ax6.hist(y_pred_proba_best[y_test == 0], bins=30, alpha=0.6, label='No Promotion', color='red')
ax6.hist(y_pred_proba_best[y_test == 1], bins=30, alpha=0.6, label='Promotion', color='green')
ax6.set_xlabel('Predicted Probability', fontsize=11)
ax6.set_ylabel('Frequency', fontsize=11)
ax6.set_title('Prediction Distribution', fontsize=12, fontweight='bold')
ax6.legend()
ax6.grid(alpha=0.3)

plt.suptitle('Promotion Prediction Model - Comprehensive Analysis', 
             fontsize=16, fontweight='bold', y=0.995)

viz_file = RESULTS_DIR / "promotion_prediction_analysis.png"
plt.savefig(viz_file, dpi=300, bbox_inches='tight')
print(f"✓ Visualization saved to: {viz_file}")

# ============================================================================
# 9. SAVE MODEL
# ============================================================================
print("\n[9] Saving model...")

import joblib

model_file = RESULTS_DIR / f"best_model_{best_model_name.replace(' ', '_').lower()}.pkl"
joblib.dump(best_model, model_file)
print(f"✓ Model saved to: {model_file}")

scaler_file = RESULTS_DIR / "scaler.pkl"
joblib.dump(scaler, scaler_file)
print(f"✓ Scaler saved to: {scaler_file}")

# ============================================================================
# 10. SUMMARY REPORT
# ============================================================================
print("\n" + "="*80)
print("PROMOTION PREDICTION MODEL - SUMMARY")
print("="*80)

print(f"\n📊 Dataset:")
print(f"   • Total Records: {len(df_clean):,}")
print(f"   • Training Set: {len(X_train):,} ({len(X_train)/len(df_clean)*100:.1f}%)")
print(f"   • Test Set: {len(X_test):,} ({len(X_test)/len(df_clean)*100:.1f}%)")
print(f"   • Features Used: {len(feature_cols)}")
print(f"   • Promotion Rate: {y.mean()*100:.2f}%")

print(f"\n🏆 Best Model: {best_model_name}")
print(f"   • AUC-ROC: {results[best_model_name]['auc']:.4f}")
print(f"   • F1-Score: {results[best_model_name]['f1']:.4f}")
print(f"   • CV AUC: {results[best_model_name]['cv_mean']:.4f} (+/- {results[best_model_name]['cv_std']:.4f})")

print(f"\n🎯 Top 5 Most Important Features:")
for idx, row in feature_importance.head(5).iterrows():
    print(f"   {idx+1}. {row['feature']}: {row['importance']:.4f}")

print(f"\n💡 Key Insights:")
if 'group_job_level' in feature_importance['feature'].values:
    job_level_importance = feature_importance[feature_importance['feature'] == 'group_job_level']['importance'].values[0]
    print(f"   • Job level importance: {job_level_importance:.4f}")
if 'level_name_encoded' in feature_importance['feature'].values:
    level_name_importance = feature_importance[feature_importance['feature'] == 'level_name_encoded']['importance'].values[0]
    print(f"   • Specific job level importance: {level_name_importance:.4f}")

print(f"\n✅ Model ready for:")
print(f"   1. Predicting promotion probability for employees")
print(f"   2. Identifying high-potential candidates")
print(f"   3. Succession planning recommendations")
print(f"   4. Performance gap analysis")

print("\n" + "="*80)
print("Analysis complete! Check results/promotion_prediction/ for outputs.")
print("="*80)
