# 🔗 Integrasi dengan Database Existing (DigiSpace CNA)

## 📋 Overview

Panduan lengkap untuk mengintegrasikan aplikasi MPCIM Thesis dengan database existing **db_digispace_cna_augustus_182025**.

**Arsitektur:**
```
┌─────────────────────────────────────────────────────┐
│         MPCIM Thesis Application                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  SOURCE DB (DigiSpace CNA)                          │
│  ├─ Host: localhost:5433                           │
│  ├─ Database: db_digispace_cna_augustus_182025     │
│  ├─ Access: READ-ONLY                              │
│  └─ Purpose: Employee master data                  │
│                                                     │
│  THESIS DB (MPCIM)                                  │
│  ├─ Host: localhost:5432                           │
│  ├─ Database: mpcim_thesis                         │
│  ├─ Access: READ-WRITE                             │
│  └─ Purpose: Predictions, logs, analysis           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Keuntungan Dual Database Approach

### ✅ **Advantages**

1. **Safety First**
   - Source database tetap aman (read-only)
   - Tidak ada risiko mengubah data production
   - Rollback mudah jika ada masalah

2. **Separation of Concerns**
   - Data source vs analytics terpisah
   - Performa source DB tidak terpengaruh
   - Bisa optimize thesis DB untuk analytics

3. **Flexibility**
   - Sync data sesuai kebutuhan (daily, weekly)
   - Bisa filter data yang di-sync
   - Bisa tambah kolom di thesis DB tanpa ubah source

4. **Research Value**
   - Historical tracking (predictions over time)
   - Model monitoring & drift detection
   - A/B testing support

---

## 🚀 Setup Guide

### Step 1: Install Dependencies

```bash
pip install sqlalchemy psycopg2-binary python-dotenv
```

### Step 2: Configure Environment

File `.env` sudah dikonfigurasi dengan:

```bash
# SOURCE DATABASE (DigiSpace CNA - Read Only)
SOURCE_DB_HOST=localhost
SOURCE_DB_PORT=5433
SOURCE_DB_DATABASE=db_digispace_cna_augustus_182025
SOURCE_DB_USERNAME=postgres
SOURCE_DB_PASSWORD=

# THESIS DATABASE (MPCIM - Read/Write)
THESIS_DATABASE_URL=postgresql://postgres:@localhost:5432/mpcim_thesis
```

### Step 3: Create Thesis Database

```bash
# Option 1: Using psql
psql -U postgres -c "CREATE DATABASE mpcim_thesis;"

# Option 2: Using pgAdmin
# 1. Open pgAdmin
# 2. Right-click Databases -> Create -> Database
# 3. Name: mpcim_thesis
```

### Step 4: Run Setup Script

```bash
python scripts/database/setup_dual_database.py
```

**Script ini akan:**
1. ✅ Test koneksi ke kedua database
2. ✅ Initialize thesis database (create tables)
3. ✅ Discover source database schema
4. ✅ Identify employee-related tables
5. ✅ Show sample data
6. ✅ Provide next steps

**Expected Output:**
```
================================================================================
MPCIM THESIS - DUAL DATABASE SETUP
================================================================================

STEP 1: TESTING DATABASE CONNECTIONS
================================================================================

SOURCE DATABASE (DigiSpace CNA):
--------------------------------------------------------------------------------
✅ Connected
   Version: PostgreSQL 14.x
   Tables: 25
   Available tables: employees, departments, positions...

THESIS DATABASE (MPCIM):
--------------------------------------------------------------------------------
✅ Connected
   URL: postgresql://postgres@localhost:5432/...

STEP 2: INITIALIZING THESIS DATABASE
================================================================================

Creating tables...
✅ Thesis database initialized

STEP 3: DISCOVERING SOURCE DATABASE SCHEMA
================================================================================

✅ Found 25 tables in source database

Available tables:
--------------------------------------------------------------------------------
  ⭐ employees                                    1,234 rows,  25 columns
  ⭐ performance_reviews                            567 rows,  15 columns
     departments                                     12 rows,   5 columns
     positions                                       45 rows,   8 columns
     ...

📊 Found 2 employee-related tables:
   - employees
   - performance_reviews

Detailed info for "employees":
--------------------------------------------------------------------------------
Columns (25):
  - id                            integer              (required)
  - name                          varchar              (required)
  - email                         varchar              (nullable)
  - department_id                 integer              (nullable)
  - position_id                   integer              (nullable)
  - performance_score             numeric              (nullable)
  - behavioral_score              numeric              (nullable)
  ...
