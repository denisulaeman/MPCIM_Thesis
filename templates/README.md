# 📋 DATA TEMPLATES - MPCIM

Template files untuk persiapan data MPCIM Knowledge Graph

---

## 📁 **FILES INCLUDED**

### **1. TEMPLATE_EMPLOYEE_DATA.csv**
Template untuk data karyawan dengan semua kolom yang diperlukan.

**Kolom Utama**:
- Basic info (ID, nama, department, tenure)
- Demographics (gender, marital status)
- Performance scores
- Behavioral scores
- Psychological scores (Quick Assessment)
- Promotion history

**Minimum**: 100 karyawan  
**Recommended**: 500-1,000 karyawan

---

### **2. TEMPLATE_JOB_POSITIONS.csv**
Template untuk definisi jabatan dan requirements.

**Kolom Utama**:
- Job info (ID, title, department, level)
- Minimum requirements (performance, behavior, psychological, leadership)
- Tenure range
- Description

**Minimum**: 5 jabatan  
**Recommended**: 10-15 jabatan

---

### **3. TEMPLATE_SKILLS.csv**
Template untuk daftar kompetensi/skills.

**Kolom Utama**:
- Skill info (ID, name, category)
- Importance level (1-5)
- Description

**Categories**: Technical, Soft, Leadership, Domain-specific

**Minimum**: 20 skills  
**Recommended**: 30-50 skills

---

### **4. TEMPLATE_EMPLOYEE_SKILLS.csv**
Template untuk mapping karyawan dengan skills mereka.

**Kolom Utama**:
- employee_id (link ke TEMPLATE_EMPLOYEE_DATA)
- skill_id (link ke TEMPLATE_SKILLS)
- proficiency (1-5)

**Minimum**: 5 skills per karyawan  
**Recommended**: 8-12 skills per karyawan

---

### **5. TEMPLATE_JOB_SKILL_REQUIREMENTS.csv**
Template untuk mapping jabatan dengan required skills.

**Kolom Utama**:
- job_id (link ke TEMPLATE_JOB_POSITIONS)
- skill_id (link ke TEMPLATE_SKILLS)
- min_proficiency (1-5)

**Minimum**: 5 skills per jabatan  
**Recommended**: 8-15 skills per jabatan

---

### **6. DATA_PREPARATION_GUIDE.md**
Panduan lengkap untuk persiapan data.

**Isi**:
- Overview & requirements
- Step-by-step workflow
- Validation checklist
- Tips & best practices
- Troubleshooting

---

## 🚀 **QUICK START**

### **Option 1: Use Sample Data** (For Testing)

Gunakan data yang sudah di-generate:
```bash
# Data sudah tersedia di:
data/knowledge_graph/
├── jobs.csv
├── skills.csv
├── employee_skills.csv
└── job_skill_requirements.csv

# Langsung run:
python scripts/knowledge_graph/build_graph.py
streamlit run app/Home.py
```

---

### **Option 2: Use Your Own Data** (For Production)

1. **Download Templates**
   - Copy semua TEMPLATE_*.csv files
   - Buka dengan Excel/Google Sheets

2. **Fill Data**
   - Isi sesuai instruksi di setiap file
   - Lihat contoh data yang sudah ada
   - Validasi dengan checklist

3. **Place Files**
   ```
   # Employee data:
   data/final/integrated_full_dataset.csv
   
   # Knowledge graph data:
   data/knowledge_graph/
   ├── jobs.csv
   ├── skills.csv
   ├── employee_skills.csv
   └── job_skill_requirements.csv
   ```

4. **Run Scripts**
   ```bash
   # Build graph
   python scripts/knowledge_graph/build_graph.py
   
   # Test
   python scripts/testing/test_knowledge_graph.py
   
   # Run app
   streamlit run app/Home.py
   ```

---

## 📊 **DATA REQUIREMENTS**

### **Minimum (For Testing)**
- 50-100 karyawan
- 5-10 jabatan
- 20-30 skills
- 300-500 employee-skill mappings
- 50-100 job-skill requirements

### **Recommended (For Thesis/Production)**
- 500-1,000 karyawan ⭐
- 10-15 jabatan
- 30-50 skills
- 3,000-10,000 employee-skill mappings
- 100-200 job-skill requirements

---

## ✅ **VALIDATION CHECKLIST**

Before running the system, validate:

- [ ] All employee_id are unique
- [ ] All job_id are unique
- [ ] All skill_id are unique
- [ ] All IDs referenced exist in their respective files
- [ ] Scores are in valid range (0-100)
- [ ] Proficiency levels are 1-5
- [ ] No missing values in required columns
- [ ] File encoding is UTF-8
- [ ] Separator is comma (,)

---

## 💡 **TIPS**

### **Data Quality**
1. Start with clean, accurate data
2. Validate before importing
3. Test with small dataset first
4. Scale up gradually

### **Privacy**
1. Anonymize employee names if needed
2. Remove sensitive information
3. Use hashed IDs

### **Performance**
1. Start with 100 employees for testing
2. Monitor performance when scaling
3. Optimize if needed

---

## 🆘 **NEED HELP?**

**Read**:
- `DATA_PREPARATION_GUIDE.md` - Complete guide
- `../IMPLEMENTATION_COMPLETE.md` - System overview
- `../KNOWLEDGE_GRAPH_ROADMAP.md` - Implementation details

**Check Examples**:
- `../data/final/sample_dataset_1000_balanced.csv` - Sample employee data
- `../data/knowledge_graph/*.csv` - Generated sample data

**Run Tests**:
```bash
python scripts/testing/test_knowledge_graph.py
```

---

## 📞 **SUPPORT**

Jika ada pertanyaan:
1. Check documentation files
2. Review sample data
3. Run validation tests
4. Contact thesis supervisor

---

**Good luck with your data preparation!** 📊✨

**Remember**: Quality data = Quality results! 🎯
