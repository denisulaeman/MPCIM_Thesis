# Job Level Approach for Promotion Prediction & Succession Planning

## 📋 Overview

Dokumen ini menjelaskan pendekatan **job level** sebagai basis untuk prediksi promosi dan succession planning dalam penelitian ini.

### Mengapa Job Level?

Dengan keterbatasan data standarisasi jabatan dan kompleksitas 1,955 posisi unik, pendekatan job level dipilih karena:

1. ✅ **Tersedia dan terstruktur** - Data job level sudah ada dan reliable
2. ✅ **Mengurangi kompleksitas** - 12 job levels vs 1,955 positions
3. ✅ **Relevan secara bisnis** - Mencerminkan hierarki dan tanggung jawab
4. ✅ **Optimal untuk ML** - Sample size memadai per kategori (~167 karyawan/level untuk 2000 karyawan)

---

## 🗂️ Struktur Job Level

### Hierarki Job Level (3 Groups)

```
Group 0 - Support Level:
├── Non Staff
└── Non Pangkat

Group 1 - Staff/Officer Level:
├── Junior Officer
├── Officer
└── Staff

Group 2 - Management Level:
├── Assistent Manager
├── Manager
├── Senior Manager
├── General Manager
├── Direktur
├── Direktur Utama
├── Komisaris
└── Temporary Position (PJS)
```

### Career Progression Paths

```
Non Staff/Non Pangkat → Staff/Officer
Junior Officer → Officer/Staff
Officer/Staff → Assistent Manager/Manager
Assistent Manager → Manager/Senior Manager
Manager → Senior Manager/General Manager
Senior Manager → General Manager/Direktur
General Manager → Direktur/Direktur Utama
Direktur → Direktur Utama/Komisaris
Direktur Utama → Komisaris
```

---

## 🚀 Cara Penggunaan

### Prerequisites

```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn joblib
```

### Step 1: Analisis Job Level

Script ini menganalisis distribusi karyawan per job level dan membuat feature engineering.

```bash
cd scripts
python 01_job_level_analysis.py
```

**Output:**
- `results/job_level_analysis.png` - Visualisasi distribusi
- `data/final/integrated_full_dataset_with_job_level.csv` - Dataset enhanced

**Fitur yang dibuat:**
- `level_name` - Nama job level (categorical)
- `group_job_level` - Group level (0, 1, 2)
- `promotion_readiness_score` - Composite score untuk kesiapan promosi
- `is_management/is_staff/is_support` - Binary indicators
- `tenure_level_ratio` - Tenure disesuaikan dengan level

### Step 2: Model Prediksi Promosi

Script ini melatih model machine learning untuk memprediksi promosi.

```bash
python 02_promotion_prediction_model.py
```

**Output:**
- `results/promotion_prediction/model_comparison.csv` - Perbandingan model
- `results/promotion_prediction/feature_importance.csv` - Importance features
- `results/promotion_prediction/best_model_*.pkl` - Model terlatih
- `results/promotion_prediction/promotion_prediction_analysis.png` - Visualisasi

**Model yang dilatih:**
1. Logistic Regression
2. Random Forest
3. Gradient Boosting

**Metrics:**
- AUC-ROC
- F1-Score
- Precision/Recall
- Cross-validation scores

### Step 3: Succession Planning

Script ini mengidentifikasi successor candidates dan talent pools.

```bash
python 03_succession_planning.py
```

**Output:**
- `results/succession_planning/successor_candidates.csv` - Top candidates
- `results/succession_planning/talent_pool_by_level.csv` - Talent pool analysis
- `results/succession_planning/succession_gaps.csv` - Gap analysis
- `results/succession_planning/succession_planning_dashboard.png` - Dashboard
- `results/succession_planning/succession_planning_report.txt` - Report lengkap

**Fitur:**
- Identifikasi top 3 successor per job level
- Talent pool strength analysis
- Succession gap identification
- Readiness categorization (Ready Now, 1-2 Years, 3+ Years)

---

## 📊 Key Features

### 1. Promotion Readiness Score

Formula:
```python
promotion_readiness = (
    performance_score * 0.30 +
    behavior_avg * 0.20 +
    leadership_potential * 0.30 +
    holistic_score * 0.20
)
```

