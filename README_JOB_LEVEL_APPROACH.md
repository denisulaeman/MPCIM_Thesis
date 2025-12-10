# Job Level Approach - Promotion Prediction & Succession Planning

## 🎯 Executive Summary

Penelitian ini menggunakan **job level** sebagai basis untuk prediksi promosi dan succession planning dengan dataset **2000 karyawan**. Pendekatan ini dipilih karena:

- ✅ **Praktis**: Menghindari kompleksitas 1,955 job positions
- ✅ **Optimal**: ~167 karyawan per level (12 levels) - ideal untuk ML
- ✅ **Relevan**: Mencerminkan hierarki dan career progression
- ✅ **Actionable**: Mudah diimplementasikan oleh HR

---

## 📦 Apa yang Sudah Dibuat?

### 1. **Scripts Analisis** (4 files)

#### `00_run_all_analysis.py` - Quick Start
- Menjalankan semua analisis sekaligus
- Pipeline automation
- Error handling & summary report

#### `01_job_level_analysis.py` - Job Level Analysis
- Analisis distribusi karyawan per job level
- Feature engineering untuk model ML
- Identifikasi promotion paths
- Visualisasi distribusi dan promotion rates

**Output:**
- `results/job_level_analysis.png`
- `data/final/integrated_full_dataset_with_job_level.csv`

#### `02_promotion_prediction_model.py` - ML Model
- Training 3 models: Logistic Regression, Random Forest, Gradient Boosting
- Feature importance analysis
- Model evaluation (AUC-ROC, F1, Precision, Recall)
- Cross-validation

**Output:**
- `results/promotion_prediction/model_comparison.csv`
- `results/promotion_prediction/feature_importance.csv`
- `results/promotion_prediction/best_model_*.pkl`
- `results/promotion_prediction/promotion_prediction_analysis.png`

#### `03_succession_planning.py` - Succession Planning
- Identifikasi successor candidates
- Talent pool analysis per job level
- Succession gap identification
- Readiness categorization

**Output:**
- `results/succession_planning/successor_candidates.csv`
- `results/succession_planning/talent_pool_by_level.csv`
- `results/succession_planning/succession_gaps.csv`
- `results/succession_planning/succession_planning_dashboard.png`
- `results/succession_planning/succession_planning_report.txt`

### 2. **Documentation**

#### `docs/JOB_LEVEL_APPROACH_GUIDE.md` - Complete Guide
- Penjelasan lengkap pendekatan job level
- Tutorial penggunaan semua scripts
- Expected results & metrics
- Use cases & recommendations
- Justifikasi untuk thesis
- Troubleshooting guide

---

## 🚀 Quick Start

### Instalasi Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn joblib
```

### Run Complete Pipeline

```bash
cd scripts
python 00_run_all_analysis.py
```

Script ini akan menjalankan:
1. Job level analysis (5-10 menit)
2. Model training (10-15 menit)
3. Succession planning (5-10 menit)

**Total waktu**: ~20-35 menit

### Run Individual Scripts

```bash
# Step 1: Analisis job level
python 01_job_level_analysis.py

# Step 2: Training model
python 02_promotion_prediction_model.py

# Step 3: Succession planning
python 03_succession_planning.py
```

---

## 📊 Expected Results

### Model Performance (Target untuk 2000 karyawan)

| Metric | Target | Interpretation |
|--------|--------|----------------|
| **AUC-ROC** | ≥0.75 | Model dapat membedakan promosi vs non-promosi dengan baik |
| **F1-Score** | ≥0.70 | Balance antara precision dan recall |
| **Precision** | ≥0.72 | 72% prediksi promosi adalah benar |
| **Recall** | ≥0.68 | Model menangkap 68% dari actual promotions |

### Succession Planning Metrics

| Metric | Target | Interpretation |
|--------|--------|----------------|
| **Ready Now** | 15-20% | Karyawan siap promosi sekarang |
| **Ready 1-2 Years** | 25-30% | Karyawan butuh development 1-2 tahun |
| **Critical Gaps** | <10% | Job levels tanpa successor |
| **Successor Depth** | ≥2 per position | Minimal 2 candidates per management position |

### Feature Importance (Expected Top 5)

1. **Performance Score** (25-30%)
2. **Leadership Potential** (20-25%)
3. **Job Level** (15-20%)
4. **Behavior Average** (10-15%)
5. **Tenure Years** (8-12%)

---

## 📁 Output Structure

```
MPCIM_Thesis/
├── scripts/
│   ├── 00_run_all_analysis.py          # Quick start pipeline
│   ├── 01_job_level_analysis.py        # Job level analysis
│   ├── 02_promotion_prediction_model.py # ML model training
│   └── 03_succession_planning.py       # Succession planning
│
├── results/
│   ├── job_level_analysis.png          # Visualisasi distribusi
│   │
│   ├── promotion_prediction/
│   │   ├── model_comparison.csv        # Perbandingan model
│   │   ├── feature_importance.csv      # Feature importance
│   │   ├── best_model_*.pkl            # Trained model
│   │   ├── scaler.pkl                  # Feature scaler
│   │   ├── predictions.csv             # Test predictions
│   │   └── promotion_prediction_analysis.png
│   │
│   └── succession_planning/
│       ├── successor_candidates.csv     # Top candidates
│       ├── talent_pool_by_level.csv    # Talent pool analysis
│       ├── succession_gaps.csv         # Gap analysis
│       ├── succession_planning_dashboard.png
│       └── succession_planning_report.txt
│
├── data/
│   └── final/
│       └── integrated_full_dataset_with_job_level.csv  # Enhanced dataset
│
└── docs/
    └── JOB_LEVEL_APPROACH_GUIDE.md     # Complete documentation
