"""
MPCIM Thesis - SHAP (SHapley Additive exPlanations) Analysis
Author: Deni Sulaeman
Date: November 22, 2025

Comprehensive model interpretability using SHAP values.
This provides explainability for ML predictions - crucial for thesis.

SHAP Visualizations:
1. Summary Plot - Global feature importance
2. Waterfall Plot - Individual prediction explanation
3. Force Plot - Feature contributions
4. Dependence Plot - Feature interactions
5. Bar Plot - Mean absolute SHAP values
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11

print('='*80)
print('MPCIM THESIS - SHAP ANALYSIS FOR MODEL INTERPRETABILITY')
print('='*80)
print()

# ============================================================================
# 1. SETUP & LOAD DATA
# ============================================================================

print('1. LOADING DATA & MODELS')
print('-'*80)

# Paths
repo_root = Path(__file__).resolve().parents[2]
data_dir = repo_root / 'data' / 'processed'
models_dir = repo_root / 'models'
results_dir = repo_root / 'results'
output_dir = results_dir / 'shap_analysis'
output_dir.mkdir(parents=True, exist_ok=True)

# Load test data
X_test = pd.read_csv(data_dir / 'X_test.csv')
y_test = pd.read_csv(data_dir / 'y_test.csv')['has_promotion']

# Load training data (for background distribution)
X_train = pd.read_csv(data_dir / 'X_train_balanced.csv')
y_train = pd.read_csv(data_dir / 'y_train_balanced.csv')['has_promotion']

print(f'✅ Data loaded successfully')
print(f'   Training set: {len(X_train):,} samples')
print(f'   Test set: {len(X_test):,} samples')
print(f'   Features: {len(X_test.columns)}')
print()

# ============================================================================
# 2. LOAD MODELS
# ============================================================================

print('2. LOADING TRAINED MODELS')
print('-'*80)

models = {}
model_paths = {
    'XGBoost': results_dir / 'advanced_models' / 'xgboost_model.pkl',
    'Random Forest': results_dir / 'advanced_models' / 'random_forest_model.pkl',
    'Neural Network': models_dir / 'neural_network_model.pkl',
}

for name, path in model_paths.items():
    if path.exists():
        models[name] = joblib.load(path)
        print(f'✅ Loaded: {name}')
    else:
        print(f'⚠️  Not found: {name}')

if not models:
    print('❌ No models found! Please train models first.')
    exit(1)

print()

# ============================================================================
# 3. SHAP ANALYSIS - XGBOOST (PRIMARY MODEL)
# ============================================================================

print('3. SHAP ANALYSIS - XGBOOST MODEL')
print('-'*80)

if 'XGBoost' in models:
    model = models['XGBoost']
    model_name = 'XGBoost'
elif 'Random Forest' in models:
    model = models['Random Forest']
    model_name = 'Random Forest'
else:
    model = list(models.values())[0]
    model_name = list(models.keys())[0]

print(f'Analyzing: {model_name}')
print()

# Create SHAP explainer
print('Creating SHAP explainer...')
if model_name in ['XGBoost', 'Random Forest']:
    # Tree-based explainer (fast and exact)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # For binary classification, shap_values might be 2D or 3D
    if isinstance(shap_values, list):
        shap_values = shap_values[1]  # Positive class
else:
    # Kernel explainer (model-agnostic, slower)
    # Use a sample of training data as background
    background = shap.sample(X_train, 100)
    explainer = shap.KernelExplainer(model.predict_proba, background)
    shap_values = explainer.shap_values(X_test)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

print(f'✅ SHAP values computed')
print(f'   Shape: {shap_values.shape}')
print()

# ============================================================================
# 4. VISUALIZATION 1: SUMMARY PLOT (GLOBAL IMPORTANCE)
# ============================================================================

print('4. GENERATING SUMMARY PLOT (Global Feature Importance)')
print('-'*80)

plt.figure(figsize=(12, 10))
shap.summary_plot(shap_values, X_test, show=False, max_display=20)
plt.title(f'SHAP Summary Plot - {model_name}\nGlobal Feature Importance', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('SHAP Value (impact on model output)', fontsize=12)
plt.tight_layout()
plt.savefig(output_dir / '01_shap_summary_plot.png', dpi=300, bbox_inches='tight')
print(f'✅ Saved: 01_shap_summary_plot.png')
plt.close()

# ============================================================================
# 5. VISUALIZATION 2: BAR PLOT (MEAN ABSOLUTE SHAP)
# ============================================================================

print('5. GENERATING BAR PLOT (Mean Absolute SHAP Values)')
print('-'*80)

plt.figure(figsize=(12, 10))
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False, max_display=20)
plt.title(f'SHAP Bar Plot - {model_name}\nMean Absolute SHAP Values', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Mean |SHAP Value|', fontsize=12)
plt.tight_layout()
plt.savefig(output_dir / '02_shap_bar_plot.png', dpi=300, bbox_inches='tight')
print(f'✅ Saved: 02_shap_bar_plot.png')
plt.close()

# ============================================================================
# 6. VISUALIZATION 3: WATERFALL PLOTS (INDIVIDUAL PREDICTIONS)
# ============================================================================

print('6. GENERATING WATERFALL PLOTS (Individual Predictions)')
print('-'*80)

# Select interesting cases
promoted_indices = np.where(y_test == 1)[0]
not_promoted_indices = np.where(y_test == 0)[0]

# Get predictions
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Case 1: High confidence PROMOTED (True Positive)
tp_indices = promoted_indices[y_pred_proba[promoted_indices] > 0.8]
if len(tp_indices) > 0:
    idx = tp_indices[0]
    
    plt.figure(figsize=(12, 8))
    shap.waterfall_plot(
        shap.Explanation(
            values=shap_values[idx],
            base_values=explainer.expected_value if hasattr(explainer, 'expected_value') else shap_values.mean(),
            data=X_test.iloc[idx],
            feature_names=X_test.columns.tolist()
        ),
        show=False
    )
    plt.title(f'SHAP Waterfall Plot - Case 1: High Confidence PROMOTED\n'
              f'Actual: PROMOTED | Predicted Probability: {y_pred_proba[idx]:.2%}',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / '03_waterfall_promoted.png', dpi=300, bbox_inches='tight')
    print(f'✅ Saved: 03_waterfall_promoted.png (Case: High confidence PROMOTED)')
    plt.close()

# Case 2: High confidence NOT PROMOTED (True Negative)
tn_indices = not_promoted_indices[y_pred_proba[not_promoted_indices] < 0.3]
if len(tn_indices) > 0:
    idx = tn_indices[0]
    
    plt.figure(figsize=(12, 8))
    shap.waterfall_plot(
        shap.Explanation(
            values=shap_values[idx],
            base_values=explainer.expected_value if hasattr(explainer, 'expected_value') else shap_values.mean(),
            data=X_test.iloc[idx],
            feature_names=X_test.columns.tolist()
        ),
        show=False
    )
    plt.title(f'SHAP Waterfall Plot - Case 2: High Confidence NOT PROMOTED\n'
              f'Actual: NOT PROMOTED | Predicted Probability: {y_pred_proba[idx]:.2%}',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / '04_waterfall_not_promoted.png', dpi=300, bbox_inches='tight')
    print(f'✅ Saved: 04_waterfall_not_promoted.png (Case: High confidence NOT PROMOTED)')
    plt.close()

# Case 3: Borderline case (near threshold)
borderline_indices = np.where((y_pred_proba > 0.65) & (y_pred_proba < 0.75))[0]
if len(borderline_indices) > 0:
    idx = borderline_indices[0]
    
    plt.figure(figsize=(12, 8))
    shap.waterfall_plot(
        shap.Explanation(
            values=shap_values[idx],
            base_values=explainer.expected_value if hasattr(explainer, 'expected_value') else shap_values.mean(),
            data=X_test.iloc[idx],
            feature_names=X_test.columns.tolist()
        ),
        show=False
    )
    actual_label = "PROMOTED" if y_test.iloc[idx] == 1 else "NOT PROMOTED"
    plt.title(f'SHAP Waterfall Plot - Case 3: Borderline Case\n'
              f'Actual: {actual_label} | Predicted Probability: {y_pred_proba[idx]:.2%}',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / '05_waterfall_borderline.png', dpi=300, bbox_inches='tight')
    print(f'✅ Saved: 05_waterfall_borderline.png (Case: Borderline)')
    plt.close()

print()

# ============================================================================
# 7. VISUALIZATION 4: DEPENDENCE PLOTS (FEATURE INTERACTIONS)
# ============================================================================

print('7. GENERATING DEPENDENCE PLOTS (Feature Interactions)')
print('-'*80)

# Top features to analyze
feature_importance = np.abs(shap_values).mean(axis=0)
top_features_idx = np.argsort(feature_importance)[-5:][::-1]
top_features = X_test.columns[top_features_idx].tolist()

print(f'Top 5 features: {top_features}')
print()

# Create dependence plots for top 3 features
for i, feature in enumerate(top_features[:3], 1):
    plt.figure(figsize=(10, 6))
    shap.dependence_plot(
        feature, 
        shap_values, 
        X_test,
        show=False
    )
    plt.title(f'SHAP Dependence Plot - {feature}\nHow {feature} affects predictions',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / f'06_dependence_{i}_{feature.replace("/", "_")}.png', 
                dpi=300, bbox_inches='tight')
    print(f'✅ Saved: 06_dependence_{i}_{feature}.png')
    plt.close()

print()

# ============================================================================
# 8. QUICK ASSESSMENT CONTRIBUTION ANALYSIS
# ============================================================================

print('8. QUICK ASSESSMENT CONTRIBUTION ANALYSIS')
print('-'*80)

# Identify QA features
qa_keywords = ['psychological', 'drive', 'mental', 'adaptability', 
               'collaboration', 'leadership', 'holistic', 'alignment', 'quick_assessment']

qa_features = [col for col in X_test.columns 
               if any(keyword in col.lower() for keyword in qa_keywords)]

print(f'Quick Assessment features found: {len(qa_features)}')
print(f'Features: {qa_features}')
print()

if qa_features:
    # Calculate QA contribution
    qa_indices = [X_test.columns.get_loc(f) for f in qa_features]
    qa_shap_values = shap_values[:, qa_indices]
    
    qa_importance = np.abs(qa_shap_values).mean(axis=0)
    total_importance = np.abs(shap_values).mean(axis=0).sum()
    qa_total_importance = qa_importance.sum()
    qa_contribution_pct = (qa_total_importance / total_importance) * 100
    
    print(f'📊 QA Features Contribution: {qa_contribution_pct:.2f}%')
    print()
    
    # Create QA-specific summary plot
    plt.figure(figsize=(12, 8))
    shap.summary_plot(qa_shap_values, X_test[qa_features], show=False)
    plt.title(f'SHAP Summary - Quick Assessment Features Only\n'
              f'Total Contribution: {qa_contribution_pct:.2f}%',
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / '07_shap_qa_features.png', dpi=300, bbox_inches='tight')
    print(f'✅ Saved: 07_shap_qa_features.png')
    plt.close()
    
    # QA bar plot
    plt.figure(figsize=(10, 6))
    qa_importance_df = pd.DataFrame({
        'Feature': qa_features,
        'Mean |SHAP|': qa_importance
    }).sort_values('Mean |SHAP|', ascending=True)
    
    plt.barh(qa_importance_df['Feature'], qa_importance_df['Mean |SHAP|'], color='steelblue')
    plt.xlabel('Mean |SHAP Value|', fontsize=12)
    plt.title(f'Quick Assessment Features - Mean Absolute SHAP Values\n'
              f'Total Contribution: {qa_contribution_pct:.2f}%',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / '08_qa_importance_bar.png', dpi=300, bbox_inches='tight')
    print(f'✅ Saved: 08_qa_importance_bar.png')
    plt.close()

print()

# ============================================================================
# 9. FEATURE IMPORTANCE COMPARISON
# ============================================================================

print('9. FEATURE IMPORTANCE COMPARISON (Traditional vs SHAP)')
print('-'*80)

# Get model's native feature importance
if hasattr(model, 'feature_importances_'):
    native_importance = model.feature_importances_
    
    # Create comparison dataframe
    comparison_df = pd.DataFrame({
        'Feature': X_test.columns,
        'Native Importance': native_importance,
        'SHAP Importance': np.abs(shap_values).mean(axis=0)
    })
    
    # Normalize for comparison
    comparison_df['Native Importance (Normalized)'] = (
        comparison_df['Native Importance'] / comparison_df['Native Importance'].sum()
    )
    comparison_df['SHAP Importance (Normalized)'] = (
        comparison_df['SHAP Importance'] / comparison_df['SHAP Importance'].sum()
    )
    
    # Sort by SHAP importance
    comparison_df = comparison_df.sort_values('SHAP Importance', ascending=False)
    
    # Plot top 15
    top_15 = comparison_df.head(15)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Native importance
    ax1.barh(top_15['Feature'], top_15['Native Importance (Normalized)'], color='coral')
    ax1.set_xlabel('Normalized Importance', fontsize=12)
    ax1.set_title('Native Feature Importance (from model)', fontsize=14, fontweight='bold')
    ax1.invert_yaxis()
    
    # SHAP importance
    ax2.barh(top_15['Feature'], top_15['SHAP Importance (Normalized)'], color='steelblue')
    ax2.set_xlabel('Normalized Importance', fontsize=12)
    ax2.set_title('SHAP Feature Importance (from predictions)', fontsize=14, fontweight='bold')
    ax2.invert_yaxis()
    
    plt.suptitle('Feature Importance Comparison: Native vs SHAP\nTop 15 Features',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / '09_importance_comparison.png', dpi=300, bbox_inches='tight')
    print(f'✅ Saved: 09_importance_comparison.png')
    plt.close()
    
    # Save comparison table
    comparison_df.to_csv(output_dir / 'feature_importance_comparison.csv', index=False)
    print(f'✅ Saved: feature_importance_comparison.csv')

print()

# ============================================================================
# 10. SAVE SHAP VALUES FOR LATER USE
# ============================================================================

print('10. SAVING SHAP VALUES & EXPLAINER')
print('-'*80)

# Save SHAP values
np.save(output_dir / 'shap_values.npy', shap_values)
print(f'✅ Saved: shap_values.npy')

# Save explainer (for use in Streamlit app)
joblib.dump(explainer, output_dir / 'shap_explainer.pkl')
print(f'✅ Saved: shap_explainer.pkl')

# Save feature names
with open(output_dir / 'feature_names.txt', 'w') as f:
    f.write('\n'.join(X_test.columns.tolist()))
print(f'✅ Saved: feature_names.txt')

print()

# ============================================================================
# 11. GENERATE SUMMARY REPORT
# ============================================================================

print('11. GENERATING SUMMARY REPORT')
print('-'*80)

report = f"""
# SHAP ANALYSIS SUMMARY REPORT
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Model Analyzed
- Model: {model_name}
- Test Samples: {len(X_test):,}
- Features: {len(X_test.columns)}