### 2. Readiness Categories

| Category | Criteria |
|----------|----------|
| **Ready Now** | Performance ≥85, Leadership ≥80, Tenure ≥2, Behavior ≥85 |
| **Ready 1-2 Years** | Performance ≥75, Leadership ≥70, Tenure ≥1, Behavior ≥75 |
| **Ready 3+ Years** | Performance ≥65, Leadership ≥60, Tenure ≥0, Behavior ≥65 |
| **Not Ready** | Below all criteria |

### 3. Succession Risk Assessment

- **Low Risk**: Job level memiliki ≥1 "Ready Now" successor
- **High Risk**: Job level tidak memiliki "Ready Now" successor

---

## 📈 Expected Results (untuk 2000 karyawan)

### Distribusi Job Level (Estimasi)

| Job Level | Estimated Count | Percentage |
|-----------|----------------|------------|
| Staff | ~400 | 20% |
| Officer | ~350 | 17.5% |
| Manager | ~300 | 15% |
| Senior Manager | ~200 | 10% |
| Assistent Manager | ~180 | 9% |
| Junior Officer | ~150 | 7.5% |
| General Manager | ~120 | 6% |
| Direktur | ~100 | 5% |
| Non Staff | ~80 | 4% |
| Others | ~120 | 6% |

### Model Performance (Target)

| Metric | Target Value |
|--------|--------------|
| AUC-ROC | ≥0.75 |
| F1-Score | ≥0.70 |
| Precision | ≥0.72 |
| Recall | ≥0.68 |

### Succession Planning Metrics

- **Ready Now**: 15-20% of employees
- **Ready 1-2 Years**: 25-30% of employees
- **Critical Gaps**: <10% of job levels
- **Successor Depth**: ≥2 candidates per management position

---

## 🎯 Use Cases

### 1. Prediksi Promosi Individual

```python
import joblib
import pandas as pd

# Load model
model = joblib.load('results/promotion_prediction/best_model_random_forest.pkl')
scaler = joblib.load('results/promotion_prediction/scaler.pkl')

# Prepare employee data
employee_data = pd.DataFrame({...})
employee_scaled = scaler.transform(employee_data)

# Predict
promotion_probability = model.predict_proba(employee_scaled)[:, 1]
print(f"Promotion probability: {promotion_probability[0]:.2%}")
```

### 2. Identifikasi High-Potential Employees

```python
# Load successor candidates
successors = pd.read_csv('results/succession_planning/successor_candidates.csv')

# Filter by readiness
high_potential = successors[successors['readiness_category'] == 'Ready Now']
print(f"High-potential employees: {len(high_potential)}")
```

### 3. Gap Analysis per Department

```python
# Load talent pool data
talent_pool = pd.read_csv('results/succession_planning/talent_pool_by_level.csv')

# Identify weak talent pools
weak_pools = talent_pool[talent_pool['avg_readiness'] < 70]
print("Departments needing talent development:")
print(weak_pools)
```

---

## 💡 Insights & Recommendations

### Key Findings

1. **Job level adalah prediktor kuat** untuk promosi
   - Feature importance biasanya 15-25%
   - Kombinasi dengan performance score memberikan akurasi terbaik

2. **Management level memiliki promotion rate lebih tinggi**
   - Typical: 25-35% vs 10-15% untuk staff level
   - Career path lebih jelas di management level

3. **Tenure dan level berinteraksi**
   - Tenure minimal berbeda per level
   - Manager: 3-5 tahun, Staff: 2-3 tahun

### Recommendations

#### Untuk HR/Talent Management:

1. **Fokus development pada "Ready 1-2 Years"**
   - Mereka punya potensi tapi butuh support
   - ROI tertinggi untuk training investment

2. **Retention strategy untuk "Ready Now"**
   - High-risk untuk turnover
   - Perlu career path yang jelas

3. **Address succession gaps**
   - Prioritas: Management level
   - Opsi: External hiring atau accelerated development

4. **Level-specific development programs**
   - Staff → Manager: Leadership skills
   - Manager → Senior: Strategic thinking
   - Senior → Director: Business acumen

#### Untuk Model Improvement:

