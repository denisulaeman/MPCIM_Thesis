# 📓 Google Colab Guide - MPCIM Thesis

## 🎯 Overview

File Jupyter Notebook telah dibuat untuk menjalankan analisis MPCIM Thesis di Google Colab!

**File**: `MPCIM_Thesis_Colab.ipynb`

---

## 🚀 Cara Menggunakan di Google Colab

### Step 1: Upload Notebook ke Google Colab

#### Option A: Upload Langsung
1. Buka [Google Colab](https://colab.research.google.com/)
2. Klik **File** → **Upload notebook**
3. Pilih file `MPCIM_Thesis_Colab.ipynb`
4. Notebook akan terbuka di Colab

#### Option B: Via Google Drive
1. Upload file `MPCIM_Thesis_Colab.ipynb` ke Google Drive Anda
2. Klik kanan file → **Open with** → **Google Colaboratory**
3. Notebook akan terbuka di Colab

---

### Step 2: Upload Dataset

Notebook akan meminta Anda untuk upload file CSV. Anda bisa menggunakan salah satu dari:

#### Recommended Dataset:
- **`sample_dataset_100_balanced.csv`** (Demo, 70% promoted)
  - Location: `data/final/sample_dataset_100_balanced.csv`
  - Size: ~17 KB
  - Perfect untuk demo dan testing

#### Alternative Dataset:
- **`integrated_full_dataset.csv`** (Full data, 712 rows)
  - Location: `data/final/integrated_performance_behavioral.csv`
  - Size: ~68 KB
  - Real imbalanced data (9.3% promoted)

---

### Step 3: Run Notebook

Jalankan cell secara berurutan:

1. **Cell 1**: Install packages (tunggu ~30 detik)
2. **Cell 2**: Import libraries
3. **Cell 3**: Upload dataset (klik tombol upload)
4. **Cell 4**: Load & explore data
5. **Cell 5**: Data preparation (SMOTE + scaling)
6. **Cell 6**: Model training (Random Forest)
7. **Cell 7**: Feature importance visualization

**Tip**: Gunakan **Runtime** → **Run all** untuk menjalankan semua cell sekaligus

---

## 📊 What's Included in the Notebook

### 1. Setup & Installation
- Automatic installation of required packages:
  - pandas, numpy, matplotlib, seaborn, plotly
  - scikit-learn, xgboost, shap
  - imbalanced-learn (SMOTE)

### 2. Data Upload & Exploration
- Upload CSV file from your computer
- Display first 5 rows
- Show basic statistics
- Data types and shape

### 3. Data Preparation
- Handle missing values
- Encode categorical variables
- Train-test split (80-20)
- SMOTE for handling imbalanced data
- Feature scaling (StandardScaler)

### 4. Model Training
- Random Forest Classifier (100 trees)
- Evaluation metrics:
  - Accuracy
  - Precision
  - Recall
  - F1-Score
  - ROC-AUC

### 5. Feature Importance
- Top 10 most important features
- Horizontal bar chart visualization

---

## 🎓 For Thesis Defense

### Quick Demo Steps:

1. **Open Colab**: Show the notebook interface
2. **Run Setup**: Execute installation cell
3. **Upload Data**: Use `sample_dataset_100_balanced.csv`
4. **Show Results**: 
   - Data exploration output
   - Model performance metrics
   - Feature importance chart

### Key Points to Highlight:

✅ **Cloud-Based**: No local installation needed  
✅ **Reproducible**: Anyone can run the analysis  
✅ **Interactive**: Real-time execution and visualization  
✅ **Professional**: Clean code with proper documentation  

---

## 📁 Files You Need

### Required Files:
1. **`MPCIM_Thesis_Colab.ipynb`** - The Jupyter notebook
2. **Dataset CSV** - One of these:
   - `sample_dataset_100_balanced.csv` (recommended)
   - `integrated_performance_behavioral.csv` (full data)

### Optional Files:
- `sample_dataset_1000_balanced.csv` - Larger balanced dataset
- `UPLOAD_TEMPLATE.csv` - Template for custom data

---

## 🔧 Troubleshooting

### Issue 1: Package Installation Fails
**Solution**: Run the installation cell again
```python
!pip install --upgrade pip
!pip install -q pandas numpy matplotlib seaborn scikit-learn xgboost shap imbalanced-learn
```

### Issue 2: File Upload Timeout
**Solution**: 
- Use smaller dataset (sample_dataset_100_balanced.csv)
- Or mount Google Drive and load from there:
```python
from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv('/content/drive/MyDrive/your_file.csv')
```

### Issue 3: Out of Memory
**Solution**: 
- Use smaller dataset
- Or upgrade to Colab Pro for more RAM

### Issue 4: Runtime Disconnected
**Solution**: 
- Colab free tier has time limits
- Save your work frequently
- Use **Runtime** → **Manage sessions** to monitor

---

## 💡 Advanced Usage

### Add More Models

Add this cell after the Random Forest training:

```python
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

# Gradient Boosting
gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
gb_model.fit(X_train_scaled, y_train_bal)
gb_pred = gb_model.predict(X_test_scaled)
print(f"GB Accuracy: {accuracy_score(y_test, gb_pred):.4f}")

# XGBoost
xgb_model = XGBClassifier(n_estimators=100, random_state=42)
xgb_model.fit(X_train_scaled, y_train_bal)
xgb_pred = xgb_model.predict(X_test_scaled)
print(f"XGB Accuracy: {accuracy_score(y_test, xgb_pred):.4f}")
```

### Add SHAP Analysis

Add this cell for model interpretability:

```python
import shap

# Create SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test_scaled)

# Summary plot
shap.summary_plot(shap_values, X_test_scaled, feature_names=X.columns)

# Feature importance
shap.summary_plot(shap_values, X_test_scaled, feature_names=X.columns, plot_type='bar')
```

### Add Confusion Matrix

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Not Promoted', 'Promoted'],
            yticklabels=['Not Promoted', 'Promoted'])
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()
```

### Add ROC Curve

```python
from sklearn.metrics import roc_curve, auc

fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.show()
```

---

## 📊 Expected Results

### With `sample_dataset_100_balanced.csv`:
- **Accuracy**: ~85-95%
- **Precision**: ~80-90%
- **Recall**: ~85-95%
- **F1-Score**: ~82-92%
- **ROC-AUC**: ~0.90-0.95

### With full dataset (imbalanced):
- **Accuracy**: ~75-85%
- **Precision**: ~60-75%
- **Recall**: ~70-85%
- **F1-Score**: ~65-80%
- **ROC-AUC**: ~0.85-0.92

---

## 🎉 Benefits of Using Google Colab

### ✅ Advantages:
1. **Free GPU/TPU**: Access to powerful hardware
2. **No Setup**: No local installation needed
3. **Collaboration**: Easy to share with advisors/committee
4. **Cloud Storage**: Save to Google Drive
5. **Reproducible**: Anyone can run your analysis
6. **Interactive**: Real-time execution and visualization

### ⚠️ Limitations:
1. **Session Timeout**: Free tier has time limits (~12 hours)
2. **RAM Limits**: 12-13 GB RAM on free tier
3. **Storage**: Temporary storage (deleted after session)
4. **Internet Required**: Need stable internet connection

---

## 📚 Additional Resources

### Google Colab Documentation:
- [Official Guide](https://colab.research.google.com/notebooks/intro.ipynb)
- [Markdown Guide](https://colab.research.google.com/notebooks/markdown_guide.ipynb)
- [Data Loading](https://colab.research.google.com/notebooks/io.ipynb)

### Python Libraries:
- [Scikit-learn](https://scikit-learn.org/stable/)
- [XGBoost](https://xgboost.readthedocs.io/)
- [SHAP](https://shap.readthedocs.io/)
- [Imbalanced-learn](https://imbalanced-learn.org/)

---

## 🆘 Need Help?

### Common Questions:

**Q: Can I use my own dataset?**  
A: Yes! Just make sure it has the same structure (has_promotion column as target)

**Q: How long does it take to run?**  
A: ~2-5 minutes for the complete analysis

**Q: Can I save the trained model?**  
A: Yes! Add this code:
```python
import joblib
joblib.dump(model, 'model.pkl')
files.download('model.pkl')
```

**Q: Can I share this with my advisor?**  
A: Yes! Click **Share** button in Colab and send the link

---

## ✅ Checklist Before Thesis Defense

- [ ] Notebook runs without errors
- [ ] All visualizations display correctly
- [ ] Model metrics are reasonable
- [ ] Feature importance makes sense
- [ ] Can explain each step of the analysis
- [ ] Have backup dataset ready
- [ ] Tested on different datasets
- [ ] Screenshots of key results saved

---

## 🎓 Summary

**You now have**:
1. ✅ Complete Jupyter Notebook for Google Colab
2. ✅ Step-by-step guide for running analysis
3. ✅ Dataset recommendations
4. ✅ Troubleshooting tips
5. ✅ Advanced usage examples

**Next steps**:
1. Upload notebook to Google Colab
2. Test with sample dataset
3. Review results
4. Prepare for thesis defense

---

**Good luck with your thesis defense! 🎓🎉**

---

**Last Updated**: November 25, 2025  
**Version**: 1.0  
**Status**: Ready for Use ✅
