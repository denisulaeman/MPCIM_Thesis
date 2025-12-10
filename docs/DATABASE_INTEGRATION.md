

# 🗄️ Database Integration Guide

## 📋 Overview

Integrasi database untuk MPCIM Thesis Application menggunakan **PostgreSQL** (production) atau **SQLite** (development).

**Arsitektur:**
- **ORM**: SQLAlchemy
- **Migration**: Alembic (optional)
- **Pattern**: Repository Pattern
- **Connection Pooling**: QueuePool

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install sqlalchemy psycopg2-binary python-dotenv alembic
```

### 2. Setup Environment Variables

Edit `.env` file:

```bash
# PostgreSQL (Production)
DATABASE_URL=postgresql://username:password@localhost:5432/mpcim_thesis

# Or SQLite (Development)
DATABASE_URL=sqlite:///./mpcim_thesis.db

# Connection Pool Settings
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_POOL_TIMEOUT=30
DATABASE_POOL_RECYCLE=3600
DATABASE_ECHO=false
```

### 3. Initialize Database

```python
from app.database import init_database

# Create all tables
init_database()
```

---

## 📊 Database Schema

### Tables

1. **employees** - Employee master data
2. **predictions** - Prediction logs
3. **users** - HR users
4. **audit_logs** - Activity tracking
5. **model_performance** - Model monitoring
6. **ai_analysis_cache** - AI response caching
7. **feedback** - User feedback

### ER Diagram

```
employees (1) ──< (N) predictions
employees (1) ──< (N) feedback
predictions (1) ──< (N) feedback
users (1) ──< (N) audit_logs
users (1) ──< (N) feedback
```

---

## 💻 Usage Examples

### Example 1: Create Employee

```python
from app.database import db_manager, EmployeeRepository

with db_manager.get_session() as session:
    employee = EmployeeRepository.create(
        session,
        employee_id='EMP001',
        name='John Doe',
        email='john@company.com',
        department='IT',
        performance_score=85.5,
        behavioral_score=90.0,
        has_quick_assessment=True,
        psychological_score=23.5
    )
    print(f"Created: {employee}")
```

### Example 2: Log Prediction

```python
from app.database import db_manager, PredictionRepository

with db_manager.get_session() as session:
    prediction = PredictionRepository.create(
        session,
        employee_id='EMP001',
        model_name='XGBoost',
        model_version='1.0',
        prediction=1,  # PROMOTED
        probability=0.85,
        confidence_level='High',
        input_features={
            'performance_score': 85.5,
            'behavioral_score': 90.0,
            'tenure_years': 5.0
        },
        threshold_used=0.70,
        distance_from_threshold=0.15,
        predicted_by='hr_user1'
    )
    print(f"Logged prediction: {prediction.id}")
```

### Example 3: Query Employees

```python
from app.database import db_manager, EmployeeRepository

with db_manager.get_session() as session:
    # Get all employees
    all_employees = EmployeeRepository.get_all(session)
    
    # Get by department
    it_employees = EmployeeRepository.get_by_department(session, 'IT')
    
    # Search
    results = EmployeeRepository.search(session, 'John')
    
    # Get statistics
    stats = EmployeeRepository.get_statistics(session)
    print(f"Total employees: {stats['total_employees']}")
    print(f"Promotion rate: {stats['promotion_rate']:.2f}%")
```

### Example 4: Update Actual Outcome

```python
from app.database import db_manager, PredictionRepository

with db_manager.get_session() as session:
    # After 6 months, update actual outcome
    prediction = PredictionRepository.update_actual_outcome(
        session,
        prediction_id=1,
        actual_outcome=1  # Actually promoted
    )
    
    # Check accuracy
    stats = PredictionRepository.get_accuracy_stats(session)
    print(f"Model accuracy: {stats['accuracy']:.2f}%")
```

### Example 5: AI Analysis Caching

```python
from app.database import db_manager, AIAnalysisCacheRepository

with db_manager.get_session() as session:
    # Check cache first
    input_data = {'model_name': 'XGBoost', 'metrics': {...}}
    
    cached = AIAnalysisCacheRepository.get_or_none(
        session,
        analysis_type='model_performance',
        input_data=input_data
    )
    
    if cached:
        print("Using cached analysis")
        analysis = cached.analysis_result
    else:
        # Call Gemini AI
        analysis = call_gemini_ai(input_data)
        
        # Cache the result
        AIAnalysisCacheRepository.set(
            session,
            analysis_type='model_performance',
            input_data=input_data,
            analysis_result=analysis,
            ai_provider='gemini',
            ai_model='gemini-2.0-flash-exp',
            expires_in_hours=24,
            tokens_used=1500,
            cost_usd=0.0015
        )
```

### Example 6: Audit Logging

```python
from app.database import db_manager, AuditLogRepository

with db_manager.get_session() as session:
    # Log user action
    AuditLogRepository.log(
        session,
        user_id=1,
        username='hr_user1',
        action='predict',
        entity_type='employee',
        entity_id='EMP001',
        description='Made promotion prediction',
        metadata={'model': 'XGBoost', 'probability': 0.85},
        ip_address='192.168.1.100',
        user_agent='Mozilla/5.0...'
    )
```

---

## 🔧 Integration with Streamlit

### Option 1: Direct Usage

```python
# app/pages/Employees.py
import streamlit as st
from database import db_manager, EmployeeRepository

st.title("Employee Management")

with db_manager.get_session() as session:
    employees = EmployeeRepository.get_all(session)
    
    for emp in employees:
        st.write(f"{emp.name} - {emp.department}")
