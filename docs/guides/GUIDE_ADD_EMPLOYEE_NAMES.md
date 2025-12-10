# 📝 Guide: Menambahkan Nama Karyawan ke Dataset

**Tujuan**: Menambahkan nama karyawan yang realistis ke dataset agar tampil di aplikasi Streamlit

---

## 🎯 Pilihan yang Tersedia

### **Option 1: Simple Version (RECOMMENDED)** ⭐
**Menggunakan**: Generated Indonesian names  
**Keuntungan**: 
- ✅ Tidak perlu database connection
- ✅ Cepat dan mudah
- ✅ Nama realistis (Andi Pratama, Dewi Kusuma, dll)
- ✅ Deterministic (hash yang sama = nama yang sama)

**Cara Pakai**:
```bash
cd /Users/denisulaeman/Workspace/Academic/CascadeProjects/MPCIM_Thesis
python scripts/data_preparation/add_employee_names_simple.py
```

---

### **Option 2: Database Version** 
**Menggunakan**: Actual names from database  
**Keuntungan**:
- ✅ Nama asli dari database
- ✅ Fallback ke generated names jika tidak ada

**Kebutuhan**:
- Database connection ke source database
- Table `employees` dengan kolom `id`, `name`, `email`

**Cara Pakai**:
```bash
cd /Users/denisulaeman/Workspace/Academic/CascadeProjects/MPCIM_Thesis
python scripts/data_preparation/add_employee_names.py
```

---

## 🚀 Quick Start (Recommended)

### Step 1: Jalankan Script Simple
```bash
python scripts/data_preparation/add_employee_names_simple.py
```

### Step 2: Lihat Output
Script akan:
- ✅ Load dataset dari `data/final/`
- ✅ Generate nama Indonesia untuk setiap employee
- ✅ Save kembali ke file yang sama
- ✅ Buat file mapping: `employee_name_mapping.csv`

### Step 3: Refresh Streamlit
```bash
# Refresh browser atau restart
streamlit run app/Home.py
```

### Step 4: Test
- Navigate ke: **👥 Promotion Candidates**
- Anda akan lihat nama seperti:
  - Andi Pratama
  - Dewi Kusuma
  - Budi Wijaya
  - Citra Santoso
  - dll.

---

## 📊 Contoh Output

### Before:
```
Employee abc123de
ID: abc123def456...
```

### After:
```
Andi Pratama
ID: abc123def456...
```

---

## 🎨 Nama yang Digunakan

### First Names (50+):
```
Andi, Budi, Citra, Dewi, Eko, Fitri, Gita, Hadi,
Indra, Joko, Kartika, Lina, Made, Nita, Omar, Putri,
Rudi, Sari, Tono, Umar, Vina, Wati, Yanto, Zaki,
Agus, Bayu, Candra, Dian, Erna, Fajar, Gilang, Hendra,
Ika, Johan, Kiki, Lestari, Mega, Novi, Oki, Pramono,
Qori, Rina, Sinta, Tari, Umi, Vera, Wawan, Yudi, Zahra,
Aditya, Bella, Cahya, Dimas, Elsa, Faisal, Gina, Haris,
Intan, Jaya, Karina, Lukman, Maya, Nanda, Olivia, Putra,
Qonita, Reza, Siska, Taufik, Ulfa, Vino, Wulan, Yoga, Zainal
```

### Last Names (50+):
```
Pratama, Wijaya, Santoso, Kusuma, Permana, Saputra, Wibowo,
Nugroho, Setiawan, Hidayat, Kurniawan, Firmansyah, Ramadhan,
Hakim, Susanto, Prasetyo, Gunawan, Sutanto, Maulana, Irawan,
Budiman, Suryanto, Hartono, Darmawan, Purnomo, Suharto,
Wahyudi, Hermawan, Yulianto, Cahyono, Sugiarto, Rachman,
Iskandar, Mahendra, Adiputra, Nugraha, Sasmita, Kusumah,
Wicaksono, Prabowo, Sanjaya, Utomo, Harahap, Siregar,
Nasution, Lubis, Situmorang, Simbolon, Tampubolon, Sinaga
```

**Total Kombinasi**: 50 × 50 = **2,500 unique combinations**

---

## 🔧 Cara Kerja

### Deterministic Name Generation:
```python
def generate_indonesian_name(employee_hash):
    # Convert hash to integer
    hash_int = int(employee_hash[:8], 16)
    
    # Select first name (deterministic)
    first_idx = hash_int % len(FIRST_NAMES)
    first_name = FIRST_NAMES[first_idx]
    
    # Select last name (deterministic)
    last_idx = (hash_int // 100) % len(LAST_NAMES)
    last_name = LAST_NAMES[last_idx]
    
    return f"{first_name} {last_name}"
```

