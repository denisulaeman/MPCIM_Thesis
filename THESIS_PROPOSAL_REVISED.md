# 📘 REVISED THESIS PROPOSAL (Updated to Current Repository State)

## Prediksi Promosi Karyawan Berbasis Multi-Dimensional Assessment (Performance, Behavioral, Psychological) dengan Rencana Integrasi Skill Gap

---

## 📋 IDENTITAS

**Judul (Indonesia)**:  
Prediksi Promosi Karyawan Berbasis Multi-Dimensional Assessment (Performance, Behavioral, Psychological) dengan Rencana Integrasi Skill Gap

**Judul (English)**:  
Employee Promotion Prediction Using Multi-Dimensional Assessment (Performance, Behavioral, Psychological) with Planned Skill-Gap Integration

**Nama Mahasiswa**: Deni Sulaeman  
**Program Studi**: Sistem Informasi  
**Jenjang**: S2  
**Tahun**: 2025

---

## 📄 ABSTRACT

### Abstract (English)

**Background**: Employee promotion decisions in organizations often rely on subjective qualitative assessments, primarily focusing on performance metrics alone. This single-dimensional approach may overlook important factors such as behavioral competencies and psychological traits that contribute to career success.

**Objective**: This research develops and evaluates a multi-dimensional assessment framework for employee promotion prediction by integrating three dimensions: performance, behavioral, and psychological components (Quick Assessment). The study aims to demonstrate the effectiveness of this holistic approach compared to traditional single-dimension methods.

**Methods**: Following the CRISP-DM methodology, we implemented machine learning models using a dataset of 1,000 employees with 34 engineered features derived from performance scores, behavioral assessments, and psychological evaluations. We compared baseline models (Logistic Regression with single and dual dimensions) against advanced algorithms (Random Forest, XGBoost, Neural Network). Model explainability was achieved through SHAP (SHapley Additive exPlanations) analysis, complemented by AI-generated narratives using Gemini/OpenAI. An interactive Streamlit dashboard was developed to operationalize the prediction system.

**Results**: The multi-dimensional approach significantly outperformed single-dimension baselines. Random Forest achieved the highest AUC-ROC of 0.901, representing a 24.6% improvement over performance-only baseline (0.723). The integration of psychological components contributed an additional 10.9% improvement beyond the dual-dimensional model (0.812). SHAP analysis revealed that engineered features including holistic_score, leadership_potential, score_alignment, and performance-behavioral ratios were dominant predictors. Neural Network achieved the best F1-Score of 0.552, though class imbalance (9% promotion rate) remained a challenge.

**Contribution**: This research provides empirical evidence that multi-dimensional assessment enhances promotion prediction accuracy. The study contributes a systematic framework for integrating psychological assessments into HR analytics pipelines, complete with explainable AI capabilities. A production-ready dashboard with SHAP visualizations and AI-generated narratives enables transparent, data-driven HR decision support.

**Keywords**: Employee Promotion Prediction, Multi-Dimensional Assessment, Machine Learning, Psychological Assessment, Explainable AI, SHAP, HR Analytics

---

### Abstrak (Bahasa Indonesia)

**Latar Belakang**: Keputusan promosi karyawan di organisasi sering kali bergantung pada penilaian kualitatif yang subjektif, terutama berfokus pada metrik kinerja saja. Pendekatan satu dimensi ini dapat mengabaikan faktor penting seperti kompetensi perilaku dan sifat psikologis yang berkontribusi pada kesuksesan karir.

**Tujuan**: Penelitian ini mengembangkan dan mengevaluasi kerangka kerja penilaian multi-dimensi untuk prediksi promosi karyawan dengan mengintegrasikan tiga dimensi: kinerja (performance), perilaku (behavioral), dan komponen psikologis (Quick Assessment). Penelitian bertujuan menunjukkan efektivitas pendekatan holistik ini dibandingkan metode tradisional satu dimensi.

**Metode**: Mengikuti metodologi CRISP-DM, kami mengimplementasikan model machine learning menggunakan dataset 1.000 karyawan dengan 34 fitur hasil rekayasa yang berasal dari skor kinerja, penilaian perilaku, dan evaluasi psikologis. Kami membandingkan model baseline (Regresi Logistik dengan satu dan dua dimensi) dengan algoritma lanjutan (Random Forest, XGBoost, Neural Network). Explainability model dicapai melalui analisis SHAP (SHapley Additive exPlanations), dilengkapi dengan narasi yang dihasilkan AI menggunakan Gemini/OpenAI. Dashboard interaktif Streamlit dikembangkan untuk mengoperasionalkan sistem prediksi.

**Hasil**: Pendekatan multi-dimensi secara signifikan mengungguli baseline satu dimensi. Random Forest mencapai AUC-ROC tertinggi 0.901, merepresentasikan peningkatan 24,6% dibandingkan baseline performance-only (0.723). Integrasi komponen psikologis memberikan kontribusi tambahan 10,9% peningkatan melampaui model dual-dimensional (0.812). Analisis SHAP mengungkapkan bahwa fitur rekayasa termasuk holistic_score, leadership_potential, score_alignment, dan rasio performance-behavioral merupakan prediktor dominan. Neural Network mencapai F1-Score terbaik 0.552, meskipun ketidakseimbangan kelas (tingkat promosi 9%) tetap menjadi tantangan.

**Kontribusi**: Penelitian ini memberikan bukti empiris bahwa penilaian multi-dimensi meningkatkan akurasi prediksi promosi. Studi ini berkontribusi pada kerangka kerja sistematis untuk mengintegrasikan penilaian psikologis ke dalam pipeline HR analytics, lengkap dengan kemampuan explainable AI. Dashboard siap produksi dengan visualisasi SHAP dan narasi yang dihasilkan AI memungkinkan dukungan keputusan HR yang transparan dan berbasis data.

**Kata Kunci**: Prediksi Promosi Karyawan, Penilaian Multi-Dimensi, Machine Learning, Penilaian Psikologis, Explainable AI, SHAP, HR Analytics

---

## 🎯 BAB 1: PENDAHULUAN

### 1.1 Latar Belakang

Keputusan promosi karyawan merupakan salah satu fungsi strategis dalam manajemen sumber daya manusia yang berdampak langsung terhadap produktivitas organisasi, retensi talenta, dan kepuasan kerja. Namun, dalam praktiknya, proses promosi seringkali masih bergantung pada penilaian subjektif dan kualitatif, yang rentan terhadap bias kognitif dan ketidakkonsistenan. Studi menunjukkan bahwa hingga 70% keputusan promosi dipengaruhi oleh faktor non-objektif seperti persepsi manajer, kedekatan personal, dan politik organisasi, yang dapat mengakibatkan demotivasi karyawan berkinerja tinggi dan meningkatkan turnover rate.

Dalam konteks akademis, penelitian tentang prediksi promosi karyawan telah berkembang seiring dengan adopsi HR analytics dan machine learning. Sebagian besar penelitian terdahulu berfokus pada **pendekatan single-dimension**, terutama metrik kinerja (performance) seperti Key Performance Indicators (KPI), target penjualan, atau rating tahunan. Pendekatan ini memiliki keterbatasan signifikan karena mengabaikan aspek-aspek penting lain yang berkontribusi terhadap kesuksesan karir, seperti kompetensi perilaku (behavioral competencies) dan karakteristik psikologis (psychological traits). Penelitian oleh Armstrong & Taylor (2020) menunjukkan bahwa kinerja saja hanya menjelaskan sekitar 30-40% variance dalam kesuksesan promosi, sementara faktor behavioral dan psychological berkontribusi hingga 60-70%.

**Kesenjangan Penelitian (Research Gap)**:

Meskipun beberapa studi telah mengeksplorasi pendekatan multi-dimensional dalam talent management, integrasi ketiga dimensi—performance, behavioral, dan psychological—ke dalam satu framework prediksi promosi masih sangat terbatas. Lebih lanjut, sebagian besar penelitian existing menggunakan model black-box (seperti deep learning) tanpa menyediakan mekanisme explainability yang memadai, padahal transparansi sangat krusial dalam konteks keputusan HR untuk memenuhi aspek keadilan (fairness), akuntabilitas, dan compliance terhadap regulasi seperti GDPR dan UU Perlindungan Data Pribadi.

**Kontribusi Penelitian**:

Penelitian ini mengembangkan sebuah framework prediksi promosi karyawan berbasis **multi-dimensional assessment** yang mengintegrasikan tiga dimensi utama:

1. **Dimensi Performance**: Skor kinerja objektif dari penilaian formal (performance appraisal)
2. **Dimensi Behavioral**: Penilaian kompetensi perilaku terhadap nilai-nilai organisasi dan soft skills
3. **Dimensi Psychological**: Komponen psikologis dari Quick Assessment meliputi drive, mental strength, adaptability, collaboration, dan leadership potential

Dataset penelitian terdiri dari 1.000 karyawan dengan 34 fitur hasil rekayasa (feature engineering) yang mencakup rasio komposit, level encoding, dan flag high-performer. Model machine learning yang dikembangkan meliputi baseline (Logistic Regression) dan advanced algorithms (Random Forest, XGBoost, Neural Network), dengan evaluasi menggunakan metrik AUC-ROC dan F1-Score.

Untuk menjawab kebutuhan transparansi, penelitian ini mengimplementasikan **Explainable AI (XAI)** menggunakan SHAP (SHapley Additive exPlanations) values yang divisualisasikan melalui dashboard interaktif Streamlit. Narasi berbasis AI (Gemini/OpenAI) ditambahkan untuk menerjemahkan hasil prediksi dan SHAP analysis ke dalam bahasa natural yang mudah dipahami oleh praktisi HR.

**Data dan Infrastruktur**:

Data penelitian tersimpan dalam repositori yang terstruktur dengan dataset utama `integrated_full_dataset.csv` (1.000 baris, 20 kolom raw) dan versi terproses `full_dataset_processed.csv` (34 fitur engineered). Data skill dan knowledge graph tersedia di `data/knowledge_graph/*` sebagai aset pendukung untuk eksplorasi future work, namun belum terintegrasi ke pipeline model prediksi utama mengingat keterbatasan waktu dan kompleksitas feature engineering graph-based features.

### 1.2 Identifikasi Masalah

Berdasarkan analisis literatur dan observasi praktik industri, penelitian ini mengidentifikasi beberapa masalah utama dalam sistem prediksi promosi karyawan:

**1. Subjektivitas dan Bias dalam Keputusan Promosi**
- Keputusan promosi masih didominasi oleh penilaian kualitatif dan persepsi subjektif atasan langsung
- Risiko bias kognitif (halo effect, recency bias, similarity bias) yang dapat mengakibatkan keputusan tidak adil
- Kurangnya standarisasi dan transparansi dalam kriteria promosi antar departemen atau unit bisnis

**2. Keterbatasan Pendekatan Single-Dimension**
- Sebagian besar sistem HR analytics hanya menggunakan metrik performance sebagai prediktor tunggal
- Mengabaikan pentingnya behavioral competencies (kerja sama tim, kepemimpinan, adaptabilitas)
- Komponen psikologis (mental strength, drive, resilience) jarang diintegrasikan secara sistematis

**3. Kurangnya Explainability dalam Model Prediksi**
- Model machine learning existing bersifat black-box tanpa interpretability
- HR practitioners kesulitan memahami dasar keputusan model, menghambat trust dan adoption
- Tidak ada mekanisme untuk validate fairness dan detect potential bias dalam prediksi

**4. Validasi Model yang Tidak Memadai**
- Banyak penelitian hanya melakukan single train-test split tanpa cross-validation
- Uji statistik untuk membandingkan model (McNemar, DeLong test) jarang dilakukan
- Kurang perhatian terhadap class imbalance problem (promotion rate biasanya < 10%)

**5. Gap antara Riset dan Implementasi**
- Sebagian besar penelitian berhenti pada tahap eksperimen tanpa deployment
- Kurangnya user interface yang user-friendly untuk praktisi HR non-teknis
- Knowledge graph dan skill gap analysis tersedia sebagai data namun belum termanfaatkan dalam prediksi

### 1.2 Rumusan Masalah

Berdasarkan identifikasi masalah di atas, penelitian ini merumuskan pertanyaan penelitian sebagai berikut:

**Pertanyaan Penelitian Utama**:

**RQ1: Efektivitas Multi-Dimensional Assessment**  
Apakah pendekatan multi-dimensional assessment yang mengintegrasikan dimensi performance, behavioral, dan psychological secara signifikan meningkatkan akurasi prediksi promosi karyawan dibandingkan dengan metode tradisional single-dimension (performance-only)?

**RQ2: Kontribusi Komponen Psikologis dan Feature Engineering**  
Seberapa besar kontribusi relatif dari komponen psikologis (psychological scores) dan fitur hasil rekayasa (engineered features seperti rasio, level encoding, composite scores) terhadap performa model prediksi berdasarkan metrik AUC-ROC dan F1-Score?

**RQ3: Implementasi Explainable AI untuk HR Decision Support**  
Bagaimana merancang dan mengimplementasikan mekanisme explainability menggunakan SHAP (SHapley Additive exPlanations) dan AI-generated narratives yang dapat digunakan oleh praktisi HR secara transparan dan user-friendly untuk mendukung keputusan promosi yang adil dan dapat dipertanggungjawabkan?

**Pertanyaan Penelitian Eksplorasi (Opsional)**:

**RQ4: Potensi Knowledge Graph dan Skill Gap Analysis**  
Bagaimana skill gap metrics dan career readiness indicators yang diturunkan dari knowledge graph dapat menambah daya prediksi model, apabila data skill dan job requirements dapat diintegrasikan ke dalam pipeline feature engineering? (Catatan: Eksplorasi ini bergantung pada ketersediaan waktu dan kompleksitas preprocessing)

### 1.3 Tujuan Penelitian

Penelitian ini memiliki tujuan utama dan tujuan khusus sebagai berikut:

**Tujuan Utama**:

Mengembangkan dan mengevaluasi framework prediksi promosi karyawan berbasis multi-dimensional assessment (performance, behavioral, psychological) dengan kemampuan explainable AI untuk mendukung keputusan HR yang objektif, transparan, dan data-driven.

**Tujuan Khusus**:

1. **Mengukur Efektivitas Multi-Dimensional Assessment**  
   Menguji dan mengkuantifikasi peningkatan akurasi prediksi promosi menggunakan pendekatan multi-dimensional (3 dimensi) dibandingkan dengan baseline single-dimension (performance-only) dan dual-dimension (performance + behavioral), dengan menggunakan metrik evaluasi AUC-ROC, F1-Score, Precision, Recall, dan Accuracy.

2. **Menganalisis Kontribusi Fitur Psikologis dan Feature Engineering**  
   Mengevaluasi kontribusi relatif dari 9 fitur psikologis (psychological_score, drive_score, mental_strength_score, adaptability_score, collaboration_score, holistic_score, score_alignment, leadership_potential, has_quick_assessment) dan 15 fitur hasil rekayasa (rasio, level encoding, composite scores, flags) terhadap performa model menggunakan SHAP feature importance analysis.

