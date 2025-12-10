# Draft Paper – Dual-Dimensional Predictive Analytics untuk Promosi Karyawan

## Abstrak
Penelitian ini membangun model prediksi promosi karyawan dengan mengintegrasikan dua dimensi penilaian utama (performance dan behavioral) pada dataset teranonomisasi berisi 712 karyawan (promosi 9,27%). Data diproses melalui pembersihan outlier (IQR), rekayasa fitur (14 fitur termasuk rasio/keselarasan), penanganan imbalance dengan SMOTE, dan pemisahan latih/uji terstratifikasi (80/20). Tiga baseline Logistic Regression dibandingkan dengan model lanjutan (Random Forest, XGBoost, dan Multi-Layer Perceptron). Model terbaik (MLP) mencapai akurasi 90,9% dan F1-score 55,2%, meningkatkan F1 baseline sebesar 48,97% dengan presisi dua kali lipat (24,4% → 50,0%). Uji statistik menunjukkan behavioral score signifikan terhadap promosi (p=0,037), sementara performance tidak (p=0,083); ditemukan pula korelasi negatif masa kerja dengan promosi (tenure paradox). Ekstensi fitur psikologis (28 fitur total) pada dataset seimbang menunjukkan 44,7% keputusan model dipengaruhi faktor psikologis (kepemimpinan, drive, kesiapan mental), menegaskan perlunya penilaian holistik. Hasil ini mendemonstrasikan bahwa pendekatan multi-dimensi meningkatkan akurasi dan interpretabilitas keputusan promosi.

**Kata kunci**: promosi karyawan, machine learning, performance, behavioral, psychological assessment, imbalance handling.

## 1. Pendahuluan
- Tantangan utama promosi adalah ketergantungan pada senioritas dan penilaian subjektif; dataset internal menunjukkan hanya 9,27% karyawan yang dipromosikan.
- Literatur menunjukkan performa teknis tidak selalu memadai; indikator perilaku dan psikologis berkontribusi pada kesiapan kepemimpinan.
- Tujuan: (1) membuktikan manfaat integrasi multi-dimensi, (2) meningkatkan presisi identifikasi kandidat promosi, (3) menyediakan dashboard interpretatif untuk HR.

## 2. Data dan Metodologi
### 2.1 Sumber Data
- Database PostgreSQL organisasi (195 tabel, 60 relevan) dan berkas perilaku Excel.
- Rekaman: 13.478 penilaian kinerja, 19.929 penilaian perilaku, 130 riwayat promosi; digabung via NIK yang di-hash MD5.
- Dataset akhir: 712 karyawan dengan dua dimensi lengkap; distribusi target 66 promosi vs 646 non-promosi.

### 2.2 Pra-pemrosesan
- Anonimisasi penuh (hash), tanpa identitas personal atau data finansial.
- Penanganan outlier: 46 kinerja dan 35 perilaku dicapping dengan IQR.
- Missing values: hanya 14 nilai pada `performance_rating`; diimputasi/di-encode sesuai pipeline.

### 2.3 Rekayasa Fitur (14)
- Rasio/keseimbangan: `perf_beh_ratio`, `score_difference`, `combined_score`.
- Kategori: `tenure_category` (junior/mid/senior), `performance_level`, `behavioral_level`.
- Binary flag: `high_performer`; encoding gender, status nikah, status karyawan, rating kinerja.

### 2.4 Penanganan Imbalance
- SMOTE pada set latih (66:646 → 516:516) dengan stratifikasi; set uji dibiarkan asli.

### 2.5 Pemisahan Data
- Train/test 80/20, stratified, random_state=42; fitur dinormalisasi dengan StandardScaler.

### 2.6 Model dan Evaluasi
- Baseline: Logistic Regression (performance-only, behavioral-only, dual).
- Advanced: Random Forest (100 trees, max_depth=10), XGBoost (100 estimators, depth=6, lr=0.1), MLP (64-32-16, ReLU, Adam).
- Metrik: Accuracy, Precision, Recall, F1 (utama), ROC-AUC; confusion matrix untuk interpretasi kesalahan.

## 3. Hasil
### 3.1 Deskripsi Dataset
| Metric | Performance | Behavioral | Tenure (tahun) |
|--------|-------------|------------|----------------|
| Mean | 81,88 | 89,72 | 8,17 |
| Std | 34,94 | 8,71 | 7,28 |
| Min | 36,63 | 71,51 | 0 |
| Max | 125,31 | 111,09 | 125 |

### 3.2 Uji Signifikansi dan Korelasi
- Behavioral vs promosi: p=0,037 (signifikan); Performance vs promosi: p=0,083 (tidak signifikan).
- Korelasi promosi: behavioral r=0,078; performance r=0,065; tenure r=-0,169 (negatif).
- Temuan: dimensi perilaku lebih informatif daripada kinerja mentah; masa kerja panjang menurunkan peluang promosi.