```

---

## 🎓 Untuk Thesis

### Metodologi (Copy-paste ready)

**Pendekatan Job Level untuk Prediksi Promosi**

Penelitian ini menggunakan job level sebagai basis pengelompokan karyawan untuk prediksi promosi dan succession planning. Dengan 12 job levels yang dikelompokkan dalam 3 kategori (Support, Staff/Officer, Management), pendekatan ini memberikan keseimbangan optimal antara granularitas dan sample size.

**Justifikasi:**
1. **Relevansi Organisasional**: Job level mencerminkan hierarki dan tanggung jawab dalam struktur organisasi
2. **Optimalisasi Data**: Distribusi data lebih seimbang (~167 karyawan per level) dibandingkan job positions (rata-rata 1 karyawan per position)
3. **Interpretabilitas**: Career progression paths lebih mudah dipahami dan diimplementasikan
4. **Validitas Konstruk**: Job level memiliki validitas tinggi sebagai proxy untuk kompleksitas pekerjaan

**Feature Engineering:**
- `group_job_level`: Ordinal encoding (0=Support, 1=Staff, 2=Management)
- `level_name_encoded`: Categorical encoding untuk 12 levels
- `promotion_readiness_score`: Composite score (performance×0.3 + leadership×0.3 + behavior×0.2 + holistic×0.2)
- `is_management/is_staff/is_support`: Binary indicators
- `tenure_level_ratio`: Tenure disesuaikan dengan level

**Model Selection:**
Tiga algoritma machine learning dibandingkan: Logistic Regression, Random Forest, dan Gradient Boosting. Model terbaik dipilih berdasarkan AUC-ROC dengan 5-fold cross-validation.

### Limitasi (Copy-paste ready)

**Keterbatasan Penelitian:**

1. **Kehilangan Nuansa Spesifik**: Perbedaan antara posisi dalam level yang sama (misal: IT Manager vs Sales Manager) tidak tertangkap sepenuhnya. Penelitian selanjutnya dapat mengeksplorasi pendekatan hybrid dengan informasi departemen.

2. **Asumsi Homogenitas**: Model mengasumsikan karyawan dalam level yang sama memiliki karakteristik serupa, yang mungkin tidak selalu akurat untuk organisasi dengan struktur kompleks.

3. **Career Path Simplifikasi**: Jalur karir yang didefinisikan mungkin tidak mencakup semua kemungkinan lateral moves atau special assignments yang terjadi dalam praktik.

4. **Data Temporal**: Analisis ini menggunakan snapshot data pada satu titik waktu. Analisis longitudinal dapat memberikan insight lebih dalam tentang career progression patterns.

### Kontribusi (Copy-paste ready)

**Kontribusi Penelitian:**

1. **Praktis**: Menyediakan framework yang dapat langsung diimplementasikan oleh praktisi HR tanpa memerlukan data standarisasi jabatan yang kompleks.

2. **Metodologis**: Mendemonstrasikan pendekatan pragmatis untuk mengatasi keterbatasan data dalam konteks talent management di Indonesia.

3. **Teoritis**: Memvalidasi penggunaan job level sebagai konstruk yang valid untuk prediksi promosi dalam konteks organisasi Indonesia.

4. **Aplikatif**: Menghasilkan sistem succession planning yang actionable dengan identifikasi successor candidates dan gap analysis.

---

## 💡 Key Insights & Recommendations

### Untuk HR/Talent Management

1. **Fokus Development pada "Ready 1-2 Years"**
   - ROI tertinggi untuk training investment
   - Potensi besar tapi butuh support

2. **Retention Strategy untuk "Ready Now"**
   - High-risk untuk turnover
   - Perlu career path yang jelas dan challenging assignments

3. **Address Succession Gaps**
   - Prioritas: Management level
   - Opsi: External hiring atau accelerated development

4. **Level-Specific Development Programs**
   - Staff → Manager: Leadership & people management
   - Manager → Senior: Strategic thinking & business acumen
   - Senior → Director: Vision & organizational leadership

### Untuk Model Improvement

1. **Tambahkan Fitur Temporal**
   - Performance trend (3-5 tahun terakhir)
   - Promotion velocity di level yang sama

2. **Department-Specific Models**
   - Jika sample size cukup (>100 per dept)
   - IT vs Sales vs Operations memiliki pattern berbeda

3. **Ensemble dengan Rule-Based System**
   - ML untuk scoring
   - Business rules untuk final decision
   - Human-in-the-loop untuk edge cases

---

## 🔍 Validation Checklist

Sebelum menggunakan hasil untuk thesis:

- [ ] **Data Quality**
  - [ ] Check missing values (<5%)
  - [ ] Validate job level mapping
  - [ ] Verify promotion history accuracy

- [ ] **Model Performance**
  - [ ] AUC-ROC ≥0.75
  - [ ] Cross-validation stable (std <0.05)
  - [ ] No data leakage

- [ ] **Business Validation**
  - [ ] Review top successors dengan HR
  - [ ] Validate career paths dengan domain expert
  - [ ] Check succession gaps dengan actual needs

- [ ] **Interpretability**
  - [ ] Feature importance makes sense
  - [ ] Predictions are explainable
  - [ ] Results align with business intuition

---

## 📞 Support & Questions

### Common Questions

**Q: Bagaimana jika promotion rate sangat rendah (<5%)?**
A: Gunakan SMOTE atau class weights untuk handle imbalance. Consider juga mengubah target menjadi "promotion readiness" (continuous) instead of binary.

**Q: Model accuracy rendah (<0.70)?**
A: 
1. Check feature engineering - tambahkan interaction terms
2. Try hyperparameter tuning
3. Consider ensemble methods
4. Validate data quality

**Q: Succession gaps terlalu banyak (>30%)?**
A:
1. Review readiness criteria - mungkin terlalu strict
2. Expand time horizon (include "Ready 1-2 Years")
3. Consider external hiring strategy

**Q: Job level importance rendah (<10%)?**
A:
1. Check encoding method
2. Create interaction features dengan performance
3. Consider level-specific models
4. Validate dengan domain expert

### Troubleshooting

Jika ada error saat running scripts:

1. **Import Error**: Install missing packages
   ```bash
   pip install -r requirements.txt
   ```

2. **File Not Found**: Check data paths
   ```python
   # Verify paths in script
   print(BASE_DIR)
   print(DATA_DIR)
   ```

3. **Memory Error**: Reduce sample size atau use chunking
   ```python
   df = pd.read_csv(file, chunksize=10000)
   ```

4. **Model Training Slow**: Reduce n_estimators atau use n_jobs=-1
   ```python
   RandomForestClassifier(n_estimators=50, n_jobs=-1)
   ```

---

## 📚 References

1. Cappelli, P., & Keller, J. R. (2014). Talent management: Conceptual approaches and practical challenges. *Annual Review of Organizational Psychology and Organizational Behavior*, 1(1), 305-331.

2. Church, A. H., & Rotolo, C. T. (2013). How are top companies assessing their high-potentials and senior executives? *Consulting Psychology Journal: Practice and Research*, 65(3), 199.

3. Silzer, R., & Church, A. H. (2009). The pearls and perils of identifying potential. *Industrial and Organizational Psychology*, 2(4), 377-412.

4. Fernández-Aráoz, C., Groysberg, B., & Nohria, N. (2011). How to hang on to your high potentials. *Harvard Business Review*, 89(10), 76-83.

---

## ✅ Next Steps

1. **Run the pipeline**
   ```bash
   python scripts/00_run_all_analysis.py
   ```

2. **Review outputs**
   - Check visualizations in `results/`
   - Read succession planning report
   - Validate with domain experts

3. **Iterate if needed**
   - Adjust readiness criteria
   - Fine-tune model parameters
   - Add domain-specific features

4. **Document for thesis**
   - Use methodology section above
   - Include visualizations
   - Discuss findings and limitations

5. **Implement in production** (optional)
   - Create API for predictions
   - Build dashboard for HR
   - Schedule periodic updates

---

**Good luck with your thesis! 🎓**

---

*Last Updated: December 2025*
*Author: Denis Ulaeman*
