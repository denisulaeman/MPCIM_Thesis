"""
Generate Synthetic HR Data for MPCIM Thesis Demo
================================================
This script generates realistic synthetic employee data with:
- Proper correlations between features
- Realistic promotion rate (~12-15%)
- No duplicates or data leakage
- Same structure as full_dataset_processed.csv
"""

import pandas as pd
import numpy as np
import hashlib
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

# ============================================================
# CONFIGURATION
# ============================================================
N_EMPLOYEES = 1500  # Number of unique employees
PROMOTION_BASE_RATE = 0.12  # ~12% base promotion rate

# Indonesian names for realistic data
FIRST_NAMES = [
    'Adi', 'Agus', 'Ahmad', 'Andi', 'Anita', 'Bambang', 'Budi', 'Citra', 'Deni',
    'Dewi', 'Eko', 'Endang', 'Fajar', 'Fitri', 'Hadi', 'Hendra', 'Indra', 'Irwan',
    'Joko', 'Kartini', 'Lina', 'Maya', 'Mega', 'Nina', 'Novi', 'Putri', 'Rahmat',
    'Ratna', 'Rini', 'Rita', 'Rizki', 'Sari', 'Siti', 'Sri', 'Suci', 'Taufik',
    'Tri', 'Umi', 'Vina', 'Wati', 'Widya', 'Yanti', 'Yudi', 'Yuni', 'Zainal'
]

LAST_NAMES = [
    'Harahap', 'Hutabarat', 'Manurung', 'Nasution', 'Nugraha', 'Permana', 
    'Prasetyo', 'Pratama', 'Purnama', 'Putra', 'Rahayu', 'Saputra', 'Sari',
    'Setiawan', 'Simanjuntak', 'Sinaga', 'Sitompul', 'Situmorang', 'Susanto',
    'Sutanto', 'Tampubolon', 'Utama', 'Wibowo', 'Wijaya', 'Yuliana'
]

COMPANIES = list(range(60, 110))  # Company IDs 60-109

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_hash(name, idx):
    """Generate consistent employee ID hash"""
    return hashlib.md5(f"{name}_{idx}".encode()).hexdigest()

def clip_score(score, min_val=0, max_val=100):
    """Clip score to valid range"""
    return np.clip(score, min_val, max_val)

def get_performance_rating(score):
    """Convert performance score to rating"""
    if score >= 90:
        return 'Excellent'
    elif score >= 75:
        return 'Good'
    elif score >= 60:
        return 'Average'
    else:
        return 'Below Average'

def get_tenure_category(years):
    """Convert tenure years to category"""
    if years <= 2:
        return 'junior'
    elif years <= 5:
        return 'mid'
    elif years <= 10:
        return 'senior'
    else:
        return 'veteran'

def get_performance_level(score):
    """Convert performance score to level"""
    if score >= 85:
        return 'high'
    elif score >= 70:
        return 'medium'
    else:
        return 'low'

def get_behavioral_level(score):
    """Convert behavioral score to level"""
    if score >= 90:
        return 'high'
    elif score >= 75:
        return 'medium'
    else:
        return 'low'

# ============================================================
# MAIN DATA GENERATION
# ============================================================

print("=" * 60)
print("🔧 GENERATING SYNTHETIC HR DATA FOR MPCIM THESIS")
print("=" * 60)

# Generate base employee data
employees = []

