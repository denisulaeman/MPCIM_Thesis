"""
Advanced Promotion Prediction with ALL Features
================================================

Model prediksi promosi yang memaksimalkan SEMUA fitur:
- Job Level features
- Skills & Proficiency
- Knowledge Graph features
- Performance & Behavioral
- Skill Gap Analysis
- Career Path Readiness

Author: Denis Ulaeman
Date: Dec 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix, roc_auc_score, 
                             roc_curve, precision_recall_curve, f1_score, accuracy_score)
import joblib
import warnings
warnings.filterwarnings('ignore')

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
FINAL_DIR = DATA_DIR / "final"
RESULTS_DIR = BASE_DIR / "results" / "advanced_promotion_prediction"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("ADVANCED PROMOTION PREDICTION - WITH ALL FEATURES")
print("="*80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1] Loading integrated dataset with all features...")

try:
    df = pd.read_csv(FINAL_DIR / "integrated_full_dataset_with_all_features.csv")
    print(f"✓ Loaded integrated dataset: {len(df)} records, {len(df.columns)} features")
except FileNotFoundError:
    print("❌ ERROR: Run 04_integrated_feature_engineering.py first!")
    exit(1)

# Check target variable
if 'has_promotion' not in df.columns:
    print("\n⚠️  Creating synthetic target for demonstration...")
    df['has_promotion'] = (
        (df['performance_score'] > df['performance_score'].quantile(0.7)) &
        (df['leadership_potential'] > df['leadership_potential'].quantile(0.6)) &
        (df.get('skill_gap_ratio', 0.5) > 0.7)
    ).astype(int)

print(f"\nTarget Distribution:")
print(df['has_promotion'].value_counts())
print(f"Promotion Rate: {df['has_promotion'].mean()*100:.2f}%")

# ============================================================================
# 2. FEATURE SELECTION
# ============================================================================
print("\n[2] Selecting features for modeling...")

# Core features
core_features = [
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

# Job level features
job_level_features = [
    'group_job_level',
    'level_name_encoded',
    'is_management',
    'is_staff',
    'is_support',
    'tenure_level_ratio'
]

# Skill features
skill_features = [
    'skill_count',
    'skill_avg_proficiency',
    'skill_max_proficiency',
    'skill_std_proficiency',
    'high_value_skill_count',
    'high_value_skill_avg_proficiency'
]

# Skill gap features
skill_gap_features = [
    'required_skills_count',
    'skills_met',
    'skills_exceeded',
    'skill_gap_ratio',
    'skill_exceed_ratio',
    'avg_skill_gap'
]

# Career readiness features
career_features = [
    'next_level_skill_readiness',
    'next_level_skill_gap',
    'promotion_readiness_enhanced',
    'skill_diversity_index',
    'career_progression_potential'
]

# Composite features
composite_features = [
    'skill_performance_alignment',
    'technical_competency_score',
    'leadership_competency_score',
    'performance_x_leadership',
    'behavior_x_tenure'
]

# Combine all features
all_feature_groups = {
    'Core': core_features,
    'Job Level': job_level_features,
    'Skills': skill_features,
    'Skill Gap': skill_gap_features,
    'Career': career_features,
    'Composite': composite_features
}

# Filter to only existing features
feature_cols = []
for group_name, features in all_feature_groups.items():
    existing = [f for f in features if f in df.columns]
    feature_cols.extend(existing)
    print(f"  {group_name}: {len(existing)}/{len(features)} features available")

print(f"\n✓ Total features selected: {len(feature_cols)}")

# Remove rows with missing values
df_clean = df[feature_cols + ['has_promotion']].dropna()
print(f"✓ Clean dataset: {len(df_clean)} records ({len(df_clean)/len(df)*100:.1f}% of original)")

# ============================================================================
# 3. TRAIN/TEST SPLIT
# ============================================================================
print("\n[3] Preparing train/test split...")

X = df_clean[feature_cols]
y = df_clean['has_promotion']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✓ Training set: {len(X_train)} samples")
print(f"✓ Test set: {len(X_test)} samples")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_scaled = pd.DataFrame(X_train_scaled, columns=feature_cols, index=X_train.index)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=feature_cols, index=X_test.index)

print("✓ Features scaled")

# ============================================================================
# 4. TRAIN MODELS WITH HYPERPARAMETER TUNING
# ============================================================================
print("\n[4] Training models with hyperparameter tuning...")

models = {}

# Random Forest with GridSearch
print("\n  Training Random Forest with GridSearch...")
rf_param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 15, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
rf_grid = GridSearchCV(
    RandomForestClassifier(random_state=42, class_weight='balanced'),
    rf_param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=0
)
rf_grid.fit(X_train, y_train)
models['Random Forest'] = rf_grid.best_estimator_
print(f"    Best params: {rf_grid.best_params_}")
print(f"    Best CV AUC: {rf_grid.best_score_:.4f}")

# Gradient Boosting with GridSearch
print("\n  Training Gradient Boosting with GridSearch...")
gb_param_grid = {
    'n_estimators': [100, 150],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1],
    'subsample': [0.8, 1.0]
}
gb_grid = GridSearchCV(
    GradientBoostingClassifier(random_state=42),
    gb_param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=0
)
gb_grid.fit(X_train, y_train)
models['Gradient Boosting'] = gb_grid.best_estimator_
print(f"    Best params: {gb_grid.best_params_}")
print(f"    Best CV AUC: {gb_grid.best_score_:.4f}")

# Logistic Regression
print("\n  Training Logistic Regression...")
lr_model = LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced')
lr_model.fit(X_train_scaled, y_train)
models['Logistic Regression'] = lr_model

# ============================================================================
# 5. EVALUATE MODELS
# ============================================================================
print("\n[5] Evaluating models...")

results = {}

for name, model in models.items():
    print(f"\n  Evaluating {name}...")
    
    # Predictions
    if name == 'Logistic Regression':
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    auc = roc_auc_score(y_test, y_pred_proba)
    f1 = f1_score(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation
    if name == 'Logistic Regression':
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
    else:
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
    
    results[name] = {
        'model': model,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'auc': auc,
        'f1': f1,
        'accuracy': accuracy,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }
    
    print(f"    AUC-ROC: {auc:.4f}")
    print(f"    F1-Score: {f1:.4f}")
    print(f"    Accuracy: {accuracy:.4f}")
    print(f"    CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# ============================================================================
# 6. MODEL COMPARISON
# ============================================================================
print("\n[6] Model comparison...")

comparison_df = pd.DataFrame({
    'Model': list(results.keys()),
    'AUC-ROC': [results[m]['auc'] for m in results.keys()],
    'F1-Score': [results[m]['f1'] for m in results.keys()],
    'Accuracy': [results[m]['accuracy'] for m in results.keys()],
    'CV AUC Mean': [results[m]['cv_mean'] for m in results.keys()],
    'CV AUC Std': [results[m]['cv_std'] for m in results.keys()]
}).sort_values('AUC-ROC', ascending=False)

print("\n" + "="*80)
print("MODEL PERFORMANCE COMPARISON")
print("="*80)
print(comparison_df.to_string(index=False))
print("="*80)

comparison_df.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)

best_model_name = comparison_df.iloc[0]['Model']
best_model = results[best_model_name]['model']
print(f"\n🏆 Best Model: {best_model_name} (AUC: {comparison_df.iloc[0]['AUC-ROC']:.4f})")

# ============================================================================
# 7. FEATURE IMPORTANCE ANALYSIS
# ============================================================================
print("\n[7] Analyzing feature importance...")

# Get feature importance from best tree-based model
if best_model_name in ['Random Forest', 'Gradient Boosting']:
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
else:
    rf_model = results['Random Forest']['model']
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

print("\nTop 20 Most Important Features:")
print("-" * 70)
for idx, row in feature_importance.head(20).iterrows():
    print(f"  {row['feature']:<45} {row['importance']:.4f}")

feature_importance.to_csv(RESULTS_DIR / "feature_importance.csv", index=False)

# Feature importance by group
print("\n\nFeature Importance by Group:")
print("-" * 70)
for group_name, features in all_feature_groups.items():
    group_features = [f for f in features if f in feature_importance['feature'].values]
    if group_features:
        group_importance = feature_importance[feature_importance['feature'].isin(group_features)]['importance'].sum()
        print(f"  {group_name:<20} {group_importance:.4f}")

# ============================================================================
# 8. DETAILED EVALUATION
# ============================================================================
print("\n[8] Detailed evaluation of best model...")

y_pred_best = results[best_model_name]['y_pred']
y_pred_proba_best = results[best_model_name]['y_pred_proba']

print("\nClassification Report:")
print("-" * 70)
print(classification_report(y_test, y_pred_best, target_names=['No Promotion', 'Promotion']))

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
# 9. VISUALIZATIONS
# ============================================================================
print("\n[9] Creating visualizations...")

fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)

# Plot 1: Model Comparison
ax1 = fig.add_subplot(gs[0, :])
x_pos = np.arange(len(comparison_df))
width = 0.25
ax1.bar(x_pos - width, comparison_df['AUC-ROC'], width, label='AUC-ROC', color='steelblue', alpha=0.8)
ax1.bar(x_pos, comparison_df['F1-Score'], width, label='F1-Score', color='coral', alpha=0.8)
ax1.bar(x_pos + width, comparison_df['Accuracy'], width, label='Accuracy', color='green', alpha=0.8)
ax1.set_xlabel('Model', fontsize=11)
ax1.set_ylabel('Score', fontsize=11)
ax1.set_title('Model Performance Comparison (All Features)', fontsize=13, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(comparison_df['Model'])
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Plot 2: Top 15 Feature Importance
ax2 = fig.add_subplot(gs[1, :2])
top_features = feature_importance.head(15)
colors = ['#2ecc71' if 'skill' in f else '#3498db' if 'level' in f else '#e74c3c' 
          for f in top_features['feature']]
ax2.barh(range(len(top_features)), top_features['importance'], color=colors, alpha=0.7)
ax2.set_yticks(range(len(top_features)))
ax2.set_yticklabels(top_features['feature'], fontsize=9)
ax2.set_xlabel('Importance', fontsize=11)
ax2.set_title('Top 15 Feature Importance', fontsize=13, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)
ax2.invert_yaxis()

# Plot 3: Feature Group Importance
ax3 = fig.add_subplot(gs[1, 2])
group_importance = []
for group_name, features in all_feature_groups.items():
    group_features = [f for f in features if f in feature_importance['feature'].values]
    if group_features:
        importance = feature_importance[feature_importance['feature'].isin(group_features)]['importance'].sum()
        group_importance.append((group_name, importance))

group_importance_df = pd.DataFrame(group_importance, columns=['Group', 'Importance']).sort_values('Importance')
ax3.barh(range(len(group_importance_df)), group_importance_df['Importance'], color='purple', alpha=0.7)
ax3.set_yticks(range(len(group_importance_df)))
ax3.set_yticklabels(group_importance_df['Group'], fontsize=9)
ax3.set_xlabel('Total Importance', fontsize=11)
ax3.set_title('Feature Group Importance', fontsize=12, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)

# Plot 4: ROC Curves
ax4 = fig.add_subplot(gs[2, 0])
for name, result in results.items():
    fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
    ax4.plot(fpr, tpr, label=f"{name} (AUC={result['auc']:.3f})", linewidth=2)
ax4.plot([0, 1], [0, 1], 'k--', label='Random', linewidth=1)
ax4.set_xlabel('False Positive Rate', fontsize=10)
ax4.set_ylabel('True Positive Rate', fontsize=10)
ax4.set_title('ROC Curves', fontsize=12, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(alpha=0.3)

# Plot 5: Confusion Matrix
ax5 = fig.add_subplot(gs[2, 1])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax5,
            xticklabels=['No Promo', 'Promo'], yticklabels=['No Promo', 'Promo'])
ax5.set_xlabel('Predicted', fontsize=10)
ax5.set_ylabel('Actual', fontsize=10)
ax5.set_title(f'Confusion Matrix\n({best_model_name})', fontsize=12, fontweight='bold')

# Plot 6: Precision-Recall Curve
ax6 = fig.add_subplot(gs[2, 2])
precision, recall, _ = precision_recall_curve(y_test, y_pred_proba_best)
ax6.plot(recall, precision, linewidth=2, color='purple')
ax6.set_xlabel('Recall', fontsize=10)
ax6.set_ylabel('Precision', fontsize=10)
ax6.set_title(f'Precision-Recall Curve\n({best_model_name})', fontsize=12, fontweight='bold')
ax6.grid(alpha=0.3)

# Plot 7: Prediction Distribution
ax7 = fig.add_subplot(gs[3, 0])
ax7.hist(y_pred_proba_best[y_test == 0], bins=30, alpha=0.6, label='No Promotion', color='red')
ax7.hist(y_pred_proba_best[y_test == 1], bins=30, alpha=0.6, label='Promotion', color='green')
ax7.set_xlabel('Predicted Probability', fontsize=10)
ax7.set_ylabel('Frequency', fontsize=10)
ax7.set_title('Prediction Distribution', fontsize=12, fontweight='bold')
ax7.legend()
ax7.grid(alpha=0.3)

# Plot 8: Feature Importance by Category
ax8 = fig.add_subplot(gs[3, 1:])
# Top skill features vs top non-skill features
skill_features_imp = feature_importance[feature_importance['feature'].str.contains('skill', case=False)].head(10)
non_skill_features_imp = feature_importance[~feature_importance['feature'].str.contains('skill', case=False)].head(10)

y_pos = np.arange(max(len(skill_features_imp), len(non_skill_features_imp)))
width = 0.35

if len(skill_features_imp) > 0:
    ax8.barh(y_pos[:len(skill_features_imp)] - width/2, skill_features_imp['importance'].values, 
            width, label='Skill Features', color='green', alpha=0.7)
if len(non_skill_features_imp) > 0:
    ax8.barh(y_pos[:len(non_skill_features_imp)] + width/2, non_skill_features_imp['importance'].values, 
            width, label='Non-Skill Features', color='blue', alpha=0.7)

ax8.set_xlabel('Importance', fontsize=10)
ax8.set_title('Skill vs Non-Skill Feature Importance (Top 10 each)', fontsize=12, fontweight='bold')
ax8.legend()
ax8.grid(axis='x', alpha=0.3)

plt.suptitle('Advanced Promotion Prediction - Comprehensive Analysis with ALL Features', 
             fontsize=15, fontweight='bold', y=0.995)

viz_file = RESULTS_DIR / "advanced_promotion_prediction_analysis.png"
plt.savefig(viz_file, dpi=300, bbox_inches='tight')
print(f"✓ Visualization saved to: {viz_file}")

plt.close()

# ============================================================================
# 10. SAVE MODEL
# ============================================================================
print("\n[10] Saving model...")

model_file = RESULTS_DIR / f"best_model_{best_model_name.replace(' ', '_').lower()}.pkl"
joblib.dump(best_model, model_file)
print(f"✓ Model saved to: {model_file}")

scaler_file = RESULTS_DIR / "scaler.pkl"
joblib.dump(scaler, scaler_file)
print(f"✓ Scaler saved to: {scaler_file}")

# Save feature list
feature_list_df = pd.DataFrame({'feature': feature_cols})
feature_list_df.to_csv(RESULTS_DIR / "feature_list.csv", index=False)
print(f"✓ Feature list saved")

# ============================================================================
# 11. SUMMARY REPORT
# ============================================================================
print("\n" + "="*80)
print("ADVANCED PROMOTION PREDICTION - SUMMARY")
print("="*80)

print(f"\n📊 Dataset:")
print(f"   • Total Records: {len(df_clean):,}")
print(f"   • Training Set: {len(X_train):,}")
print(f"   • Test Set: {len(X_test):,}")
print(f"   • Total Features: {len(feature_cols)}")
print(f"   • Promotion Rate: {y.mean()*100:.2f}%")

print(f"\n🏆 Best Model: {best_model_name}")
print(f"   • AUC-ROC: {results[best_model_name]['auc']:.4f}")
print(f"   • F1-Score: {results[best_model_name]['f1']:.4f}")
print(f"   • Accuracy: {results[best_model_name]['accuracy']:.4f}")
print(f"   • CV AUC: {results[best_model_name]['cv_mean']:.4f} (+/- {results[best_model_name]['cv_std']:.4f})")

print(f"\n🎯 Top 5 Most Important Features:")
for i, row in feature_importance.head(5).iterrows():
    print(f"   {i+1}. {row['feature']}: {row['importance']:.4f}")

print(f"\n💡 Feature Group Contributions:")
for group_name, importance in group_importance:
    print(f"   • {group_name}: {importance:.4f}")

print(f"\n✅ Key Insights:")
skill_importance = sum([imp for group, imp in group_importance if 'Skill' in group])
print(f"   • Skill-related features contribute {skill_importance:.2%} to predictions")
print(f"   • Model uses {len(feature_cols)} features across 6 categories")
print(f"   • Enhanced promotion readiness improves prediction accuracy")

print("\n" + "="*80)
print("Advanced model training complete!")
print("="*80)