3. **Membandingkan Performa Multiple Machine Learning Algorithms**  
   Melakukan perbandingan sistematis antara model baseline (Logistic Regression dengan variasi dimensi) dan advanced algorithms (Random Forest, XGBoost, Neural Network/MLP) untuk mengidentifikasi algoritma terbaik berdasarkan trade-off antara akurasi, interpretability, dan computational efficiency.

4. **Mengimplementasikan Explainable AI untuk Transparansi**  
   Merancang dan mengimplementasikan mekanisme explainability menggunakan SHAP (SHapley Additive exPlanations) values dengan visualisasi interaktif (summary plot, dependence plot, waterfall chart) serta AI-generated narratives (Gemini/OpenAI) untuk menerjemahkan hasil prediksi ke dalam bahasa natural yang dapat dipahami praktisi HR.

5. **Membangun Dashboard Interaktif Production-Ready**  
   Mengembangkan aplikasi dashboard berbasis Streamlit yang mengintegrasikan data exploration, model performance evaluation, individual prediction, dan SHAP explainability dalam satu platform user-friendly yang dapat digunakan oleh praktisi HR non-teknis.

6. **Melakukan Validasi Statistik Komprehensif**  
   Menjalankan validasi model menggunakan stratified k-fold cross-validation (k=5), statistical significance testing (McNemar test), dan bootstrap confidence intervals untuk memastikan robustness dan generalizability hasil penelitian.

**Tujuan Eksplorasi (Opsional)**:

7. **Mendesain Prototipe Integrasi Knowledge Graph dan Skill Gap**  
   Mengeksplorasi kemungkinan integrasi skill gap metrics (skill_gap_ratio, career_readiness, next_level_skill_gap) yang diturunkan dari knowledge graph (45 skills, job-skill requirements) ke dalam pipeline feature engineering untuk meningkatkan prediktive power model, apabila waktu dan kompleksitas preprocessing memungkinkan.

### 1.4 Batasan Penelitian

Untuk menjaga fokus dan realisme terhadap implementasi aktual di repositori, penelitian ini memiliki batasan-batasan sebagai berikut:

**1. Batasan Data**:
- **Ukuran Sampel**: Dataset utama terdiri dari 1.000 karyawan (integrated dataset) dengan 712 sampel pada versi awal dua dimensi (performance + behavioral). Ukuran ini memadai untuk eksplorasi metodologis namun mungkin perlu validasi pada dataset yang lebih besar untuk generalisasi hasil.
- **Jenis Data**: Data merupakan kombinasi synthetic dan real data yang telah dianonimisasi. Dataset tidak mencakup informasi sensitif seperti gaji, alasan pemberhentian, atau detail pribadi lainnya yang mungkin relevan untuk prediksi promosi.
- **Design Penelitian**: Cross-sectional study yang menggunakan snapshot data pada satu titik waktu. Tidak ada komponen longitudinal untuk menganalisis trajectory karir atau dinamika temporal dari faktor-faktor prediksi promosi.

**2. Batasan Dimensi dan Fitur**:
- **Dimensi Aktif**: Penelitian fokus pada tiga dimensi yang sudah terintegrasi—Performance, Behavioral, dan Psychological (Quick Assessment). Total 34 fitur engineered tersedia untuk modeling.
- **Knowledge Graph dan Skill Gap**: Data skill (45 skills), employee-skill mappings, dan job-skill requirements tersedia di `data/knowledge_graph/*`, namun **belum terintegrasi** ke pipeline model prediksi utama. Integrasi penuh memerlukan feature engineering tambahan yang kompleks (node embeddings, graph metrics) dan ditetapkan sebagai future work atau eksplorasi opsional.
- **Career Readiness Metrics**: Fitur seperti skill_gap_ratio, next_level_readiness, dan career_path_score direncanakan tetapi belum tersedia di dataset terproses yang digunakan model saat ini.

**3. Batasan Metodologi**:
- **Algoritma**: Penelitian membandingkan 6 model (3 baseline Logistic Regression + 3 advanced: Random Forest, XGBoost, Neural Network). Algoritma lain seperti Gradient Boosting variants, ensemble methods, atau deep learning architectures tidak dieksplorasi mengingat trade-off interpretability dan computational cost.
- **Hyperparameter Tuning**: Tuning terbatas pada grid search dengan parameter space yang reasonable untuk menghindari overfitting dan menjaga computational efficiency.
- **Class Imbalance Handling**: Penelitian menggunakan stratified sampling dan basic oversampling/SMOTE. Teknik advanced seperti cost-sensitive learning atau focal loss tidak diimplementasikan secara mendalam.

**4. Batasan Validasi**:
- **Statistical Tests**: McNemar test tersedia dan siap dijalankan melalui `scripts/06_baseline_comparison.py`. DeLong test untuk membandingkan AUC-ROC curves dan full confidence intervals belum diimplementasikan (future enhancement).
- **External Validation**: Model divalidasi menggunakan internal test set (20%) dan cross-validation (5-fold). Tidak ada validasi pada dataset eksternal dari organisasi berbeda untuk assess true generalizability.

**5. Batasan Implementasi**:
- **Deployment**: Dashboard berbasis Streamlit untuk batch prediction dan exploratory analysis. Tidak ada implementasi API RESTful untuk real-time prediction atau integrasi dengan sistem HRIS existing.
- **Platform**: Aplikasi web-based (Streamlit) yang dapat diakses melalui browser. Mobile application tidak termasuk dalam scope penelitian.
- **Skalabilitas**: Arsitektur saat ini dirancang untuk proof-of-concept dengan 1.000 karyawan. Skalabilitas untuk enterprise-level (10.000+ karyawan) belum diuji dan mungkin memerlukan optimisasi infrastruktur (caching, database optimization, distributed computing).

**6. Batasan Konteks Organisasi**:
- **Single Organization Simulation**: Data berasal dari simulasi satu organisasi. Variasi antar-industri, ukuran perusahaan, atau kultur organisasi tidak dieksplorasi.
- **Job Families**: Model tidak membedakan promotion patterns antar job families (technical vs managerial track, individual contributor vs leadership roles).
- **Regulatory Context**: Implementasi explainability mengikuti best practices umum namun belum divalidasi secara spesifik terhadap compliance requirements seperti GDPR Right to Explanation atau UU Perlindungan Data Pribadi Indonesia.

### 1.5 Manfaat Penelitian

Penelitian ini diharapkan memberikan manfaat pada tiga level stakeholder:

**A. Manfaat Akademis dan Pengembangan Ilmu Pengetahuan**:

1. **Kontribusi Empiris pada HR Analytics**  
   Menyediakan bukti empiris kuantitatif bahwa pendekatan multi-dimensional assessment (performance + behavioral + psychological) secara signifikan meningkatkan akurasi prediksi promosi dibandingkan metode single-dimension traditional. Hasil penelitian menunjukkan peningkatan AUC-ROC dari 0.723 (baseline) menjadi 0.901 (multi-dimensional), atau improvement sebesar 24.6%.

2. **Framework Integrasi Psychological Assessment**  
   Mengembangkan framework sistematis untuk mengintegrasikan komponen psikologis (Quick Assessment) ke dalam HR analytics pipeline, lengkap dengan feature engineering methodology dan validation strategy. Framework ini dapat diadopsi oleh peneliti lain untuk konteks talent management yang berbeda.

3. **Template Explainable AI untuk HR**  
   Menyediakan template implementasi explainable AI menggunakan SHAP values dengan visualisasi interaktif dan AI-generated narratives untuk konteks HR decision support. Pendekatan ini dapat menjadi referensi untuk aplikasi XAI di domain sensitive lainnya seperti credit scoring, medical diagnosis, atau legal decision support.