for i in range(N_EMPLOYEES):
    # Name
    first_name = np.random.choice(FIRST_NAMES)
    last_name = np.random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    
    # Employee ID hash
    employee_id_hash = generate_hash(name, i)
    
    # Company
    company_id = np.random.choice(COMPANIES)
    
    # Demographics
    tenure_years = np.random.choice(range(0, 16), p=[
        0.08, 0.10, 0.12, 0.12, 0.10,  # 0-4 years
        0.10, 0.08, 0.07, 0.06, 0.05,  # 5-9 years
        0.04, 0.03, 0.02, 0.01, 0.01, 0.01  # 10-15 years
    ])
    
    gender = np.random.choice(['M', 'F', 'O'], p=[0.55, 0.40, 0.05])
    marital_status = np.random.choice(['single', 'married', 'widow'], p=[0.35, 0.60, 0.05])
    is_permanent = np.random.choice(['t', 'f'], p=[0.85, 0.15])
    
    # ========================================================
    # GENERATE CORRELATED SCORES (Key for realistic results!)
    # ========================================================
    
    # Base talent/potential (latent variable)
    base_talent = np.random.normal(70, 15)
    
    # Performance score (correlated with talent + some noise)
    performance_score = clip_score(
        base_talent + np.random.normal(5, 10) + 
        (tenure_years * 0.5)  # Experience helps slightly
    )
    
    # Behavioral/Competency scores (correlated with talent)
    drive_score = clip_score(base_talent + np.random.normal(0, 12))
    mental_strength_score = clip_score(base_talent + np.random.normal(0, 12))
    adaptability_score = clip_score(base_talent + np.random.normal(0, 12))
    collaboration_score = clip_score(base_talent + np.random.normal(5, 10))
    
    # Behavioral average
    behavior_avg = np.mean([drive_score, mental_strength_score, 
                           adaptability_score, collaboration_score])
    
    # Psychological score
    psychological_score = clip_score(
        base_talent + np.random.normal(0, 10)
    )
    
    # ========================================================
    # DETERMINE PROMOTION (Based on realistic factors)
    # ========================================================
    
    # Promotion probability factors (start negative to get lower base rate)
    promo_score = -2.5  # Base: very low promotion rate
    
    # Performance is the main factor
    promo_score += (performance_score - 70) * 0.04
    
    # Behavioral score matters
    promo_score += (behavior_avg - 75) * 0.025
    
    # Tenure effect (optimal at 3-7 years)
    if 3 <= tenure_years <= 7:
        promo_score += 0.3
    elif tenure_years > 10:
        promo_score -= 0.2  # Very senior, less likely to be promoted again
    elif tenure_years < 2:
        promo_score -= 0.3  # Too junior
    
    # Permanent employees more likely
    if is_permanent == 't':
        promo_score += 0.15
    else:
        promo_score -= 0.3
    
    # High performer bonus
    if performance_score >= 90:
        promo_score += 0.8
    elif performance_score >= 85:
        promo_score += 0.4
    elif performance_score < 60:
        promo_score -= 0.5
    
    # Calculate final probability
    promo_probability = 1 / (1 + np.exp(-promo_score))  # Sigmoid
    promo_probability = np.clip(promo_probability, 0.01, 0.45)  # Cap at 1-45%
    
    # Determine promotion
    has_promotion = 1 if np.random.random() < promo_probability else 0
    
    # ========================================================
    # DERIVED FEATURES
    # ========================================================
    
    performance_rating = get_performance_rating(performance_score)
    has_quick_assessment = np.random.choice([0, 1], p=[0.1, 0.9])
    
    holistic_score = (performance_score * 0.4 + behavior_avg * 0.3 + 
                     psychological_score * 0.3)
    
    score_alignment = 1 - abs(performance_score - behavior_avg) / 100
    leadership_potential = (performance_score * 0.3 + behavior_avg * 0.4 + 
                           psychological_score * 0.3)
    
    perf_beh_ratio = performance_score / max(behavior_avg, 1)
    combined_score = (performance_score + behavior_avg) / 2
    score_difference = performance_score - behavior_avg
    
    tenure_category = get_tenure_category(tenure_years)
    performance_level = get_performance_level(performance_score)
    behavioral_level = get_behavioral_level(behavior_avg)
    high_performer = 1 if performance_score >= 85 else 0
    
    # Encoded features
    gender_map = {'M': 1, 'F': 0, 'O': 0}
    marital_map = {'single': 1, 'married': 0, 'widow': 2}
    is_perm_map = {'t': 1, 'f': 0}
    rating_map = {'Excellent': 1, 'Good': 2, 'Average': 0, 'Below Average': 3}
    tenure_cat_map = {'junior': 0, 'mid': 1, 'senior': 2, 'veteran': 3}
    perf_level_map = {'low': 1, 'medium': 2, 'high': 0}
    beh_level_map = {'low': 1, 'medium': 2, 'high': 0}
    
    employee = {
        'employee_id_hash': employee_id_hash,
        'name': name,
        'company_id': company_id,
        'tenure_years': tenure_years,
        'gender': gender,
        'marital_status': marital_status,
        'is_permanent': is_permanent,
        'performance_score': round(performance_score, 2),
        'performance_rating': performance_rating,
        'has_promotion': has_promotion,
        'behavior_avg': round(behavior_avg, 4),
        'psychological_score': round(psychological_score, 3),
        'drive_score': round(drive_score, 1),
        'mental_strength_score': round(mental_strength_score, 1),
        'adaptability_score': round(adaptability_score, 1),
        'collaboration_score': round(collaboration_score, 1),
        'has_quick_assessment': has_quick_assessment,
        'holistic_score': round(holistic_score, 4),
        'score_alignment': round(score_alignment, 4),
        'leadership_potential': round(leadership_potential, 4),
        'perf_beh_ratio': round(perf_beh_ratio, 4),
        'combined_score': round(combined_score, 4),
        'score_difference': round(score_difference, 4),
        'tenure_category': tenure_category,
        'performance_level': performance_level,
        'behavioral_level': behavioral_level,
        'high_performer': high_performer,
        'gender_encoded': gender_map.get(gender, 0),
        'marital_status_encoded': marital_map.get(marital_status, 0),
        'is_permanent_encoded': is_perm_map.get(is_permanent, 0),
        'performance_rating_encoded': rating_map.get(performance_rating, 0),
        'tenure_category_encoded': tenure_cat_map.get(tenure_category, 0),
        'performance_level_encoded': perf_level_map.get(performance_level, 0),
        'behavioral_level_encoded': beh_level_map.get(behavioral_level, 0)
    }
    
    employees.append(employee)