```

### Option 2: With Caching

```python
import streamlit as st
from database import db_manager, EmployeeRepository

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_employees():
    with db_manager.get_session() as session:
        employees = EmployeeRepository.get_all(session)
        return [emp.to_dict() for emp in employees]

st.title("Employee Management")
employees = get_employees()
st.dataframe(employees)
```

### Option 3: With Session State

```python
import streamlit as st
from database import db_manager, PredictionRepository

if 'prediction_logged' not in st.session_state:
    st.session_state.prediction_logged = False

if st.button("Make Prediction"):
    # Make prediction
    prediction_result = model.predict(...)
    
    # Log to database
    with db_manager.get_session() as session:
        PredictionRepository.create(
            session,
            employee_id=employee_id,
            model_name='XGBoost',
            prediction=prediction_result,
            probability=probability,
            predicted_by=st.session_state.username
        )
    
    st.session_state.prediction_logged = True
    st.success("Prediction logged to database!")
```

---

## 🌐 Free Hosting Options

### 1. Supabase (Recommended) ⭐⭐⭐

**Features:**
- PostgreSQL database
- Built-in authentication
- Real-time subscriptions
- Storage for files
- Free tier: 500MB database, 2GB bandwidth

**Setup:**
```bash
# 1. Create project at https://supabase.com
# 2. Get connection string
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

# 3. Run schema
psql $DATABASE_URL < app/database/schema.sql
```

### 2. Neon ⭐⭐⭐

**Features:**
- Serverless PostgreSQL
- Auto-scaling
- Branching (like Git)
- Free tier: 3GB storage

**Setup:**
```bash
# 1. Create project at https://neon.tech
# 2. Get connection string
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb

# 3. Initialize
python -c "from app.database import init_database; init_database()"
```

### 3. Railway ⭐⭐

**Features:**
- PostgreSQL + app deployment
- GitHub integration
- Free tier: $5 credit/month

**Setup:**
```bash
# 1. Create project at https://railway.app
# 2. Add PostgreSQL plugin
# 3. Get DATABASE_URL from environment
# 4. Deploy app
```

### 4. ElephantSQL ⭐

**Features:**
- Managed PostgreSQL
- Free tier: 20MB storage
- Good for testing

**Setup:**
```bash
# 1. Create instance at https://www.elephantsql.com
# 2. Get connection string
DATABASE_URL=postgresql://user:pass@lucky.db.elephantsql.com/user
```

---

## 🔄 Migration with Alembic

### Setup Alembic

```bash
# Install
pip install alembic

# Initialize
alembic init alembic

# Edit alembic.ini
sqlalchemy.url = postgresql://user:pass@localhost/mpcim_thesis
```

### Create Migration

```bash
# Auto-generate migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 📈 Performance Optimization

### 1. Connection Pooling

Already configured in `connection.py`:
```python
pool_size=10          # Number of persistent connections
max_overflow=20       # Additional connections when needed
pool_timeout=30       # Wait time for available connection
pool_recycle=3600     # Recycle connections after 1 hour
pool_pre_ping=True    # Verify connection before use
```

### 2. Indexing

Indexes already created for:
- Primary keys
- Foreign keys
- Frequently queried columns
- Composite indexes for common queries

### 3. Query Optimization

```python
# Bad: N+1 query problem
employees = session.query(Employee).all()
for emp in employees:
    predictions = emp.predictions  # Separate query for each!

# Good: Eager loading
from sqlalchemy.orm import joinedload

employees = session.query(Employee).options(
    joinedload(Employee.predictions)
).all()
```

### 4. Batch Operations

```python
# Bad: Individual inserts
for data in employee_data:
    session.add(Employee(**data))
    session.commit()  # Commit each time!

# Good: Bulk insert
employees = [Employee(**data) for data in employee_data]
session.bulk_save_objects(employees)
session.commit()  # Single commit
```

---

## 🔒 Security Best Practices

### 1. Never Commit Credentials

```bash
# .gitignore
.env
*.db
__pycache__/
```

### 2. Use Environment Variables

```python
import os
DATABASE_URL = os.getenv('DATABASE_URL')  # ✅ Good
DATABASE_URL = 'postgresql://...'          # ❌ Bad
```

### 3. Password Hashing

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Store hashed password
password_hash = generate_password_hash('user_password')
user = User(username='john', password_hash=password_hash)

# Verify password
is_valid = check_password_hash(user.password_hash, 'user_password')
```

### 4. SQL Injection Prevention

SQLAlchemy ORM automatically prevents SQL injection:
```python
# Safe (parameterized)
session.query(Employee).filter(Employee.name == user_input).all()

# Unsafe (raw SQL)
session.execute(f"SELECT * FROM employees WHERE name = '{user_input}'")  # ❌
```

---

## 🧪 Testing

### Unit Tests

```python
import pytest
from app.database import db_manager, EmployeeRepository

@pytest.fixture
def db_session():
    """Create test database session"""
    # Use in-memory SQLite for testing
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()

def test_create_employee(db_session):
    """Test employee creation"""
    employee = EmployeeRepository.create(
        db_session,
        employee_id='TEST001',
        name='Test User',
        email='test@example.com'
    )
    
    assert employee.employee_id == 'TEST001'
    assert employee.name == 'Test User'
```

---

## 📚 Additional Resources

- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Supabase Docs**: https://supabase.com/docs

---

## 🎯 Next Steps

1. ✅ Choose hosting provider (Supabase recommended)
2. ✅ Setup DATABASE_URL in `.env`
3. ✅ Run `init_database()` to create tables
4. ✅ Integrate with Streamlit pages
5. ✅ Add authentication (optional)
6. ✅ Setup monitoring and backups

---

**Last Updated**: November 22, 2025  
**Author**: Deni Sulaeman  
**Version**: 1.0