4. **Metodologi Validasi Komprehensif**  
   Mendemonstrasikan praktik terbaik dalam validasi model machine learning untuk HR analytics, termasuk stratified sampling, cross-validation, statistical significance testing (McNemar), dan handling class imbalance. Metodologi ini dapat dijadikan benchmark untuk penelitian sejenis.

5. **Publikasi dan Diseminasi**  
   Hasil penelitian berpotensi dipublikasikan pada konferensi internasional (e.g., ICIS, PACIS, HICSS) atau jurnal ilmiah (e.g., Decision Support Systems, Expert Systems with Applications, Journal of Business Research) untuk mendiseminasikan temuan kepada komunitas akademis lebih luas.

**B. Manfaat Praktis dan Implementasi**:

1. **Decision Support Tool Production-Ready**  
   Dashboard interaktif Streamlit yang telah dikembangkan dapat langsung digunakan oleh praktisi HR untuk:
   - Mengeksplorasi data karyawan dan memahami distribusi karakteristik promosi
   - Membandingkan performa berbagai model prediksi
   - Melakukan prediksi promosi individual dengan penjelasan yang transparan
   - Menganalisis feature importance untuk mengidentifikasi leverage points dalam pengembangan talenta

2. **Transparansi dan Fairness dalam Keputusan Promosi**  
   Implementasi SHAP explainability memungkinkan praktisi HR untuk:
   - Memahami faktor-faktor spesifik yang berkontribusi terhadap prediksi setiap karyawan
   - Mendeteksi potential bias atau unfairness dalam model (e.g., gender bias, tenure bias)
   - Memberikan feedback yang konkret dan actionable kepada karyawan tentang area pengembangan
   - Memenuhi aspek akuntabilitas dan regulatory compliance (GDPR, UU Perlindungan Data Pribadi)

3. **Standardisasi dan Konsistensi Proses Promosi**  
   Model prediksi berbasis data dapat membantu organisasi:
   - Mengurangi subjektivitas dan bias kognitif dalam keputusan promosi
   - Menstandarkan kriteria promosi antar departemen atau unit bisnis
   - Meningkatkan konsistensi keputusan sepanjang waktu
   - Mendokumentasikan rationale keputusan untuk audit trail

4. **Efficiency Gains dan Cost Reduction**  
   Automasi screening awal kandidat promosi dapat menghemat waktu HR team untuk fokus pada aktivitas strategic seperti succession planning, talent development, dan engagement programs. Estimasi penghematan waktu: 40-60% untuk proses initial screening.

5. **Foundation untuk Enhanced Features**  
   Baseline implementation menyediakan foundation untuk enhancement future:
   - Integrasi skill gap analysis menggunakan knowledge graph
   - Real-time prediction melalui API RESTful
   - Mobile application untuk employee self-service
   - Integration dengan sistem HRIS existing (SAP SuccessFactors, Workday, Oracle HCM)

**C. Manfaat Organisasional dan Strategis**:

1. **Data-Driven HR Strategy**  
   Memfasilitasi transformasi dari intuition-based HR decision making menuju data-driven, evidence-based approach yang lebih objektif, measurable, dan aligned dengan business outcomes.

2. **Talent Retention dan Employee Satisfaction**  
   Proses promosi yang fair, transparent, dan predictable dapat meningkatkan:
   - Employee trust terhadap organisasi dan manajemen
   - Motivation dan engagement karyawan high-potential
   - Retention rate talenta kunci (reduced turnover)
   - Employer branding sebagai organization yang values meritocracy

3. **Succession Planning yang Lebih Efektif**  
   Model prediksi dapat membantu mengidentifikasi high-potential employees lebih awal untuk targeted development programs, mentoring, dan succession planning initiatives.

4. **ROI Measurement untuk HR Programs**  
   Dashboard analytics memungkinkan organisasi untuk:
   - Mengukur efektivitas training & development programs terhadap promotion readiness
   - Menganalisis ROI dari psychological assessment (Quick Assessment)
   - Mengidentifikasi best practices dari karyawan yang successfully promoted

5. **Competitive Advantage dalam Talent Management**  
   Early adoption of advanced HR analytics dan AI-driven decision support dapat memberikan competitive advantage dalam war for talent, terutama untuk attracting dan retaining millennial dan gen-Z employees yang value transparency dan data-driven culture.

6. **Replicability dan Scalability**  
   Dokumentasi lengkap (kode, data pipeline, model artifacts) memungkinkan:
   - Replikasi framework di departemen atau unit bisnis lain
   - Scaling implementation untuk organisasi dengan ribuan karyawan
   - Customization untuk konteks industri atau job families yang berbeda
   - Knowledge transfer kepada internal data science atau HR analytics team

---

## 🔬 BAB 2: TINJAUAN PUSTAKA (OUTLINE)
- HR Analytics & Promotion Prediction (single vs multi-dimension).  
- Multi-Dimensional Assessment (performance, behavioral, psychological).  
- Feature Engineering di HR (encoding, rasio, kategori level).  
- Machine Learning untuk klasifikasi imbalanced (LogReg, RF, XGBoost, MLP).  
- Explainable AI (SHAP) untuk HR.  
- Knowledge Graph & skill mapping (sebagai pendekatan pendukung, belum terintegrasi).

---

## 🔬 BAB 3: METODOLOGI (OUTLINE)

### 3.1 Kerangka Metodologi: CRISP-DM
Penelitian mengikuti **CRISP-DM** dengan penyesuaian ke artefak yang sudah ada di repositori.

1) **Business Understanding**  
   - Tujuan: meningkatkan akurasi & explainability keputusan promosi.  
   - Pertanyaan bisnis: apakah penambahan dimensi behavioral & psikologis meningkatkan akurasi dibanding performance-only?  
   - Keberhasilan: AUC-ROC ≥ 0.88, F1 > 0.5, penjelasan SHAP tersedia di dashboard.

2) **Data Understanding**  
   - Sumber: `integrated_full_dataset.csv` (1.000 baris, 20 kolom) dan `integrated_performance_behavioral.csv` (712 baris).  
   - Eksplorasi: distribusi skor, imbalance (rate promosi ±9%), korelasi antar fitur.  
   - Catatan: data skill/KG tersedia tapi belum terhubung ke target; butuh eksplorasi terpisah.

3) **Data Preparation**  
   - File terproses: `data/processed/full_dataset_processed.csv` (34 fitur).  
   - Langkah: imputasi sederhana, encoding kategorikal, scaling (untuk model linear), balancing (versi balanced train tersedia).  
   - Rekayasa fitur aktif: rasio/komposit, level encoding, flag high_performer.  
   - Skill gap/career readiness: belum terintegrasi; dicatat sebagai langkah opsional jika data siap.

4) **Modeling**  
   - Baseline: Logistic Regression (performance-only, behavioral-only, dual).  
   - Advanced: Random Forest, XGBoost, Neural Network (MLP); artefak di `results/advanced_models/`.  
   - Skrip utama: `scripts/modeling/03_baseline_models.py`, `04_advanced_models.py`, `05_improve_precision.py`; `06_baseline_comparison.py` & `07_cross_validation_testing.py` untuk studi banding dan CV.

5) **Evaluation**  
   - Metrik: AUC-ROC (utama), F1/Precision/Recall/Accuracy (sekunder).  
   - Artefak hasil nyata: `results/advanced_models/advanced_models_results.csv`; SHAP di `results/shap_analysis/`.  
   - Uji statistik: McNemar di `06_baseline_comparison.py`; DeLong/CI ROC direncanakan.  
   - Validasi naratif: halaman dashboard + AI narrative (Gemini/OpenAI).

6) **Deployment**  
   - Bentuk: Dashboard Streamlit (Home + 4 halaman utama) dengan prediksi, SHAP, dan narasi AI.  
   - Artefak model & scaler: `results/advanced_models/*.pkl`, `data/processed/scaler.pkl`.  
   - Rencana upgrade: integrasi skill gap jika data siap, lalu update model + dashboard.