1. **Tambahkan fitur temporal**
   - Performance trend (3-5 tahun terakhir)
   - Promotion velocity di level yang sama

2. **Departemen-specific models**
   - Jika sample size cukup (>100 per dept)
   - IT vs Sales vs Operations memiliki pattern berbeda

3. **Ensemble dengan rule-based system**
   - ML untuk scoring
   - Business rules untuk final decision

---

## 📝 Justifikasi untuk Thesis

### Metodologi (untuk ditulis di paper)

> *"Penelitian ini menggunakan **job level** sebagai basis pengelompokan karyawan untuk prediksi promosi dan succession planning. Pendekatan ini dipilih dengan pertimbangan:*
>
> *1. **Relevansi Organisasional**: Job level mencerminkan hierarki dan tanggung jawab dalam struktur organisasi, sehingga lebih relevan untuk analisis promosi dibandingkan job title yang terlalu granular.*
>
> *2. **Optimalisasi Data**: Dengan 12 job levels untuk ~2000 karyawan, distribusi data lebih seimbang (rata-rata 167 karyawan per level) dibandingkan 1,955 job positions (rata-rata 1 karyawan per position), yang mengurangi risiko overfitting dan meningkatkan generalisasi model.*
>
> *3. **Interpretabilitas**: Career progression paths berbasis job level lebih mudah dipahami dan diimplementasikan oleh praktisi HR dibandingkan model berbasis job title yang kompleks.*
>
> *4. **Validitas Konstruk**: Job level memiliki validitas konstruk yang tinggi sebagai proxy untuk kompleksitas pekerjaan, tanggung jawab, dan ekspektasi kinerja, yang merupakan faktor kunci dalam keputusan promosi."*

### Limitasi (untuk ditulis di paper)

> *"Pendekatan job level memiliki beberapa keterbatasan:*
>
> *1. **Kehilangan Nuansa Spesifik**: Perbedaan antara posisi dalam level yang sama (misal: IT Manager vs Sales Manager) tidak tertangkap sepenuhnya.*
>
> *2. **Asumsi Homogenitas**: Model mengasumsikan bahwa karyawan dalam level yang sama memiliki karakteristik serupa, yang mungkin tidak selalu akurat.*
>
> *3. **Career Path Simplifikasi**: Jalur karir yang didefinisikan mungkin tidak mencakup semua kemungkinan lateral moves atau special assignments.*
>
> *Penelitian selanjutnya dapat mengeksplorasi pendekatan hybrid yang menggabungkan job level dengan informasi departemen atau fungsi untuk meningkatkan granularitas tanpa mengorbankan sample size."*

---

## 🔧 Troubleshooting

### Issue: Model accuracy rendah (<0.70)

**Solusi:**
1. Check class imbalance - gunakan SMOTE atau class weights
2. Feature engineering tambahan - interaction terms
3. Hyperparameter tuning - GridSearchCV
4. Coba ensemble methods

### Issue: Succession gaps terlalu banyak

**Solusi:**
1. Review readiness criteria - mungkin terlalu strict
2. Expand talent pool - include "Ready 1-2 Years"
3. Consider external hiring strategy
4. Implement accelerated development programs

### Issue: Feature importance job_level rendah

**Solusi:**
1. Check encoding - pastikan ordinal encoding benar
2. Create interaction features dengan performance
3. Consider level-specific models
4. Validate dengan domain expert

---

## 📚 References

1. Cappelli, P., & Keller, J. R. (2014). Talent management: Conceptual approaches and practical challenges. *Annual Review of Organizational Psychology and Organizational Behavior*, 1(1), 305-331.

2. Church, A. H., & Rotolo, C. T. (2013). How are top companies assessing their high-potentials and senior executives? A talent management benchmark study. *Consulting Psychology Journal: Practice and Research*, 65(3), 199.

3. Silzer, R., & Church, A. H. (2009). The pearls and perils of identifying potential. *Industrial and Organizational Psychology*, 2(4), 377-412.

---

## 📧 Contact

Untuk pertanyaan atau diskusi lebih lanjut:
- **Author**: Denis Ulaeman
- **Email**: [your-email]
- **GitHub**: [your-github]

---

**Last Updated**: December 2025