```

### Step 5: Configure Column Mapping

Edit `app/database/data_sync.py`:

```python
self.source_table_mapping = {
    'employees': {
        # Map your actual column names
        'id': 'employee_id',
        'name': 'name',
        'email': 'email',
        'department_id': 'department',  # Will need to join with departments table
        'performance_score': 'performance_score',
        'behavioral_score': 'behavioral_score',
        # Add more mappings based on your schema
    }
}
```

### Step 6: Test Sync (Dry Run)

```bash
python scripts/database/test_data_sync.py
```

**Edit script first** to match your table/column names:

```python
SOURCE_TABLE = 'employees'  # Your actual table name

COLUMN_MAPPING = {
    'id': 'employee_id',
    'name': 'name',
    # ... add your mappings
}
```

**Expected Output:**
```
================================================================================
MPCIM THESIS - DATA SYNC TEST (DRY RUN)
================================================================================

CONFIGURATION:
--------------------------------------------------------------------------------
Source Table: employees
Column Mapping: 10 columns
Limit: 10

RUNNING DRY RUN SYNC...
--------------------------------------------------------------------------------

✅ Dry run successful!

Statistics:
  Total rows from source: 10

Sample Data (first 3 rows):

Row 1:
  id                        = 1
  name                      = John Doe
  email                     = john@company.com
  department                = IT
  performance_score         = 85.5
  ...
```

### Step 7: Sync Data

```bash
python scripts/database/sync_employees.py
```

**Expected Output:**
```
================================================================================
MPCIM THESIS - EMPLOYEE DATA SYNC
================================================================================

⚠️  WARNING: This will sync data to thesis database!

Continue? (yes/no): yes

STARTING SYNC...
--------------------------------------------------------------------------------

✅ Sync completed successfully!

Statistics:
  Total rows from source: 1,234
  Created (new):          1,234
  Updated (existing):     0
  Skipped:                0
  Errors:                 0

Duration: 5.23 seconds

VERIFYING SYNC...
--------------------------------------------------------------------------------
✅ Thesis database now has:
   Total employees:        1,234
   Promoted:               156 (12.64%)
   Avg Performance Score:  78.45
   Avg Behavioral Score:   82.31
```

---

## 💻 Usage Examples

### Example 1: Read from Source Database

```python
from app.database.dual_connection import dual_db
from sqlalchemy import text

# Query source database (read-only)
with dual_db.get_source_session() as session:
    result = session.execute(text("""
        SELECT id, name, email, performance_score
        FROM employees
        WHERE department = 'IT'
        LIMIT 10
    """))
    
    for row in result:
        print(f"{row.name}: {row.performance_score}")
```

### Example 2: Sync Specific Data

```python
from app.database.data_sync import data_sync

# Sync only active employees from IT department
result = data_sync.sync_employees(
    source_table='employees',
    where_clause="status = 'active' AND department = 'IT'",
    limit=None  # All matching rows
)

print(f"Synced {result['stats']['created']} employees")
```

### Example 3: Custom Query Sync

```python
from app.database.data_sync import data_sync

# Complex query with joins
custom_query = """
    SELECT 
        e.id,
        e.name,
        e.email,
        d.name as department,
        p.title as position,
        e.performance_score,
        e.behavioral_score
    FROM employees e
    LEFT JOIN departments d ON e.department_id = d.id
    LEFT JOIN positions p ON e.position_id = p.id
    WHERE e.status = 'active'
"""

column_mapping = {
    'id': 'employee_id',
    'name': 'name',
    'email': 'email',
    'department': 'department',
    'position': 'position',
    'performance_score': 'performance_score',
    'behavioral_score': 'behavioral_score',
}

result = data_sync.sync_with_custom_query(
    query=custom_query,
    column_mapping=column_mapping
)
```

### Example 4: Log Prediction to Thesis DB

```python
from app.database import db_manager, PredictionRepository

# After making prediction
with db_manager.get_session() as session:
    prediction = PredictionRepository.create(
        session,
        employee_id='EMP001',
        model_name='XGBoost',
        prediction=1,  # PROMOTED
        probability=0.85,
        confidence_level='High',
        input_features={
            'performance_score': 85.5,
            'behavioral_score': 90.0
        },
        threshold_used=0.70,
        predicted_by='hr_user1'
    )
    
    print(f"Prediction logged: ID {prediction.id}")
```

---

## 🔄 Scheduled Sync

### Option 1: Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add line to sync daily at 2 AM
0 2 * * * cd /path/to/MPCIM_Thesis && /path/to/python scripts/database/sync_employees.py >> /var/log/mpcim_sync.log 2>&1
```