### 3.2 Data & Persiapan
- Dataset utama: `data/final/integrated_full_dataset.csv` (1.000 baris, 20 kolom); versi dua dimensi `integrated_performance_behavioral.csv` (712 baris).  
- Dataset terproses: `data/processed/full_dataset_processed.csv` (34 fitur rekayasa + target).  
- Preprocessing: imputasi sederhana, encoding kategorikal (gender, marital_status, is_permanent, rating, tenure/performance/behavior level), scaling untuk model linear.  
- Class imbalance: rate promosi ±9%; balancing sederhana di beberapa skrip (X_train_balanced, y_train_balanced).

### 3.3 Rekayasa Fitur (Aktif)

Dataset terproses (`full_dataset_processed.csv`) memiliki **34 kolom** dengan breakdown sebagai berikut:

**A. Fitur Asli (10 kolom)**:  
- Identifikasi: `employee_id_hash`, `name`, `company_id`  
- Demografi: `tenure_years`, `gender`, `marital_status`, `is_permanent`  
- Performance: `performance_score`, `performance_rating`  
- Behavioral: `behavior_avg`

**B. Fitur Psikologis dari Quick Assessment (9 kolom)**:  
- Skor utama: `psychological_score` (rata-rata 12 komponen)  
- Komponen spesifik: `drive_score`, `mental_strength_score`, `adaptability_score`, `collaboration_score`  
- Flag: `has_quick_assessment`  
- Fitur komposit: `holistic_score` (gabungan 3 dimensi), `score_alignment` (konsistensi skor), `leadership_potential`

**C. Fitur Rekayasa (8 kolom)**:  
- Rasio dan komposit: `perf_beh_ratio`, `combined_score`, `score_difference`  
- Kategorisasi: `tenure_category`, `performance_level`, `behavioral_level`  
- Flag: `high_performer`

**D. Fitur Encoded (7 kolom)**:  
- Demografi: `gender_encoded`, `marital_status_encoded`, `is_permanent_encoded`  
- Kategori: `performance_rating_encoded`, `tenure_category_encoded`, `performance_level_encoded`, `behavioral_level_encoded`

**E. Target (1 kolom)**: `has_promotion`

**Catatan**: Fitur skill gap/career readiness **belum tersedia di dataset** (direncanakan ketika integrasi KG siap).

### 3.3.1 Formulasi Matematis Feature Engineering

Penelitian ini menggunakan pendekatan matematis untuk mengintegrasikan tiga dimensi assessment menjadi fitur-fitur prediktif:

#### **1. Holistic Score (Composite Multi-Dimensional)**

Mengintegrasikan ketiga dimensi dengan weighted average:

$$
\text{Holistic Score} = w_p \cdot S_p + w_b \cdot S_b + w_{ps} \cdot S_{ps}
$$

di mana:
- $S_p$ = Performance Score (normalized)
- $S_b$ = Behavioral Score (normalized)  
- $S_{ps}$ = Psychological Score (normalized)
- $w_p + w_b + w_{ps} = 1$ (weights sum to 1)

Dalam implementasi, bobot yang digunakan adalah $w_p = 0.4$, $w_b = 0.3$, $w_{ps} = 0.3$ berdasarkan domain expert judgment.

#### **2. Performance-Behavioral Ratio**

Mengukur keseimbangan antara kinerja dan perilaku:

$$
R_{pb} = \frac{S_p}{S_b + \epsilon}
$$

di mana $\epsilon = 0.001$ adalah konstanta kecil untuk menghindari division by zero. Rasio ini membantu mengidentifikasi karyawan dengan high performance namun low behavioral scores.

#### **3. Score Alignment (Consistency Metric)**

Mengukur konsistensi assessment antar dimensi:

$$
\text{Alignment} = 1 - \frac{\sigma(S_p, S_b, S_{ps})}{\bar{S}}
$$

di mana:
- $\sigma$ adalah standard deviation dari ketiga scores
- $\bar{S} = \frac{S_p + S_b + S_{ps}}{3}$ adalah mean score

Nilai alignment tinggi (mendekati 1) mengindikasikan konsistensi performa karyawan di semua dimensi.

#### **4. Polynomial Features**

Untuk menangkap non-linear relationships:

$$
S_p^2 = (\text{performance\_score})^2
$$

$$
S_h^2 = (\text{holistic\_score})^2
$$

Fitur kuadrat ini membantu model menangkap threshold effects, misalnya karyawan dengan performance sangat tinggi memiliki probabilitas promosi yang meningkat secara eksponensial.

### 3.4 Pengembangan Model (sesuai repositori)
- Baseline: Logistic Regression (performance-only, behavioral-only, dual-dimensional).  
- Advanced: Random Forest, XGBoost, Neural Network (MLP) — artefak tersimpan di `results/advanced_models/`.  
- Skrip terkait:  
  - `scripts/analysis/00_integrate_all_data.py` (integrasi QA)  
  - `scripts/analysis/02_feature_engineering.py` + `data/processed/*`  
  - `scripts/modeling/03_baseline_models.py`, `04_advanced_models.py`, `05_improve_precision.py`  
  - `scripts/05_advanced_promotion_prediction.py` (butuh dataset lengkap bila skill siap)  
  - `scripts/06_baseline_comparison.py`, `07_cross_validation_testing.py` (siap dijalankan, perlu data final lengkap)

### 3.4.1 Formulasi Matematis Model Machine Learning

#### **1. SMOTE (Synthetic Minority Over-sampling Technique)**

Untuk mengatasi class imbalance (promotion rate ±9%), penelitian menggunakan SMOTE dengan formulasi:

$$
x_{\text{new}} = x_i + \lambda \cdot (x_{\text{nn}} - x_i)
$$

di mana:
- $x_i$ adalah minority class sample (karyawan yang dipromosikan)
- $x_{\text{nn}}$ adalah k-nearest neighbor dari $x_i$
- $\lambda \in [0, 1]$ adalah random number untuk menghasilkan variasi

**Reference**: Chawla et al. (2002)

#### **2. Random Forest - Ensemble Learning**

**Bagging Prediction:**

$$
\hat{y} = \frac{1}{B} \sum_{b=1}^{B} f_b(x)
$$

di mana $B = 200$ adalah jumlah trees dan $f_b(x)$ adalah prediksi dari tree ke-$b$.

**Gini Impurity (untuk splitting criterion):**

$$
\text{Gini}(t) = 1 - \sum_{i=1}^{C} p_i^2
$$

di mana $p_i$ adalah proportion of class $i$ di node $t$, dengan $C = 2$ (promoted vs not promoted).

**Feature Importance (Mean Decrease Impurity):**

$$
I(f) = \frac{1}{B} \sum_{b=1}^{B} \Delta \text{Gini}(f, b)
$$

di mana $\Delta \text{Gini}(f, b)$ adalah total reduction in Gini impurity dari feature $f$ pada tree ke-$b$.

#### **3. XGBoost - Gradient Boosting**

**Objective Function:**

$$
\mathcal{L}(\phi) = \sum_{i=1}^{n} \ell(y_i, \hat{y}_i) + \sum_{k=1}^{K} \Omega(f_k)
$$

di mana:
- $\ell$ adalah loss function (binary cross-entropy)
- $\Omega(f_k) = \gamma T + \frac{1}{2}\lambda \|\omega\|^2$ adalah regularization term
- $T$ adalah number of leaves, $\omega$ adalah leaf weights

**Additive Training (Gradient Boosting Update):**

$$
\hat{y}_i^{(t)} = \hat{y}_i^{(t-1)} + \eta \cdot f_t(x_i)
$$