### 3.3 Kinerja Model
| Model | Akurasi | Presisi | Recall | F1 | ROC-AUC |
|-------|---------|---------|--------|----|---------|
| Performance-only | 57,3% | 15,7% | 84,6% | 26,5% | 72,3% |
| Behavioral-only | 35,0% | 10,8% | 84,6% | 19,1% | 65,3% |
| Dual-dimensional (LR) | 76,2% | 24,4% | 76,9% | 37,0% | 81,2% |
| Random Forest | 87,4% | 39,1% | 69,2% | 50,0% | 90,1% |
| XGBoost | 89,5% | 44,4% | 61,5% | 51,6% | 88,3% |
| **MLP (best)** | **90,9%** | **50,0%** | **61,5%** | **55,2%** | **88,3%** |

**Interpretasi**: Integrasi dua dimensi menaikkan akurasi baseline 32,9% dibanding single-dimension; model MLP menggandakan presisi (24,4% → 50,0%) dengan F1 tertinggi.

### 3.4 Tenure Paradox
| Kategori Tenure | Promoted | Not | Rate |
|-----------------|----------|-----|------|
| Junior (0-2 th) | 28 | 168 | 14,3% |
| Mid (3-7 th) | 24 | 216 | 10,0% |
| Senior (8+ th) | 14 | 262 | 5,1% |

- Rata-rata masa kerja promoted 4,32 tahun vs non-promoted 8,56 tahun; organisasi cenderung mempromosikan talenta awal-karier yang seimbang performa-perilakunya.

### 3.5 Pentingnya Fitur
- Random Forest: `tenure_years` (40,5%) dan `tenure_category` (32,6%) mendominasi; berikutnya `performance_rating` (5,1%), `behavior_avg` (4,6%), `performance_score` (3,6%).
- Insight: senioritas penting, namun dimensi perilaku dan rekayasa rasio tetap berkontribusi 10–15% dan membantu interpretasi.

### 3.6 Ekstensi Psikologis (Data Seimbang)
- Dataset demo seimbang (1000 baris, 70% promoted) menambahkan 14 fitur psikologis (drive, mental strength, adaptability, collaboration, leadership, rasio psikologis).
- Model Random Forest dan kombinasi fitur menunjukkan **44,7%** total importance berasal dari fitur psikologis; `psych_perf_ratio` (6,12%) dan `leadership_potential` (5,98%) masuk 4 besar fitur.
- Evaluasi menunjukkan pemisahan data sangat kuat (skor uji 100% pada subset balanced); perlu validasi silang untuk memastikan tidak ada kebocoran data sebelum publikasi.

## 4. Diskusi
- **Nilai tambah multi-dimensi**: Perilaku terbukti signifikan secara statistik dan meningkatkan presisi; rasio/perbedaan antar dimensi memunculkan profil kandidat seimbang.
- **Praktik HR**: Tenure paradox menantang paradigma senioritas; kebijakan promosi perlu menonjolkan kesiapan awal dan keseimbangan performa-perilaku.
- **Risiko dan mitigasi**: Dataset kecil (712, hanya 66 promosi) dan ketimpangan kelas tinggi; SMOTE membantu tetapi perlu validasi K-Fold dan evaluasi pada periode berbeda untuk menguji stabilitas.
- **Ekstensi psikologis**: Indikator kepemimpinan dan motivasi memperkaya model; namun hasil perfect accuracy pada data seimbang harus diuji ulang untuk mendeteksi potensi overfitting/ data leakage.

## 5. Kesimpulan
- Integrasi performance–behavioral meningkatkan akurasi promosi (76,2% baseline → 90,9% terbaik) dengan lonjakan F1 sebesar 48,97%.
- Behavioral assessment signifikan (p=0,037) sementara performance tidak, menegaskan pentingnya soft skills dalam keputusan promosi.
- Tenure paradox mengindikasikan bias pro-talent awal-karier; temuan ini dapat menginformasikan program percepatan kepemimpinan.
- Ekstensi psikologis menunjukkan pengaruh besar (44,7%) terhadap keputusan model, mendukung pendekatan penilaian holistik.

## 6. Pekerjaan Lanjut
1) Lakukan stratified K-Fold dan uji waktu (train/test antar-periode) untuk menguji generalisasi.  
2) Tambahkan fairness check (gender/marital bias) dan kalibrasi probabilitas.  
3) Integrasikan fitur psikologis ke pipeline utama dan evaluasi pada data produksi 712/1000 baris tanpa kebocoran.  
4) Perluas interpretabilitas (SHAP pada XGBoost/MLP) dan uji ketahanan terhadap noise.  
5) Siapkan naskah jurnal dengan analisis sensitivitas hyperparameter dan ablation study (tanpa rasio, tanpa tenure, tanpa psikologis).

## 7. Reproduksibilitas
- Notebook komprehensif: `MPCIM_Complete_Analysis.ipynb` (6 model, SHAP, perbandingan).  
- Dataset utama: `data/final/integrated_performance_behavioral.csv`; dataset demo seimbang + psikologis: `data/final/sample_dataset_1000_balanced.csv`.  
- Skrip pipeline: `scripts/analysis` (EDA, rekayasa fitur) dan `scripts/modeling` (baseline & advanced).  
- UI & integrasi psikologis: `app/pages/6_👥_Promotion_Candidates.py` (fitur psikologis & interpretasi).