### Option 2: Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "MPCIM Data Sync"
4. Trigger: Daily at 2:00 AM
5. Action: Start a program
   - Program: `python.exe`
   - Arguments: `scripts/database/sync_employees.py`
   - Start in: `C:\path\to\MPCIM_Thesis`

### Option 3: Python Script with Schedule

```python
# scripts/database/scheduled_sync.py
import schedule
import time
from sync_employees import sync_data

def job():
    print("Starting scheduled sync...")
    sync_data()
    print("Sync complete!")

# Run daily at 2 AM
schedule.every().day.at("02:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Run with:
```bash
python scripts/database/scheduled_sync.py
```

---

## 🔍 Troubleshooting

### Issue 1: Cannot Connect to Source Database

**Error:**
```
❌ SOURCE DATABASE NOT CONNECTED!
```

**Solutions:**
1. Check PostgreSQL is running:
   ```bash
   # Mac
   brew services list
   brew services start postgresql@14
   
   # Linux
   sudo systemctl status postgresql
   sudo systemctl start postgresql
   ```

2. Verify port 5433 is correct:
   ```bash
   psql -U postgres -p 5433 -l
   ```

3. Check credentials in `.env`

4. Test connection manually:
   ```bash
   psql -U postgres -p 5433 -d db_digispace_cna_augustus_182025
   ```

### Issue 2: Permission Denied

**Error:**
```
permission denied for table employees
```

**Solutions:**
1. Grant read permissions:
   ```sql
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO postgres;
   ```

2. Or use a read-only user:
   ```sql
   CREATE USER readonly_user WITH PASSWORD 'password';
   GRANT CONNECT ON DATABASE db_digispace_cna_augustus_182025 TO readonly_user;
   GRANT USAGE ON SCHEMA public TO readonly_user;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
   ```

### Issue 3: Column Not Found

**Error:**
```
column "performance_score" does not exist
```

**Solutions:**
1. Run discovery script to see actual columns:
   ```bash
   python scripts/database/setup_dual_database.py
   ```

2. Update column mapping in `data_sync.py`

3. Check for typos in column names

### Issue 4: Thesis Database Not Created

**Error:**
```
database "mpcim_thesis" does not exist
```

**Solutions:**
```bash
# Create database
psql -U postgres -c "CREATE DATABASE mpcim_thesis;"

# Or with specific encoding
psql -U postgres -c "CREATE DATABASE mpcim_thesis WITH ENCODING 'UTF8';"
```

---

## 📊 Monitoring & Maintenance

### Check Sync Status

```python
from app.database import db_manager, EmployeeRepository

with db_manager.get_session() as session:
    stats = EmployeeRepository.get_statistics(session)
    print(f"Total employees: {stats['total_employees']}")
    print(f"Last updated: {stats.get('last_updated')}")
```

### Monitor Prediction Accuracy

```python
from app.database import PredictionRepository

with db_manager.get_session() as session:
    accuracy = PredictionRepository.get_accuracy_stats(session)
    print(f"Model accuracy: {accuracy['accuracy']:.2f}%")
    print(f"Total predictions: {accuracy['total']}")
```

### Database Size

```sql
-- Check database sizes
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
WHERE datname IN ('db_digispace_cna_augustus_182025', 'mpcim_thesis');
```

---

## 🎯 Best Practices

1. **Always Use Dry Run First**
   - Test with `dry_run=True` before actual sync
   - Verify column mappings
   - Check sample data

2. **Incremental Sync**
   - Add `updated_at` filter to sync only new/changed data
   - Reduces sync time
   - Less load on source database

3. **Error Handling**
   - Log all errors
   - Set up alerts for failed syncs
   - Keep error details for debugging

4. **Backup**
   - Backup thesis database before major syncs
   - Keep source database read-only
   - Test restore procedures

5. **Performance**
   - Sync during off-peak hours
   - Use batch operations
   - Add indexes on frequently queried columns

---

## 📚 Next Steps

1. ✅ Setup dual database connection
2. ✅ Discover source schema
3. ✅ Configure column mapping
4. ✅ Test sync (dry run)
5. ✅ Sync data
6. ⏳ Update Streamlit app to use database
7. ⏳ Implement prediction logging
8. ⏳ Setup scheduled sync
9. ⏳ Add monitoring dashboard

---

**Last Updated**: November 22, 2025  
**Author**: Deni Sulaeman  
**Version**: 1.0