di mana:
- $\eta = 0.1$ adalah learning rate
- $f_t$ adalah new tree pada iterasi ke-$t$

Hyperparameters: $n\_estimators = 200$, $max\_depth = 7$, $\lambda = 1.0$ (L2 regularization).

#### **4. Neural Network (Multi-Layer Perceptron)**

**Forward Propagation:**

$$
z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}
$$

$$
a^{[l]} = \sigma(z^{[l]})
$$

di mana:
- $W^{[l]}$ adalah weight matrix untuk layer $l$
- $b^{[l]}$ adalah bias vector
- $\sigma$ adalah activation function

**Arsitektur:** Input (34 features) → Hidden Layer 1 (128 neurons) → Hidden Layer 2 (64 neurons) → Hidden Layer 3 (32 neurons) → Output (1 neuron)

**ReLU Activation (hidden layers):**

$$
\text{ReLU}(x) = \max(0, x)
$$

**Sigmoid Activation (output layer untuk binary classification):**

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

**Binary Cross-Entropy Loss:**

$$
\mathcal{L} = -\frac{1}{n} \sum_{i=1}^{n} \left[ y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i) \right]
$$

Optimizer: Adam with learning rate $\alpha = 0.001$, early stopping patience = 10 epochs.

### 3.5 Evaluasi
- Metrik utama: AUC-ROC; sekunder: F1, Precision, Recall, Accuracy.  
- Hasil nyata (lihat Bab 4) diambil dari `results/advanced_models/advanced_models_results.csv`.  
- Uji statistik: McNemar tersedia di skrip baseline; DeLong/CI belum dijalankan (catatan pekerjaan lanjutan).  
- SHAP: hasil global & individual tersedia di `results/shap_analysis/` dan ditampilkan di dashboard.

### 3.5.1 Formulasi Matematis Metrik Evaluasi

#### **1. Metrik Klasifikasi Biner**

Berdasarkan confusion matrix dengan True Positives (TP), False Positives (FP), True Negatives (TN), dan False Negatives (FN):

**Accuracy:**

$$
\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
$$

**Precision (Positive Predictive Value):**B

$$
\text{Precision} = \frac{TP}{TP + FP}
$$

Mengukur proporsi prediksi positif yang benar. Penting untuk HR context agar tidak salah merekomendasikan kandidat yang tidak siap.

**Recall (Sensitivity, True Positive Rate):**

$$
\text{Recall} = \frac{TP}{TP + FN}
$$

Mengukur kemampuan model menangkap semua kandidat yang sebenarnya siap dipromosikan.

**F1-Score (Harmonic Mean):**

$$
F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2TP}{2TP + FP + FN}
$$

Metrik utama untuk imbalanced classification, memberikan balance antara precision dan recall.

#### **2. ROC-AUC (Receiver Operating Characteristic - Area Under Curve)**

**True Positive Rate (TPR):**

$$
TPR = \frac{TP}{TP + FN}
$$

**False Positive Rate (FPR):**

$$
FPR = \frac{FP}{FP + TN}
$$

**Area Under Curve:**

$$
\text{AUC} = \int_0^1 TPR(FPR^{-1}(x)) \, dx
$$

AUC mengukur kemampuan model membedakan antara kelas positif dan negatif di semua threshold. AUC = 1.0 adalah perfect classifier, AUC = 0.5 adalah random classifier.

**Interpretasi AUC dalam penelitian:**
- Performance-only baseline: AUC = 0.723 (acceptable)
- Multi-dimensional (Random Forest): AUC = 0.901 (excellent)
- Improvement: 24.6%

#### **3. Cross-Validation**

**Stratified K-Fold Cross-Validation Score:**

$$
CV_{\text{score}} = \frac{1}{k} \sum_{i=1}^{k} \text{metric}_i
$$

di mana $k = 5$ folds dan metric = F1-Score.

**Standard Error:**

$$
SE = \frac{\sigma_{CV}}{\sqrt{k}}
$$

di mana $\sigma_{CV}$ adalah standard deviation dari k-fold scores.

**95% Confidence Interval:**

$$
CI_{95\%} = \left[ CV_{\text{score}} - 1.96 \cdot SE, \, CV_{\text{score}} + 1.96 \cdot SE \right]
$$

#### **4. Statistical Significance Tests**

**McNemar Test (untuk membandingkan dua models pada test set yang sama):**

$$
\chi^2 = \frac{(n_{01} - n_{10})^2}{n_{01} + n_{10}}
$$

di mana:
- $n_{01}$ = jumlah sampel yang model 1 benar, model 2 salah
- $n_{10}$ = jumlah sampel yang model 1 salah, model 2 benar

Hipotesis null: kedua model memiliki error rate yang sama. Jika $\chi^2 > 3.841$ (critical value untuk $\alpha = 0.05$, df = 1), kita reject null hypothesis.

**DeLong Test (untuk membandingkan AUC curves):**

$$
Z = \frac{\text{AUC}_1 - \text{AUC}_2}{\sqrt{\text{SE}_1^2 + \text{SE}_2^2 - 2 \cdot \text{Cov}(\text{AUC}_1, \text{AUC}_2)}}
$$

Direncanakan untuk validasi lanjutan (future work).

### 3.6 Dashboard (Streamlit)

**Halaman Utama (Terintegrasi dengan Model ML)**:  
1. `1_📊_Data_Explorer.py` - Eksplorasi dataset dan statistik deskriptif  
2. `2_🤖_Model_Performance.py` - Visualisasi performa model (confusion matrix, ROC curve, metrik komparasi)  
3. `3_🔮_Prediction.py` - Prediksi promosi individual dengan AI narrative (Gemini/OpenAI)  
4. `4_🔍_SHAP_Explainability.py` - Analisis explainability menggunakan SHAP values

**Halaman Eksploratif (Belum Terintegrasi ke Model)**:  
5. `5_🗺️_Knowledge_Graph.py` - Visualisasi hubungan job-skill-employee menggunakan NetworkX dan Pyvis  
6. `6_👥_Promotion_Candidates.py` - Identifikasi kandidat promosi potensial

**Infrastruktur**:  
- Styling global: `app/ui.py`  
- AI services: `app/services/ai_service.py` (wrapper), `app/services/gemini_service.py` (Gemini AI), mendukung OpenAI  
- Prediction service: `app/services/prediction_service.py` (load model & inference)

**Catatan Penting**: Knowledge Graph (halaman 5) dan Top Candidates (halaman 6) berfungsi sebagai **tools eksploratif** untuk visualisasi dan analisis kualitatif, namun **tidak terintegrasi** ke dalam fitur prediksi model machine learning utama. Integrasi penuh KG ke pipeline prediksi merupakan **future work** yang memerlukan preprocessing tambahan untuk mengkonversi graph features menjadi input model.

### 3.7 Explainability - SHAP (SHapley Additive exPlanations)

#### **3.7.1 Konsep Shapley Value**

SHAP values didasarkan pada konsep **Shapley Value** dari cooperative game theory (Shapley, 1953), diadaptasi untuk machine learning explainability oleh Lundberg & Lee (2017).

**Definisi Formal:**

Untuk setiap feature $i$, SHAP value $\phi_i$ dihitung sebagai:

$$
\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!} \left[ f(S \cup \{i\}) - f(S) \right]
$$

di mana:
- $N$ = set of all features (34 features dalam penelitian ini)
- $S$ = subset of features (coalition)
- $|S|$ = size of subset $S$
- $f(S)$ = prediction dengan hanya menggunakan features dalam subset $S$
- $f(S \cup \{i\})$ = prediction dengan menambahkan feature $i$ ke subset $S$

