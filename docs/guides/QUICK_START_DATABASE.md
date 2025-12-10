# 🚀 Quick Start: Database Integration

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install sqlalchemy psycopg2-binary python-dotenv
```

### 2. Create Thesis Database
```bash
psql -U postgres -c "CREATE DATABASE mpcim_thesis;"
```

### 3. Run Setup
```bash
python scripts/database/setup_dual_database.py
```

### 4. Test Connection
Script akan otomatis:
- ✅ Test koneksi ke source DB (port 5433)
- ✅ Test koneksi ke thesis DB (port 5432)
- ✅ Show available tables
- ✅ Display sample data

### 5. Configure Mapping

Edit `scripts/database/test_data_sync.py`:

```python
SOURCE_TABLE = 'your_employee_table_name'  # From step 3 output

COLUMN_MAPPING = {
    'your_id_column': 'employee_id',
    'your_name_column': 'name',
    # ... add more based on your schema
}
```

### 6. Test Sync (Dry Run)
```bash
python scripts/database/test_data_sync.py
```

Review output, verify data looks correct.

### 7. Sync Data
```bash
python scripts/database/sync_employees.py
```

Type `yes` to confirm.

---

## ✅ Done!

Your data is now synced. Next:

1. **View data:**
   ```python
   from app.database import db_manager, EmployeeRepository
   
   with db_manager.get_session() as session:
       employees = EmployeeRepository.get_all(session)
       print(f"Total: {len(employees)}")
   ```

2. **Update Streamlit** to use database instead of CSV

3. **Log predictions** to database for monitoring

---

## 📖 Full Documentation

- **Detailed Guide**: `docs/EXISTING_DATABASE_INTEGRATION.md`
- **Database Schema**: `app/database/schema.sql`
- **API Reference**: `docs/DATABASE_INTEGRATION.md`

---

## 🆘 Need Help?

**Common Issues:**

1. **Can't connect to source DB**
   - Check PostgreSQL is running: `brew services list`
   - Verify port 5433: `psql -U postgres -p 5433 -l`

2. **Permission denied**
   - Grant read access: `GRANT SELECT ON ALL TABLES IN SCHEMA public TO postgres;`

3. **Column not found**
   - Run setup script again to see actual column names
   - Update COLUMN_MAPPING accordingly

4. **Thesis DB not created**
   - Run: `psql -U postgres -c "CREATE DATABASE mpcim_thesis;"`

---

**Questions?** Check the full documentation or review script output for guidance.
