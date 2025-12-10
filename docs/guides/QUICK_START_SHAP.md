# 🚀 Quick Start: SHAP Analysis

## ⚡ 5-Minute Guide to Model Explainability

### What is SHAP?

**SHAP (SHapley Additive exPlanations)** memberikan penjelasan untuk setiap prediksi model ML dengan menghitung kontribusi masing-masing fitur.

**Key Concepts**:
- ✅ **Positive SHAP value**: Fitur meningkatkan probabilitas promosi
- ✅ **Negative SHAP value**: Fitur menurunkan probabilitas promosi
- ✅ **Magnitude**: Seberapa besar pengaruh fitur

---

## 🎯 Running SHAP Analysis

### Prerequisites

Pastikan models sudah dilatih:
```bash
# Check if models exist
ls -lh results/advanced_models/*.pkl
ls -lh models/*.pkl
```

### Run Analysis

```bash
cd /Users/denisulaeman/Workspace/Academic/CascadeProjects/MPCIM_Thesis
python scripts/analysis/13_shap_analysis.py
```

**Expected Output**:
- 9 visualization PNG files (300 DPI)
- SHAP values saved (`.npy`)
- SHAP explainer (`.pkl`)
- Feature importance comparison (`.csv`)
- Summary report (`.md`)

**Duration**: ~2-3 minutes

---

## 📊 Generated Visualizations

### 1. Global Importance
- `01_shap_summary_plot.png` - Distribusi SHAP values per fitur
- `02_shap_bar_plot.png` - Mean absolute SHAP values

### 2. Individual Explanations
- `03_waterfall_promoted.png` - Case: High confidence promoted
- `04_waterfall_not_promoted.png` - Case: High confidence not promoted
- `05_waterfall_borderline.png` - Case: Borderline decision

### 3. Feature Interactions
- `06_dependence_1_tenure_years.png` - Tenure interaction
- `06_dependence_2_tenure_category_encoded.png` - Tenure category
- `06_dependence_3_behavior_avg.png` - Behavioral score

### 4. Comparison
- `09_importance_comparison.png` - Native vs SHAP importance

---

## 🖥️ View in Dashboard

### Start Streamlit
```bash
streamlit run app/Home.py
```

### Navigate to SHAP Page
1. Open browser: `http://localhost:8501`
2. Click **🔍 SHAP Explainability** in sidebar
3. Explore 5 tabs:
   - 📊 Global Importance
   - 💧 Individual Explanations
   - 🔗 Feature Interactions
   - 📈 Importance Comparison
   - 📄 Summary Report

---

## 📖 Understanding SHAP Plots

### Summary Plot (Beeswarm)
- **X-axis**: SHAP value (impact on prediction)
- **Y-axis**: Features (sorted by importance)
- **Color**: Feature value (red = high, blue = low)
- **Interpretation**: 
  - Features at top = most important
  - Spread shows variability of impact
  - Color pattern shows relationship direction

### Waterfall Plot
- **Shows**: How prediction differs from base value
- **Red bars**: Push prediction higher (promote)
- **Blue bars**: Push prediction lower (not promote)
- **Interpretation**: 
  - Start from base value (average)
  - Each bar adds/subtracts to final prediction
  - Final value = predicted probability

### Dependence Plot
- **X-axis**: Feature value
- **Y-axis**: SHAP value for that feature
- **Color**: Another feature (interaction)
- **Interpretation**:
  - Shows non-linear relationships
  - Color reveals interactions
  - Trend shows how feature affects prediction

---

## 💡 Key Findings from SHAP

### Top 5 Most Important Features
1. **tenure_years** (40-50%)
2. **tenure_category_encoded** (8-12%)
3. **behavior_avg** (4-6%)
4. **performance_rating_encoded** (3-5%)
5. **combined_score** (3-4%)

### Insights
- ✅ Tenure dominates predictions
- ✅ Behavioral score is statistically significant
- ✅ Performance contributes in combination
- ✅ Engineered features add value

---

## 🎓 Using SHAP in Thesis

### Chapter 4: Results
Include:
- Summary plot (global importance)
- Feature importance table
- Top 3 dependence plots

### Chapter 5: Discussion
Include:
- Waterfall plot examples (2-3 cases)
- Interpretation of feature contributions
- Comparison with literature

### Appendix
Include:
- All 9 SHAP visualizations
- Detailed feature importance tables
- SHAP analysis report

---

## 🔧 Troubleshooting

### Error: Module 'shap' not found
```bash
pip install shap
```

### Error: Models not found
Train models first:
```bash
python scripts/modeling/04_advanced_models.py
```

### Error: Data not found
Check processed data exists:
```bash
ls -lh data/processed/
```

### Visualizations not showing in dashboard
Verify files exist:
```bash
ls -lh results/shap_analysis/
```

---

## 📁 Output Location

All SHAP results saved to:
```
results/shap_analysis/
├── 01_shap_summary_plot.png
├── 02_shap_bar_plot.png
├── 03_waterfall_promoted.png
├── 04_waterfall_not_promoted.png
├── 05_waterfall_borderline.png
├── 06_dependence_1_tenure_years.png
├── 06_dependence_2_tenure_category_encoded.png
├── 06_dependence_3_behavior_avg.png
├── 09_importance_comparison.png
├── shap_values.npy
├── shap_explainer.pkl
├── feature_importance_comparison.csv
├── feature_names.txt
└── SHAP_ANALYSIS_REPORT.md
```

---

## 🚀 Next Steps

1. ✅ Review all visualizations
2. ✅ Select best plots for thesis
3. ✅ Write interpretation in Discussion chapter
4. ✅ Use waterfall plots to explain specific predictions
5. ✅ Include in defense presentation

---

## 📚 References

- **SHAP Paper**: Lundberg & Lee (2017). "A Unified Approach to Interpreting Model Predictions"
- **SHAP GitHub**: https://github.com/slundberg/shap
- **Documentation**: https://shap.readthedocs.io/

---

**Last Updated**: November 24, 2025  
**Status**: ✅ SHAP Analysis Complete  
**Quality**: 🌟 Publication-Ready