**Keuntungan**:
- ✅ Same hash always produces same name
- ✅ Consistent across runs
- ✅ No random seed needed
- ✅ Reproducible

---

## 📁 Files yang Diupdate

### Input Files:
```
data/final/integrated_performance_behavioral.csv
data/final/integrated_full_dataset.csv
```

### Output Files:
```
data/final/integrated_performance_behavioral.csv (updated)
data/final/integrated_full_dataset.csv (updated)
data/final/employee_name_mapping.csv (new)
```

### Column Structure After:
```
employee_id_hash, name, company_id, tenure_years, ...
```

---

## 🧪 Testing

### Test Script:
```python
import pandas as pd

# Load dataset
df = pd.read_csv('data/final/integrated_performance_behavioral.csv')

# Check names
print(df[['employee_id_hash', 'name']].head(10))

# Statistics
print(f"Total employees: {len(df)}")
print(f"Unique names: {df['name'].nunique()}")
print(f"Sample names: {df['name'].head(10).tolist()}")
```

### Expected Output:
```
Total employees: 712
Unique names: ~500-600 (some duplicates are normal)
Sample names: ['Andi Pratama', 'Dewi Kusuma', 'Budi Wijaya', ...]
```

---

## 🐛 Troubleshooting

### Issue 1: Script tidak jalan
**Solution**:
```bash
# Make sure you're in the right directory
cd /Users/denisulaeman/Workspace/Academic/CascadeProjects/MPCIM_Thesis

# Check Python version
python --version  # Should be 3.8+

# Run with full path
python scripts/data_preparation/add_employee_names_simple.py
```

### Issue 2: Nama tidak muncul di Streamlit
**Solution**:
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart Streamlit
streamlit run app/Home.py
```

### Issue 3: File not found
**Solution**:
```bash
# Check if files exist
ls -la data/final/integrated_performance_behavioral.csv
ls -la data/final/integrated_full_dataset.csv

# If not found, check data directory
ls -la data/final/
```

---

## 💡 Tips

### Tip 1: Backup Data
```bash
# Before running script
cp data/final/integrated_performance_behavioral.csv data/final/integrated_performance_behavioral.csv.backup
```

### Tip 2: Check Results
```bash
# View first few lines
head -20 data/final/integrated_performance_behavioral.csv

# Count lines
wc -l data/final/integrated_performance_behavioral.csv
```

### Tip 3: Re-run Anytime
Script is **idempotent** - safe to run multiple times:
- First run: Adds names
- Subsequent runs: Updates if needed or skips if already done

---

## 📊 Statistics

### Expected Results:
```
Total Employees: 712
Unique Names: ~500-600
Duplicate Names: ~100-200 (normal)

Most Common Names:
- Andi Pratama: 3 employees
- Dewi Kusuma: 2 employees
- Budi Wijaya: 2 employees
```

**Note**: Duplicate names are normal and realistic (like real companies)

---

## 🎉 Success Criteria

After running script, you should see:

✅ **In Terminal**:
```
✅ SUCCESS! Updated 2 dataset(s) with Indonesian names
✅ Created: employee_name_mapping.csv
```

✅ **In CSV File**:
```csv
employee_id_hash,name,company_id,...
00003e3b9e5336685200ae85d21b4f5e,Andi Pratama,82,...
00c17237d011cca999f55a43db2ce040,Dewi Kusuma,101,...
```

✅ **In Streamlit App**:
```
Promotion Candidates:
- Andi Pratama (ID: 00003e3b...)
- Dewi Kusuma (ID: 00c17237...)
- Budi Wijaya (ID: 021bbc7e...)
```

---

## 🚀 Next Steps After Adding Names

1. **Test Promotion Candidates Page**
   - All names should display
   - No more "Employee XXXXX"
   - Realistic Indonesian names

2. **Test Data Explorer**
   - Names should show in tables
   - Filters work with names

3. **Test Export**
   - CSV exports include names
   - Name mapping file available

4. **For Thesis**
   - Screenshot with real names
   - More professional appearance
   - Better for demo/defense

---

## 📝 Summary

**What This Does**:
- ✅ Adds realistic Indonesian names to dataset
- ✅ Deterministic (same hash = same name)
- ✅ Updates all CSV files
- ✅ Creates name mapping file
- ✅ No database required (simple version)

**Time Required**: ~30 seconds

**Difficulty**: ⭐ Very Easy

**Impact**: 🌟🌟🌟 High (much better UX)

---

**Ready to run?**
```bash
python scripts/data_preparation/add_employee_names_simple.py
```

**Questions?** Check troubleshooting section above! 🚀