## Top 10 Most Important Features (by Mean |SHAP|)
"""

# Top 10 features
top_10_importance = np.abs(shap_values).mean(axis=0)
top_10_idx = np.argsort(top_10_importance)[-10:][::-1]

for rank, idx in enumerate(top_10_idx, 1):
    feature = X_test.columns[idx]
    importance = top_10_importance[idx]
    report += f"{rank}. {feature}: {importance:.4f}\n"

# QA contribution
if qa_features:
    report += f"""
## Quick Assessment Contribution
- QA Features: {len(qa_features)}
- Total Contribution: {qa_contribution_pct:.2f}%
- Top QA Feature: {qa_features[np.argmax(qa_importance)]}

### QA Features Ranking:
"""
    qa_ranking = sorted(zip(qa_features, qa_importance), key=lambda x: x[1], reverse=True)
    for rank, (feature, importance) in enumerate(qa_ranking, 1):
        report += f"{rank}. {feature}: {importance:.4f}\n"
    qa_contrib_text = f"- QA features contribute {qa_contribution_pct:.2f}% to model predictions\n- This validates the 3-dimensional approach (Performance + Behavioral + Psychological)"
else:
    qa_contrib_text = "- No Quick Assessment features found in current dataset\n- Model uses Performance and Behavioral dimensions only"

report += f"""
## Visualizations Generated
1. 01_shap_summary_plot.png - Global feature importance
2. 02_shap_bar_plot.png - Mean absolute SHAP values
3. 03_waterfall_promoted.png - Individual case (promoted)
4. 04_waterfall_not_promoted.png - Individual case (not promoted)
5. 05_waterfall_borderline.png - Borderline case
6. 06_dependence_*.png - Feature interaction plots
7. 07_shap_qa_features.png - QA features summary (if applicable)
8. 08_qa_importance_bar.png - QA features bar plot (if applicable)
9. 09_importance_comparison.png - Native vs SHAP comparison