# Create DataFrame
df = pd.DataFrame(employees)

# ============================================================
# VALIDATION
# ============================================================

print(f"\n📊 DATASET STATISTICS:")
print(f"   - Total employees: {len(df):,}")
print(f"   - Unique employees: {df['employee_id_hash'].nunique():,}")
print(f"   - Duplicate rows: {df.duplicated().sum()}")
print(f"   - Columns: {len(df.columns)}")

print(f"\n📈 TARGET DISTRIBUTION:")
promo_counts = df['has_promotion'].value_counts()
print(f"   - Not Promoted: {promo_counts[0]:,} ({promo_counts[0]/len(df)*100:.1f}%)")
print(f"   - Promoted: {promo_counts[1]:,} ({promo_counts[1]/len(df)*100:.1f}%)")
print(f"   - Imbalance Ratio: {promo_counts[0]/promo_counts[1]:.1f}:1")

print(f"\n📋 FEATURE RANGES:")
numeric_cols = ['performance_score', 'behavior_avg', 'psychological_score', 
                'tenure_years', 'holistic_score']
for col in numeric_cols:
    print(f"   - {col}: [{df[col].min():.1f}, {df[col].max():.1f}] (mean: {df[col].mean():.1f})")

print(f"\n🔗 CORRELATION WITH TARGET:")
numeric_features = df.select_dtypes(include=[np.number]).columns
correlations = df[numeric_features].corr()['has_promotion'].drop('has_promotion').sort_values(ascending=False)
print("   Top 5 positive:")
for feat, corr in correlations.head(5).items():
    print(f"     {feat}: {corr:+.4f}")

# ============================================================
# SAVE DATA
# ============================================================

output_path = '/Users/denisulaeman/Workspace/Academic/CascadeProjects/MPCIM_Thesis/data/processed/synthetic_hr_data.csv'
df.to_csv(output_path, index=False)
print(f"\n✅ Data saved to: {output_path}")

# Also save a copy for raw data folder
raw_output_path = '/Users/denisulaeman/Workspace/Academic/CascadeProjects/MPCIM_Thesis/data/raw/synthetic_hr_data.csv'
df.to_csv(raw_output_path, index=False)
print(f"✅ Copy saved to: {raw_output_path}")

print("\n" + "=" * 60)
print("✅ SYNTHETIC DATA GENERATION COMPLETE!")
print("=" * 60)

# Show sample
print("\n📋 SAMPLE DATA (First 5 rows):")
print(df.head().to_string())
