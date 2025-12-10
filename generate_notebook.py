#!/usr/bin/env python3
import json

# Create notebook
nb = {'cells': [], 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 0}

# Add cells - keeping it concise due to token limits
cells_data = [
    ('markdown', '# 🎓 MPCIM Thesis - Complete Analysis\n\n**Dual-Dimensional Predictive Analytics untuk Career Progression**\n\nAuthor: Deni Sulaeman | November 2025'),
    ('markdown', '## 1. Setup'),
    ('code', '!pip install -q pandas numpy matplotlib seaborn plotly scikit-learn xgboost shap imbalanced-learn openpyxl'),
    ('code', 'import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score\nfrom imblearn.over_sampling import SMOTE\nimport warnings\nwarnings.filterwarnings("ignore")\nprint("✅ Libraries imported!")'),
    ('markdown', '## 2. Upload Data'),
    ('code', 'from google.colab import files\nprint("📤 Upload CSV file:")\nuploaded = files.upload()\ndata_file = list(uploaded.keys())[0]\nprint(f"✅ Uploaded: {data_file}")'),
    ('markdown', '## 3. Load & Explore'),
    ('code', 'df = pd.read_csv(data_file)\nprint(f"Shape: {df.shape}")\ndisplay(df.head())\ndisplay(df.describe())'),
    ('markdown', '## 4. Data Preparation'),
    ('code', 'y = df["has_promotion"]\nX = df.drop(columns=["has_promotion", "employee_id_hash"], errors="ignore")\nX = X.select_dtypes(include=[np.number])\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nsmote = SMOTE(random_state=42)\nX_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)\nscaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train_bal)\nX_test_scaled = scaler.transform(X_test)\nprint(f"✅ Training: {X_train_scaled.shape}, Test: {X_test_scaled.shape}")'),
    ('markdown', '## 5. Model Training'),
    ('code', 'model = RandomForestClassifier(n_estimators=100, random_state=42)\nmodel.fit(X_train_scaled, y_train_bal)\ny_pred = model.predict(X_test_scaled)\ny_pred_proba = model.predict_proba(X_test_scaled)[:, 1]\nprint(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")\nprint(f"Precision: {precision_score(y_test, y_pred):.4f}")\nprint(f"Recall: {recall_score(y_test, y_pred):.4f}")\nprint(f"F1-Score: {f1_score(y_test, y_pred):.4f}")\nprint(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")'),
    ('markdown', '## 6. Feature Importance'),
    ('code', 'importances = model.feature_importances_\nindices = np.argsort(importances)[::-1][:10]\nplt.figure(figsize=(10, 6))\nplt.barh(range(10), importances[indices])\nplt.yticks(range(10), [X.columns[i] for i in indices])\nplt.xlabel("Importance")\nplt.title("Top 10 Features")\nplt.gca().invert_yaxis()\nplt.show()'),
    ('markdown', '## 7. Done!\n\n✅ Analysis complete. Review results above.')
]

for cell_type, content in cells_data:
    nb['cells'].append({'cell_type': cell_type, 'metadata': {}, 'source': [content], 'execution_count': None, 'outputs': []} if cell_type == 'code' else {'cell_type': cell_type, 'metadata': {}, 'source': [content]})

with open('MPCIM_Thesis_Colab.ipynb', 'w') as f:
    json.dump(nb, f, indent=2)

print("✅ Notebook created: MPCIM_Thesis_Colab.ipynb")
