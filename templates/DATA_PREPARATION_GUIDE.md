# 📋 PANDUAN PERSIAPAN DATA UNTUK MPCIM

**Tanggal**: December 8, 2025  
**Untuk**: Implementasi MPCIM Knowledge Graph

---

## 🎯 **OVERVIEW**

Untuk menggunakan sistem MPCIM dengan data real Anda, perlu menyiapkan 5 file CSV:

1. **TEMPLATE_EMPLOYEE_DATA.csv** - Data karyawan
2. **TEMPLATE_JOB_POSITIONS.csv** - Daftar jabatan
3. **TEMPLATE_SKILLS.csv** - Daftar kompetensi
4. **TEMPLATE_EMPLOYEE_SKILLS.csv** - Mapping karyawan-skill
5. **TEMPLATE_JOB_SKILL_REQUIREMENTS.csv** - Mapping jabatan-skill

---

## 📊 **MINIMUM DATA REQUIREMENTS**

### **Untuk Testing/Demo**
- Karyawan: 50-100 orang
- Jabatan: 5-10 posisi
- Skills: 20-30 kompetensi
- Employee-Skills: 300-500 mappings
- Job-Skills: 50-100 requirements

### **Untuk Production/Thesis**
- Karyawan: 500-1,000 orang ⭐ **Recommended**
- Jabatan: 10-15 posisi
- Skills: 30-50 kompetensi
- Employee-Skills: 3,000-10,000 mappings
- Job-Skills: 100-200 requirements

---

## 🔄 **WORKFLOW PERSIAPAN DATA**

### **Step 1: Kumpulkan Data Karyawan** 📝

**Sumber Data**:
- HR Database / HRIS
- Performance Review Records
- Quick Assessment Results (jika ada)
- Employee Master Data

**Data yang Dibutuhkan**:
```
✅ Basic Info: ID, Nama, Department, Tenure
✅ Demographics: Gender, Marital Status, Employment Type
✅ Performance: Score, Rating
✅ Behavioral: Average Score
✅ Psychological: Quick Assessment scores (opsional)
✅ Promotion History: Has been promoted or not
```

**Template**: `TEMPLATE_EMPLOYEE_DATA.csv`

---

### **Step 2: Definisikan Job Positions** 💼

**Cara Mendefinisikan**:
1. List semua jabatan dalam organisasi
2. Tentukan level (junior/mid/senior/supervisor/manager)
3. Tentukan minimum requirements per jabatan
4. Pastikan ada career path yang jelas

**Minimum Requirements per Jabatan**:
- Performance score minimum
- Behavioral score minimum
- Psychological score minimum
- Leadership potential minimum
- Tenure range

**Template**: `TEMPLATE_JOB_POSITIONS.csv`

---

### **Step 3: Buat Skills Taxonomy** 🎯

**Kategori Skills**:

1. **Technical Skills** (30-40%)
   - Programming languages
   - Tools & software
   - Domain-specific technical skills

2. **Soft Skills** (30-40%)
   - Communication
   - Teamwork
   - Problem solving
   - Time management

3. **Leadership Skills** (20-30%)
   - Team leadership
   - Strategic thinking
   - Decision making
   - Change management

4. **Domain Skills** (opsional)
   - HR-specific
   - Finance-specific
   - Operations-specific

**Template**: `TEMPLATE_SKILLS.csv`

---

### **Step 4: Map Employee Skills** 🗺️

**Sumber Data**:
- Performance review
- Self-assessment
- Manager assessment
- Training records
- Certification records

**Proficiency Levels**:
- 1 = Beginner
- 2 = Elementary
- 3 = Intermediate
- 4 = Advanced
- 5 = Expert

**Cara Cepat**:
Jika tidak ada data detail, gunakan performance score sebagai proxy:
- Performance 90-100 → proficiency rata-rata 4-5
- Performance 80-90 → proficiency rata-rata 3-4
- Performance 70-80 → proficiency rata-rata 2-3
- Performance <70 → proficiency rata-rata 1-2

**Template**: `TEMPLATE_EMPLOYEE_SKILLS.csv`

---

### **Step 5: Define Job Requirements** 📋

**Untuk Setiap Jabatan**:
1. List skills yang dibutuhkan
2. Tentukan minimum proficiency per skill
3. Prioritize critical skills (importance 4-5)

**Guidelines**:
- Junior: 5-8 skills, proficiency 2-3
- Mid: 8-10 skills, proficiency 3-4
- Senior: 10-12 skills, proficiency 4
- Supervisor: 12-14 skills, proficiency 4-5
- Manager: 14-16 skills, proficiency 4-5

**Template**: `TEMPLATE_JOB_SKILL_REQUIREMENTS.csv`

---

## 🛠️ **TOOLS & METHODS**

### **Method 1: Manual Entry** (Small Dataset)

**Untuk**: 50-100 karyawan

**Steps**:
1. Buka template CSV di Excel/Google Sheets
2. Isi data satu per satu
3. Validasi dengan checklist
4. Export sebagai CSV

**Time**: 2-4 jam

---

### **Method 2: Export dari HRIS** (Recommended)

**Untuk**: 100+ karyawan

**Steps**:
1. Export data dari HRIS/HR Database
2. Map kolom ke template format
3. Clean & transform data
4. Validate & import

**Time**: 1-2 jam

---

### **Method 3: Generate Sample Data** (For Testing)

**Untuk**: Testing/Demo purposes

**Steps**:
1. Gunakan script yang sudah ada:
   ```bash
   python scripts/knowledge_graph/create_sample_data.py
   ```
