
# SHAP ANALYSIS SUMMARY REPORT
Generated: 2025-11-24 21:15:32

## Model Analyzed
- Model: XGBoost
- Test Samples: 143
- Features: 14

## Top 10 Most Important Features (by Mean |SHAP|)
1. tenure_years: 2.3321
2. tenure_category_encoded: 1.5689
3. behavior_avg: 0.4144
4. performance_rating_encoded: 0.3244
5. combined_score: 0.2964
6. perf_beh_ratio: 0.2381
7. marital_status_encoded: 0.2208
8. performance_score: 0.1295
9. performance_level_encoded: 0.1237
10. behavioral_level_encoded: 0.1169

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
- No Quick Assessment features found in current dataset
- Model uses Performance and Behavioral dimensions only

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