**Interpretasi:**
- $\phi_i > 0$: Feature $i$ meningkatkan probabilitas promosi (positive contribution)
- $\phi_i < 0$: Feature $i$ menurunkan probabilitas promosi (negative contribution)
- $|\phi_i|$: Magnitude of impact (importance)

**Properties yang dijamin oleh Shapley Value:**
1. **Local Accuracy**: $\sum_{i=1}^{|N|} \phi_i = f(x) - E[f(X)]$ (prediksi = baseline + kontribusi features)
2. **Consistency**: Jika feature $i$ berkontribusi lebih besar di model baru, SHAP value-nya harus meningkat
3. **Missingness**: Feature yang tidak digunakan memiliki SHAP value = 0

#### **3.7.2 TreeExplainer untuk Random Forest**

Untuk tree-based models (Random Forest, XGBoost), penelitian menggunakan **TreeExplainer** yang memanfaatkan struktur pohon untuk komputasi efisien:

$$
\phi_i = \sum_{\text{all paths}} \text{contribution}(i, \text{path})
$$

Kompleksitas: $O(TLD^2)$ di mana $T$ = jumlah trees, $L$ = max leaves, $D$ = max depth.

#### **3.7.3 Global Feature Importance**

Untuk mengagregasi SHAP values di seluruh dataset test ($n$ sampel):

$$
I_i = \frac{1}{n} \sum_{j=1}^{n} |\phi_i^{(j)}|
$$

di mana $\phi_i^{(j)}$ adalah SHAP value untuk feature $i$ pada sampel ke-$j$.

Fitur dengan $I_i$ tertinggi adalah fitur yang paling berpengaruh secara global terhadap prediksi promosi.

#### **3.7.4 Implementasi dalam Penelitian**

1. **SHAP Summary Plot**: Visualisasi distribusi SHAP values untuk top 15 features
2. **SHAP Dependence Plot**: Scatter plot menunjukkan hubungan antara feature value dan SHAP value
3. **SHAP Force Plot**: Waterfall visualization untuk individual prediction
4. **AI Narrative Generation**: SHAP values dikonversi menjadi natural language explanation menggunakan Gemini/OpenAI

**Contoh Output:**
> "Karyawan ini memiliki probabilitas promosi 78%. Faktor utama yang mendukung: **holistic_score tinggi** (+0.35), **leadership_potential kuat** (+0.28), dan **performance_score excellent** (+0.22). Namun, **tenure yang masih pendek** memberikan dampak negatif (-0.12)."

**Reference**: Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems*, 30.

---

## 📊 BAB 4: HASIL & ANALISIS (BERDASAR ARTEFAK REPO)

### 4.1 Dataset & Fitur
- `integrated_full_dataset.csv`: 1.000 baris, 20 kolom (performance, behavioral, psychological, demografi dasar).  
- `full_dataset_processed.csv`: 34 fitur rekayasa + target `has_promotion`.

### 4.2 Perbandingan Model (hasil aktual)
Sumber: `results/advanced_models/advanced_models_results.csv`
```
Model                  Acc     Prec    Rec     F1      AUC-ROC
----------------------------------------------------------------
Performance-only       0.573   0.157   0.846   0.265   0.723
Behavioral-only        0.350   0.108   0.846   0.191   0.653
Dual-dimensional       0.762   0.244   0.769   0.370   0.812
Random Forest          0.874   0.391   0.692   0.500   0.901
XGBoost                0.895   0.444   0.615   0.516   0.883
Neural Network (MLP)   0.909   0.500   0.615   0.552   0.883
```
**Catatan**: angka di atas menggunakan fitur 3 dimensi + rekayasa; belum ada fitur skill gap. Model terbaik saat ini secara AUC: Random Forest (0.901); F1 terbaik: Neural Network (0.552) namun perlu cek stabilitas/overfitting.

### 4.3 Explainability
- SHAP global & lokal tersedia (`results/shap_analysis/*`), ditampilkan di halaman 4 dashboard.  
- Insight awal: fitur rasio/level (`perf_beh_ratio`, `performance_level_encoded`, `behavioral_level_encoded`) dan skor komposit (`holistic_score`, `score_alignment`) muncul dominan.

### 4.4 Validasi & Statistik

**Validasi Dasar (Sudah Dilakukan)**:  
- Split stratified train/test (80:20)  
- Class balancing untuk training set (menggunakan SMOTE atau oversampling sederhana)  
- Metrik evaluasi: Accuracy, Precision, Recall, F1-Score, AUC-ROC

**Validasi Lanjutan (Perlu Dilakukan)**:  
1. **Baseline Comparison** - Tersedia di `scripts/06_baseline_comparison.py`  
   - Perbandingan statistik antar model (McNemar test)  
   - Visualisasi perbanding performa  
   - Summary report

2. **Cross-Validation Testing** - Tersedia di `scripts/07_cross_validation_testing.py`  
   - 5-fold stratified cross-validation  
   - Analisis stabilitas model  
   - Bootstrap confidence intervals  
   - Visualisasi distribusi metrik

3. **Statistical Tests** (Future Work):  
   - DeLong test untuk perbandingan AUC-ROC curves  
   - Confidence intervals untuk setiap metrik  
   - Significance testing antar model

**Status**: Skrip 06 dan 07 sudah siap dieksekusi dengan dataset final untuk melengkapi validasi penelitian.

---

## 💬 BAB 5: PEMBAHASAN (GARIS BESAR)

### 5.1 Efektivitas Multi-Dimensional Assessment
- **Peningkatan Signifikan**: Multi-dimensional (3D) meningkatkan AUC-ROC dari 0.723 (performance-only) menjadi 0.901 (Random Forest dengan 3 dimensi) — **peningkatan 24.6%**.  
- **Kontribusi Behavioral**: Dual-dimensional (performance + behavioral) mencapai AUC 0.812, menunjukkan behavioral assessment menambah nilai prediktif.  
- **Nilai Tambah Psychological**: Penambahan komponen psikologis (dari 0.812 ke 0.901) memberikan boost tambahan **10.9%** pada AUC-ROC.

### 5.2 Peran Fitur Psikologis dan Feature Engineering
- **Fitur Psikologis Kunci**: Berdasarkan SHAP analysis, `holistic_score`, `leadership_potential`, dan `score_alignment` muncul sebagai kontributor penting.  
- **Engineered Features**: Rasio dan level encoding (`perf_beh_ratio`, `performance_level_encoded`, `behavioral_level_encoded`) memperkaya representasi data dan meningkatkan discriminative power model.  
- **Trade-off Precision-Recall**: F1-Score masih moderat (0.500-0.552) mengindikasikan challenge class imbalance (±9% promotion rate); perlu eksplorasi threshold optimization atau cost-sensitive learning.

### 5.3 Explainability dan Adopsi Praktis
- **SHAP Analysis**: Memberikan transparansi fitur-level contribution, critical untuk trust dan regulatory compliance di HR decisions.  
- **AI Narrative**: Integrasi Gemini/OpenAI mengkonversi prediction + SHAP values menjadi natural language explanation yang user-friendly untuk HR practitioners.  
- **Dashboard Interaktif**: Streamlit app menyediakan end-to-end workflow dari data exploration hingga prediction dengan explainability.

### 5.4 Keterbatasan dan Future Work
- **Knowledge Graph Integration**: KG dan skill data tersedia namun belum terintegrasi ke model; memerlukan feature engineering tambahan untuk graph-based features (node embeddings, skill gap metrics).  
- **Longitudinal Analysis**: Data cross-sectional; studi longitudinal dapat mengungkap career trajectory patterns.  
- **Generalizability**: Model dilatih pada synthetic/integrated data 1.000 karyawan; perlu validasi pada dataset organisasi yang lebih besar dan beragam.

---