2. Modify parameters sesuai kebutuhan
3. Generate data otomatis

**Time**: 5 menit

---

## ✅ **DATA VALIDATION CHECKLIST**

### **Employee Data** ✅
- [ ] Semua employee_id unik
- [ ] Tidak ada missing values di kolom wajib
- [ ] Performance score 0-100
- [ ] Behavior score 0-100
- [ ] Performance rating sesuai dengan score
- [ ] Tenure years > 0
- [ ] Gender valid (M/F/O)
- [ ] Marital status valid
- [ ] is_permanent valid (t/f)

### **Job Positions** ✅
- [ ] Semua job_id unik
- [ ] Level valid (junior/mid/senior/supervisor/manager)
- [ ] Min scores realistis (60-95)
- [ ] Tenure range masuk akal
- [ ] Ada career path progression

### **Skills** ✅
- [ ] Semua skill_id unik
- [ ] Category valid (Technical/Soft/Leadership/Domain-XX)
- [ ] Importance 1-5
- [ ] Skill name jelas & spesifik

### **Employee-Skills** ✅
- [ ] Semua employee_id ada di Employee Data
- [ ] Semua skill_id ada di Skills
- [ ] Proficiency 1-5
- [ ] Setiap employee minimal 5 skills
- [ ] Tidak ada duplicate (employee_id + skill_id)

### **Job-Skills** ✅
- [ ] Semua job_id ada di Job Positions
- [ ] Semua skill_id ada di Skills
- [ ] Min proficiency 1-5
- [ ] Setiap job minimal 5 skills
- [ ] Tidak ada duplicate (job_id + skill_id)

---

## 🚀 **AFTER DATA PREPARATION**

### **Step 1: Place Files**

Copy semua CSV files ke folder:
```
data/final/
├── integrated_full_dataset.csv (dari TEMPLATE_EMPLOYEE_DATA.csv)
└── ...

data/knowledge_graph/
├── jobs.csv (dari TEMPLATE_JOB_POSITIONS.csv)
├── skills.csv (dari TEMPLATE_SKILLS.csv)
├── employee_skills.csv (dari TEMPLATE_EMPLOYEE_SKILLS.csv)
└── job_skill_requirements.csv (dari TEMPLATE_JOB_SKILL_REQUIREMENTS.csv)
```

### **Step 2: Run Scripts**

```bash
# 1. Feature Engineering (jika ada data baru)
python scripts/analysis/02_feature_engineering.py

# 2. Build Knowledge Graph
python scripts/knowledge_graph/build_graph.py

# 3. Test
python scripts/testing/test_knowledge_graph.py

# 4. Run App
streamlit run app/Home.py
```

---

## 💡 **TIPS & BEST PRACTICES**

### **Data Quality**
1. ✅ **Consistency**: Pastikan format data konsisten
2. ✅ **Completeness**: Minimal missing values
3. ✅ **Accuracy**: Data harus akurat & up-to-date
4. ✅ **Validity**: Nilai dalam range yang valid

### **Data Privacy**
1. 🔒 **Anonymize**: Hash employee names jika perlu
2. 🔒 **Remove PII**: Hapus data sensitif (NIK, alamat, dll)
3. 🔒 **Aggregate**: Gunakan aggregated data jika perlu

### **Performance**
1. ⚡ **Start Small**: Test dengan 100 karyawan dulu
2. ⚡ **Scale Up**: Tambah data bertahap
3. ⚡ **Optimize**: Monitor performance saat scale up

---

## 🆘 **TROUBLESHOOTING**

### **Problem: Data tidak load**

**Solution**:
1. Check file encoding (harus UTF-8)
2. Check separator (harus comma)
3. Check file path
4. Check column names (harus exact match)

### **Problem: Graph build error**

**Solution**:
1. Validate semua IDs ada
2. Check for duplicates
3. Validate data types
4. Check for missing values

### **Problem: No qualified matches**

**Solution**:
1. Lower minimum requirements
2. Check employee scores
3. Verify skill mappings
4. Adjust proficiency levels

---

## 📞 **SUPPORT**

Jika ada pertanyaan atau masalah:

1. **Check Documentation**:
   - `IMPLEMENTATION_COMPLETE.md`
   - `KNOWLEDGE_GRAPH_ROADMAP.md`

2. **Check Examples**:
   - Sample data di `data/final/sample_dataset_1000_balanced.csv`
   - Generated data di `data/knowledge_graph/`

3. **Run Tests**:
   ```bash
   python scripts/testing/test_knowledge_graph.py
   ```

---

## 🎯 **QUICK START CHECKLIST**

- [ ] Download semua template files
- [ ] Kumpulkan data karyawan dari HRIS
- [ ] Isi TEMPLATE_EMPLOYEE_DATA.csv
- [ ] Definisikan jabatan di TEMPLATE_JOB_POSITIONS.csv
- [ ] Buat skills taxonomy di TEMPLATE_SKILLS.csv
- [ ] Map employee skills di TEMPLATE_EMPLOYEE_SKILLS.csv
- [ ] Define job requirements di TEMPLATE_JOB_SKILL_REQUIREMENTS.csv
- [ ] Validate semua data
- [ ] Copy files ke folder yang sesuai
- [ ] Run build_graph.py
- [ ] Test dengan test_knowledge_graph.py
- [ ] Run Streamlit app
- [ ] Explore & enjoy! 🎉

---

**Good luck with your data preparation!** 📊✨