## Key Insights for Thesis

### 1. Model Interpretability
- SHAP values provide feature-level explanations for each prediction
- Positive SHAP = increases promotion probability
- Negative SHAP = decreases promotion probability

### 2. Quick Assessment Value
{qa_contrib_text}

### 3. Feature Interactions
- Dependence plots show non-linear relationships
- Some features have interaction effects (shown by color coding in dependence plots)

## Usage in Thesis

### Chapter 4: Results
- Include summary plot (Figure X.X)
- Include QA contribution analysis (Figure X.X)
- Include feature importance comparison table

### Chapter 5: Discussion
- Use waterfall plots to explain specific predictions
- Discuss feature interactions from dependence plots
- Highlight QA contribution as key finding

### Appendix
- Include all SHAP visualizations
- Include detailed feature importance tables
"""

# Save report
with open(output_dir / 'SHAP_ANALYSIS_REPORT.md', 'w') as f:
    f.write(report)

print(f'✅ Saved: SHAP_ANALYSIS_REPORT.md')
print()

# ============================================================================
# COMPLETION
# ============================================================================

print('='*80)
print('✅ SHAP ANALYSIS COMPLETE!')
print('='*80)
print()
print(f'📁 Output directory: {output_dir}')
print()
print('📊 Generated Files:')
print('   - 9 visualization PNG files')
print('   - shap_values.npy (for later use)')
print('   - shap_explainer.pkl (for Streamlit integration)')
print('   - feature_importance_comparison.csv')
print('   - SHAP_ANALYSIS_REPORT.md')
print()
print('💡 Next Steps:')
print('   1. Review all visualizations')
print('   2. Include key plots in thesis')
print('   3. Use waterfall plots to explain predictions')
print('   4. Integrate SHAP into Streamlit app (optional)')
print()
print('📚 For Thesis:')
print('   - Summary plot → Chapter 4 (Results)')
print('   - QA contribution → Chapter 4 (Key Finding)')
print('   - Waterfall plots → Chapter 5 (Discussion)')
print('   - Dependence plots → Appendix')