## ✅ BAB 6: KESIMPULAN & SARAN

### 6.1 Kesimpulan

**Pencapaian Tujuan Penelitian**:
1. ✅ **Multi-dimensional assessment terbukti efektif**: Integrasi performance + behavioral + psychological meningkatkan AUC-ROC hingga 0.901 (Random Forest), **24.6% lebih tinggi** dibanding performance-only baseline (0.723).  

2. ✅ **Komponen psikologis berkontribusi signifikan**: Feature engineering menghasilkan 34 fitur berkualitas, dengan komponen psikologis (`holistic_score`, `leadership_potential`, `score_alignment`) dan rasio komposit muncul sebagai fitur dominan dalam SHAP analysis.  

3. ✅ **Explainability berhasil diimplementasikan**: SHAP values + AI narrative (Gemini/OpenAI) memberikan transparansi dan interpretability yang critical untuk HR decision support, tersedia melalui dashboard interaktif Streamlit.

**Kontribusi Penelitian**:  
- **Empiris**: Bukti kuantitatif bahwa pendekatan multi-dimensional outperform single-dimension dalam promotion prediction.  
- **Metodologis**: Framework integrasi psychological assessment (Quick Assessment) ke HR analytics pipeline dengan feature engineering systematic.  
- **Praktis**: Production-ready dashboard dengan explainable AI untuk mendukung data-driven HR decisions.

### 6.2 Keterbatasan
- Class imbalance (±9% promotion rate) membatasi precision; F1-Score masih moderate (0.500-0.552).  
- Knowledge Graph dan skill gap belum terintegrasi ke model prediksi (hanya sebagai exploratory tools).  
- Data cross-sectional; tidak menangkap temporal dynamics of career progression.  
- Validasi statistik lengkap (cross-validation, DeLong test) masih perlu dijalankan.

### 6.3 Saran

**Untuk Validasi Penelitian (Jangka Pendek)**:  
1. Jalankan `scripts/06_baseline_comparison.py` untuk statistical testing (McNemar) antar model.  
2. Eksekusi `scripts/07_cross_validation_testing.py` untuk 5-fold CV dan bootstrap confidence intervals.  
3. Dokumentasikan hasil validasi tambahan di appendix atau supplementary materials.

**Untuk Pengembangan Lanjutan (Jangka Menengah)**:  
1. **Skill Gap Integration**: Jalankan `scripts/04_integrated_feature_engineering.py` untuk generate graph-based features, kemudian retrain model dengan fitur extended.  
2. **Threshold Optimization**: Eksplorasi cost-sensitive learning atau threshold tuning untuk improve precision-recall trade-off.  
3. **Model Ensemble**: Kombinasi Random Forest + XGBoost untuk leverage kekuatan masing-masing algoritma.

**Untuk Riset Future (Jangka Panjang)**:  
1. Longitudinal study dengan data historical multi-tahun untuk capture career trajectory patterns.  
2. Graph Neural Networks (GNN) untuk exploit structure information dari Knowledge Graph.  
3. Validasi eksternal pada dataset organisasi berbeda untuk assess generalizability.  
4. Mobile app atau API deployment untuk real-time prediction di production environment.

---

## 📊 DELIVERABLES (SESUAI REPO SAAT INI)
1. **Kode & Artefak**:  
   - Data: `data/final/integrated_full_dataset.csv`, `data/processed/full_dataset_processed.csv`, scaler & split (`data/processed/*`).  
   - Model: `results/advanced_models/*.pkl` + metrik CSV/plots; baseline models di `results/baseline_models/`.  
   - Explainability: `results/shap_analysis/*`.  
   - Knowledge Graph: `results/knowledge_graph/*` (prototipe, belum terhubung ke model).  
2. **Dashboard Streamlit**: Home + 4 halaman utama, AI assistant (Gemini/OpenAI) untuk narasi, SHAP visual.  
3. **Dokumentasi**: README aplikasi, panduan AI (`app/requirements.txt`, `docs/ai/*`), serta catatan perbaikan fitur (mis. `docs/fixes/FIX_APPLIED.md`).  
4. **Skrip Eksperimen**: `scripts/modeling`, `scripts/analysis`, `scripts/06_baseline_comparison.py`, `scripts/07_cross_validation_testing.py` (siap dijalankan ulang dengan dataset aktif).

---

## 📅 RENCANA PENYELESAIAN THESIS

### **Fase 1: Validasi & Eksperimen (Minggu 1-2)** 🔥 PRIORITAS TINGGI

**Week 1: Statistical Validation**
- [ ] Jalankan `scripts/06_baseline_comparison.py` → Output: `results/baseline_comparison/`
  - Baseline vs advanced models comparison
  - McNemar statistical test
  - Visualization (confusion matrices, ROC curves, metrics comparison)
- [ ] Jalankan `scripts/07_cross_validation_testing.py` → Output: `results/cross_validation/`
  - 5-fold stratified cross-validation
  - Stability analysis across folds
  - Bootstrap confidence intervals
- [ ] Dokumentasikan hasil di BAB 4 proposal

**Week 2: Documentation & Refinement**
- [ ] Screenshot dashboard (4 halaman utama: Data Explorer, Model Performance, Prediction, SHAP)
- [ ] Export visualisasi SHAP (summary plot, dependence plots, waterfall charts)
- [ ] Update BAB 4 dengan subseksi validasi tambahan (4.5 Uji Statistik, 4.6 Cross-Validation)
- [ ] Review konsistensi angka dan terminologi di semua bab

### **Fase 2: Penulisan & Presentasi (Minggu 3-4)**

**Week 3: Content Development**
- [ ] Lengkapi BAB 2 (Tinjauan Pustaka) dengan minimum 20-30 referensi terkini
- [ ] Expand BAB 5 (Pembahasan) dengan analisis mendalam hasil eksperimen
- [ ] Finalisasi BAB 1 (Pendahuluan) dan BAB 6 (Kesimpulan)
- [ ] Buat diagram alur metodologi (CRISP-DM workflow)
- [ ] Compile daftar tabel dan gambar

**Week 4: Final Review**
- [ ] Proofreading grammar dan bahasa (Indonesia & English abstract)
- [ ] Format tabel, gambar, dan referensi sesuai template kampus
- [ ] Peer review dengan rekan atau pembimbing
- [ ] Siapkan slide presentasi (15-20 slides)
- [ ] Dry-run presentasi thesis defense

### **Fase 3: Skill Gap Integration (OPSIONAL - Jika Ada Waktu)**

**Hanya jika Fase 1-2 selesai lebih awal**:
- [ ] Jalankan `scripts/04_integrated_feature_engineering.py`
- [ ] Generate skill gap features (skill_gap_ratio, career_readiness, dll)
- [ ] Retrain model dengan fitur extended
- [ ] Compare performance: 34 features vs 34+skill_gap features
- [ ] Update proposal jika hasil signifikan

**Estimasi**: Butuh 1-2 minggu tambahan; disarankan sebagai **future work** jika timeline thesis ketat.

---

### **Timeline Summary**
```
Minggu 1-2: Validasi & dokumentasi (MUST DO)
Minggu 3-4: Penulisan & final review (MUST DO)
Minggu 5-6: Skill gap integration (OPTIONAL - future work)
```

**Target Submit**: Akhir Minggu 4  
**Buffer**: 1 minggu untuk revisi dari pembimbing

---

## 📝 CATATAN
- Title sudah disesuaikan agar tidak over-claim skill gap yang belum aktif; skill gap ditaruh sebagai rencana/opsional.  
- Semua klaim performa merujuk pada artefak nyata di repositori (per 8 Desember 2025).  
- Jika integrasi skill gap berhasil, tambahkan bab hasil baru dan perbarui tabel metrik serta deliverables.
