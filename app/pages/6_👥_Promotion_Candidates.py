"""
MPCIM Dashboard - Promotion Candidates & Employee Analysis
Author: Deni Sulaeman
Date: November 24, 2025

HR Decision Support: Identify promotion-worthy employees and analyze their profiles.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import joblib
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Try to import database connection
try:
    from database.connection import DatabaseManager
    from database.repositories import EmployeeRepository
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

# Import AI predictor utilities
try:
    from utils import ai_predictor
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    st.warning("⚠️ AI predictor utilities not available")

# Import Gemini AI helper
try:
    from utils.gemini_ai_helper import get_gemini_helper
    gemini_helper = get_gemini_helper()
    GEMINI_AVAILABLE = gemini_helper.is_available()
except ImportError:
    GEMINI_AVAILABLE = False
    gemini_helper = None

# Page config
st.set_page_config(
    page_title="Promotion Candidates - MPCIM",
    page_icon="👥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .candidate-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .high-potential {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #11998e;
        margin-bottom: 1rem;
    }
    .medium-potential {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f093fb;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">👥 Promotion Candidates Analysis</div>', unsafe_allow_html=True)

# Paths
repo_root = Path(__file__).resolve().parents[2]
models_dir = repo_root / 'models'
results_dir = repo_root / 'results' / 'advanced_models'
data_dir = repo_root / 'data'

# Load model and scaler
@st.cache_resource
def load_model_and_scaler():
    """Load trained model and scaler"""
    try:
        # Try new model with psychological features first
        model_path_new = models_dir / 'random_forest_model_with_psychological.pkl'
        scaler_path_new = models_dir / 'scaler_with_psychological.pkl'
        
        if model_path_new.exists() and scaler_path_new.exists():
            model = joblib.load(model_path_new)
            scaler = joblib.load(scaler_path_new)
            st.success("✅ Using model with psychological assessment features!")
            return model, scaler, True
        
        # Fallback to old model
        model_path_old = repo_root / 'results' / 'advanced_models' / 'random_forest_model.pkl'
        scaler_path_old = data_dir / 'processed' / 'scaler.pkl'
        
        model = joblib.load(model_path_old)
        scaler = joblib.load(scaler_path_old)
        st.warning("⚠️ Using old model without psychological features")
        
        return model, scaler, True
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, False

model, scaler, model_loaded = load_model_and_scaler()

# Load data function - EXACTLY SAME AS DATA EXPLORER
def load_employee_data():
    """Load employee data - EXACT same logic as Data Explorer (NO CACHE for session state)"""
    # Check if data is already loaded in session state (from Data Explorer)
    # Data Explorer uses 'mpcim_df' key
    if 'mpcim_df' in st.session_state and st.session_state.mpcim_df is not None:
        df = st.session_state.mpcim_df.copy()
        st.success(f"📊 Using uploaded data from Data Explorer ({len(df):,} rows)")
        
        # Add name if not present
        if 'name' not in df.columns and 'employee_id_hash' in df.columns:
            df['name'] = df['employee_id_hash'].apply(lambda x: f"Employee {str(x)[:8]}")
        
        return df, 'session'
    
    # Otherwise load from files - SAME PRIORITY AS DATA EXPLORER
    try:
        # Try balanced sample first for quick demo (same as Data Explorer)
        sample_100_balanced_path = data_dir / 'final' / 'sample_dataset_100_balanced.csv'
        if sample_100_balanced_path.exists():
            df = pd.read_csv(sample_100_balanced_path)
            st.info("📊 Using sample_dataset_100_balanced.csv (same as Data Explorer)")
        else:
            # Fallback to original sample
            sample_100_path = data_dir / 'final' / 'sample_dataset_100.csv'
            if sample_100_path.exists():
                df = pd.read_csv(sample_100_path)
                st.info("📊 Using sample_dataset_100.csv")
            else:
                # Try integrated_full_dataset (with QA)
                csv_path_qa = data_dir / 'final' / 'integrated_full_dataset.csv'
                if csv_path_qa.exists():
                    df = pd.read_csv(csv_path_qa)
                    st.info("📊 Using integrated_full_dataset.csv")
                else:
                    # Fallback to integrated_performance_behavioral
                    csv_path = data_dir / 'final' / 'integrated_performance_behavioral.csv'
                    if csv_path.exists():
                        df = pd.read_csv(csv_path)
                        st.info("📊 Using integrated_performance_behavioral.csv")
                    else:
                        st.error("❌ No data file found!")
                        return None, None
        
        # Generate employee names from hash if not present
        if 'name' not in df.columns and 'employee_id_hash' in df.columns:
            df['name'] = df['employee_id_hash'].apply(lambda x: f"Employee {str(x)[:8]}")
        
        # Validate data is not normalized
        if 'performance_score' in df.columns:
            perf_max = df['performance_score'].max()
            perf_min = df['performance_score'].min()
            
            # Check if data appears normalized (not in 0-100 range)
            if perf_max < 95 or (perf_min > 5 and perf_max < 100):
                st.warning("⚠️ **Data appears to be normalized/scaled!**")
                st.warning("Model expects original scale (0-100) for accurate predictions.")
                st.info("💡 **Recommended**: Use `sample_dataset_100_balanced.csv` or `sample_dataset_1000_balanced.csv` (NOT _normalized version)")
                st.info(f"📊 Current data range: {perf_min:.1f} - {perf_max:.1f}")
        
        return df, 'csv'
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.write("Debug info:", str(e))
        return None, None

# Feature engineering function
def engineer_features(df):
    """Apply feature engineering to raw data - MUST match training features"""
    df = df.copy()
    
    # Fill any NaN in base columns first
    df['performance_score'].fillna(df['performance_score'].median(), inplace=True)
    df['behavior_avg'].fillna(df['behavior_avg'].median(), inplace=True)
    df['tenure_years'].fillna(df['tenure_years'].median(), inplace=True)
    
    # Combined score
    df['combined_score'] = (df['performance_score'] + df['behavior_avg']) / 2
    
    # Tenure categories
    df['tenure_category'] = pd.cut(df['tenure_years'], 
                                    bins=[0, 3, 7, 100], 
                                    labels=['Junior', 'Mid', 'Senior'])
    df['tenure_category_encoded'] = df['tenure_category'].map({'Junior': 0, 'Mid': 1, 'Senior': 2})
    df['tenure_category_encoded'].fillna(1, inplace=True)  # Default to Mid
    
    # Performance rating encoding
    if 'performance_rating' in df.columns:
        rating_map = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Very Good': 3, 'Excellent': 4}
        df['performance_rating_encoded'] = df['performance_rating'].map(rating_map)
        df['performance_rating_encoded'].fillna(2, inplace=True)  # Default to 'Good'
    else:
        df['performance_rating_encoded'] = 2  # Default
    
    # Score ratio (perf/beh)
    df['perf_beh_ratio'] = df['performance_score'] / (df['behavior_avg'] + 0.1)
    
    # Score difference
    df['score_difference'] = df['performance_score'] - df['behavior_avg']
    
    # High performer flag (performance > 85)
    df['high_performer'] = (df['performance_score'] > 85).astype(int)
    
    # Binary encodings
    df['gender_encoded'] = (df['gender'] == 'M').astype(int)
    df['is_permanent_encoded'] = (df['is_permanent'] == 't').astype(int) if df['is_permanent'].dtype == 'object' else df['is_permanent'].astype(int)
    
    # Marital status encoding
    marital_map = {'Single': 0, 'Married': 1, 'Divorced': 2, 'Widowed': 3}
    df['marital_status_encoded'] = df['marital_status'].map(marital_map)
    df['marital_status_encoded'].fillna(0, inplace=True)
    
    # Performance level encoding (based on score ranges)
    # Handle NaN values before converting to int
    # Use 300 as upper bound to handle outliers
    df['performance_level_encoded'] = pd.cut(df['performance_score'], 
                                             bins=[0, 60, 75, 85, 300],
                                             labels=[0, 1, 2, 3])
    df['performance_level_encoded'] = df['performance_level_encoded'].fillna(1).astype(int)
    
    # Behavioral level encoding (based on score ranges)
    df['behavioral_level_encoded'] = pd.cut(df['behavior_avg'],
                                            bins=[0, 60, 75, 85, 100],
                                            labels=[0, 1, 2, 3])
    df['behavioral_level_encoded'] = df['behavioral_level_encoded'].fillna(1).astype(int)
    
    # ========================================================================
    # PSYCHOLOGICAL ASSESSMENT FEATURES (NEW!)
    # ========================================================================
    
    # Check if psychological columns exist
    if 'psychological_score' in df.columns:
        # Fill NaN in psychological columns
        df['psychological_score'].fillna(df['psychological_score'].median(), inplace=True)
        df['drive_score'].fillna(df['drive_score'].median(), inplace=True)
        df['mental_strength_score'].fillna(df['mental_strength_score'].median(), inplace=True)
        df['adaptability_score'].fillna(df['adaptability_score'].median(), inplace=True)
        df['collaboration_score'].fillna(df['collaboration_score'].median(), inplace=True)
        df['leadership_potential'].fillna(df['leadership_potential'].median(), inplace=True)
        
        # Psychological level encoding
        df['psychological_level_encoded'] = pd.cut(df['psychological_score'],
                                                   bins=[0, 60, 75, 85, 100],
                                                   labels=[0, 1, 2, 3])
        df['psychological_level_encoded'] = df['psychological_level_encoded'].fillna(1).astype(int)
        
        # Psychological-Performance ratio
        df['psych_perf_ratio'] = df['psychological_score'] / (df['performance_score'] + 0.1)
        
        # Psychological-Behavior ratio
        df['psych_behavior_ratio'] = df['psychological_score'] / (df['behavior_avg'] + 0.1)
        
        # Holistic balance (std of 3 main scores)
        df['holistic_balance'] = df[['performance_score', 'behavior_avg', 'psychological_score']].std(axis=1)
        
        # High psychological flag
        df['high_psychological'] = (df['psychological_score'] > 75).astype(int)
        
        # High drive flag
        df['high_drive'] = (df['drive_score'] > 75).astype(int)
        
        # High adaptability flag
        df['high_adaptability'] = (df['adaptability_score'] > 75).astype(int)
        
        # High leadership potential flag
        df['high_leadership'] = (df['leadership_potential'] > 75).astype(int)
        
    else:
        # If no psychological data, fill with default values
        df['psychological_score'] = 70.0  # Default median
        df['drive_score'] = 70.0
        df['mental_strength_score'] = 70.0
        df['adaptability_score'] = 70.0
        df['collaboration_score'] = 80.0
        df['leadership_potential'] = 70.0
        df['psychological_level_encoded'] = 1
        df['psych_perf_ratio'] = 1.0
        df['psych_behavior_ratio'] = 1.0
        df['holistic_balance'] = 5.0
        df['high_psychological'] = 0
        df['high_drive'] = 0
        df['high_adaptability'] = 0
        df['high_leadership'] = 0
    
    return df

# Predict promotion probability
def predict_promotion(df_features, model, scaler):
    """Predict promotion probability for employees"""
    # Feature columns - Check if psychological features available
    original_features = [
        'tenure_years',
        'performance_score',
        'behavior_avg',
        'perf_beh_ratio',
        'combined_score',
        'score_difference',
        'high_performer',
        'gender_encoded',
        'marital_status_encoded',
        'is_permanent_encoded',
        'tenure_category_encoded',
        'performance_level_encoded',
        'behavioral_level_encoded',
        'performance_rating_encoded'
    ]
    
    psychological_features = [
        'psychological_score',
        'drive_score',
        'mental_strength_score',
        'adaptability_score',
        'collaboration_score',
        'leadership_potential',
        'psychological_level_encoded',
        'psych_perf_ratio',
        'psych_behavior_ratio',
        'holistic_balance',
        'high_psychological',
        'high_drive',
        'high_adaptability',
        'high_leadership'
    ]
    
    # Check if psychological features exist
    has_psychological = all(col in df_features.columns for col in psychological_features)
    
    if has_psychological:
        feature_cols = original_features + psychological_features
    else:
        feature_cols = original_features
    
    # Ensure all features exist with proper defaults
    for col in feature_cols:
        if col not in df_features.columns:
            if col == 'high_performer':
                df_features[col] = 0
            elif col in ['performance_level_encoded', 'behavioral_level_encoded']:
                df_features[col] = 1  # Default to level 1
            elif col == 'performance_rating_encoded':
                df_features[col] = 2  # Default to 'Good'
            else:
                df_features[col] = 0
    
    # Select features in correct order
    X = df_features[feature_cols].copy()
    
    # Fill any NaN values
    X = X.fillna(0)
    
    # Scale features
    try:
        X_scaled = scaler.transform(X)
        
        # Predict
        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)[:, 1]
        
        return predictions, probabilities
    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.write("Features available:", X.columns.tolist())
        st.write("First row:", X.iloc[0].to_dict())
        return np.zeros(len(X)), np.zeros(len(X))

# Sidebar - Info
with st.sidebar:
    st.markdown("### 📊 Data Source")
    
    # Show data source info
    if 'mpcim_df' in st.session_state and st.session_state.mpcim_df is not None:
        st.success(f"✅ Uploaded data ({len(st.session_state.mpcim_df):,} rows)")
    else:
        st.info("💡 Using default sample data")
    
    # Refresh button
    if st.button("🔄 Refresh Data", help="Reload data from Data Explorer"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Filter Options")
    
    min_probability = st.slider(
        "Minimum Promotion Probability",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Filter candidates by minimum predicted probability"
    )
    
    show_all = st.checkbox("Show all employees", value=False)

# Load data
df_raw, source_used = load_employee_data()

if df_raw is None or not model_loaded:
    st.error("⚠️ Unable to load data or model. Please check configuration.")
    st.stop()

# Debug info
with st.expander("🔍 Debug Info", expanded=False):
    st.write(f"**Data Source**: {source_used}")
    st.write(f"**Total Rows**: {len(df_raw):,}")
    st.write(f"**Columns**: {df_raw.columns.tolist()}")
    if 'performance_score' in df_raw.columns:
        st.write(f"**Performance Score Range**: {df_raw['performance_score'].min():.1f} - {df_raw['performance_score'].max():.1f}")
    st.write(f"**Session State Data**: {'Yes' if 'mpcim_df' in st.session_state and st.session_state.mpcim_df is not None else 'No'}")
    if 'mpcim_df' in st.session_state and st.session_state.mpcim_df is not None:
        st.write(f"**Session State Rows**: {len(st.session_state.mpcim_df):,}")

# Engineer features
df = engineer_features(df_raw)

# Predict promotions
predictions, probabilities = predict_promotion(df, model, scaler)

# Add predictions to dataframe
df['predicted_promotion'] = predictions
df['promotion_probability'] = probabilities

# Sort by probability
df = df.sort_values('promotion_probability', ascending=False)

# Statistics
st.markdown("### 📊 Overview Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Employees", f"{len(df):,}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    high_potential = len(df[df['promotion_probability'] >= 0.7])
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("High Potential", f"{high_potential:,}", 
              delta=f"{high_potential/len(df)*100:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    medium_potential = len(df[(df['promotion_probability'] >= 0.5) & (df['promotion_probability'] < 0.7)])
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Medium Potential", f"{medium_potential:,}",
              delta=f"{medium_potential/len(df)*100:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    avg_prob = df['promotion_probability'].mean()
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Avg Probability", f"{avg_prob:.1%}")
    st.markdown('</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top 10 Candidates", "📋 All Candidates", "🔍 Employee Detail", "🤖 AI Insights"])

# ============================================================================
# TAB 1: TOP 10 CANDIDATES
# ============================================================================
with tab1:
    st.markdown("### 🏆 Top 10 Promotion Candidates")
    st.caption("Ranked by promotion probability")
    
    # Debug: Check for duplicates
    if len(df['employee_id_hash'].unique()) < len(df):
        st.warning(f"⚠️ Found duplicate employees in data. Showing unique only.")
        df_unique = df.drop_duplicates(subset=['employee_id_hash'], keep='first')
        top_10 = df_unique.head(10).copy()
    else:
        top_10 = df.head(10).copy()
    
    # Display as compact table with cards
    for rank, (idx, row) in enumerate(top_10.iterrows(), 1):
        prob = row['promotion_probability']
        emp_name = row.get('name', 'N/A')
        emp_id = row.get('employee_id_hash', 'N/A')[:12]
        
        # Medal for top 3
        if rank == 1:
            medal = "🥇"
            bg_color = "#FFD700"
        elif rank == 2:
            medal = "🥈"
            bg_color = "#C0C0C0"
        elif rank == 3:
            medal = "🥉"
            bg_color = "#CD7F32"
        else:
            medal = f"#{rank}"
            bg_color = "#667eea"
        
        # Compact card with all info in one row
        col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 1.5, 1, 1, 0.8, 0.8, 0.8])
        
        with col1:
            st.markdown(f"<div style='background:{bg_color};color:white;padding:8px;border-radius:5px;text-align:center;font-size:18px;font-weight:bold;'>{medal}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**{emp_name}**")
            st.caption(f"🆔 {emp_id}...")
        
        with col3:
            st.metric("Probability", f"{prob:.1%}")
        
        with col4:
            perf = row['performance_score']
            beh = row['behavior_avg']
            psych = row.get('psychological_score', 0)
            st.metric("Perf/Beh/Psych", f"{perf:.0f}/{beh:.0f}/{psych:.0f}")
            # Add psychological indicator
            if psych > 75:
                st.caption("🧠 Strong")
            elif psych > 60:
                st.caption("🧠 Good")
            else:
                st.caption("🧠 Fair")
        
        with col5:
            st.metric("Tenure", f"{row['tenure_years']:.0f}y")
        
        with col6:
            # Leadership indicator
            if 'leadership_potential' in row and row['leadership_potential'] > 75:
                st.markdown("👑")
                st.caption("Leader")
            else:
                st.markdown("")
                st.caption("")
        
        with col7:
            if st.button("👁️", key=f"top_{idx}", help="View Details", use_container_width=True):
                # Store the actual position in dataframe
                st.session_state['selected_employee'] = rank - 1  # rank starts at 1, index at 0
                st.session_state['show_modal'] = True
                st.rerun()
        
        st.divider()
    
    # Show modal if requested
    if st.session_state.get('show_modal', False):
        sel_idx = st.session_state.get('selected_employee', 0)
        if sel_idx < len(df):
            emp = df.iloc[sel_idx]
            
            # Modal using st.dialog (Streamlit 1.31+) or custom HTML
            st.markdown("""
            <style>
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                z-index: 9998;
            }
            .modal-content {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                z-index: 9999;
                max-width: 800px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
            }
            .modal-header {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #1f77b4;
            }
            .modal-close {
                position: absolute;
                top: 15px;
                right: 15px;
                font-size: 24px;
                cursor: pointer;
                color: #999;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Modal content with custom styling
            with st.container():
                st.markdown(f"""
                <div class="modal-header">
                    🔍 Detail: {emp.get('name', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
                
                # Close button at top
                if st.button("❌ Close", key="close_modal_top", use_container_width=False):
                    st.session_state['show_modal'] = False
                    st.rerun()
                
                st.markdown("---")
                
                # Main metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("🆔 Employee ID", emp.get('employee_id_hash', 'N/A')[:12] + '...')
                with col2:
                    st.metric("🎯 Probability", f"{emp['promotion_probability']:.1%}")
                with col3:
                    st.metric("📊 Performance", f"{emp['performance_score']:.1f}")
                with col4:
                    st.metric("🎯 Behavior", f"{emp['behavior_avg']:.1f}")
                
                # Psychological Assessment Section
                st.markdown("---")
                st.markdown("### 🧠 Psychological Assessment")
                
                if 'psychological_score' in emp and emp.get('psychological_score', 0) > 0:
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        psych_score = emp.get('psychological_score', 0)
                        st.metric("Overall", f"{psych_score:.1f}")
                        if psych_score > 75:
                            st.caption("✅ Excellent")
                        elif psych_score > 60:
                            st.caption("✅ Good")
                        else:
                            st.caption("⚠️ Fair")
                    
                    with col2:
                        drive = emp.get('drive_score', 0)
                        st.metric("🔥 Drive", f"{drive:.1f}")
                        if drive > 75:
                            st.caption("High motivation")
                        else:
                            st.caption("Moderate")
                    
                    with col3:
                        mental = emp.get('mental_strength_score', 0)
                        st.metric("💪 Mental", f"{mental:.1f}")
                        if mental > 75:
                            st.caption("Resilient")
                        else:
                            st.caption("Developing")
                    
                    with col4:
                        adapt = emp.get('adaptability_score', 0)
                        st.metric("🔄 Adapt", f"{adapt:.1f}")
                        if adapt > 75:
                            st.caption("Very flexible")
                        else:
                            st.caption("Moderate")
                    
                    with col5:
                        collab = emp.get('collaboration_score', 0)
                        st.metric("🤝 Collab", f"{collab:.1f}")
                        if collab > 75:
                            st.caption("Team player")
                        else:
                            st.caption("Developing")
                    
                    # Leadership potential
                    st.markdown("---")
                    leadership = emp.get('leadership_potential', 0)
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric("👔 Leadership Potential", f"{leadership:.1f}")
                    with col2:
                        if leadership > 80:
                            st.success("🌟 High leadership potential - Ready for leadership roles")
                        elif leadership > 70:
                            st.info("✅ Good leadership potential - Can develop into leadership")
                        else:
                            st.warning("📈 Moderate - Needs leadership development")
                    
                    # Holistic score
                    holistic = emp.get('holistic_score', 0)
                    if holistic > 0:
                        st.markdown("---")
                        st.markdown("### 📊 Holistic Assessment")
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.metric("Combined Score", f"{holistic:.1f}")
                        with col2:
                            alignment = emp.get('score_alignment', 0)
                            if alignment > 0.7:
                                st.success(f"✅ Well-balanced profile (alignment: {alignment:.2f})")
                            elif alignment > 0.5:
                                st.info(f"📊 Moderately balanced (alignment: {alignment:.2f})")
                            else:
                                st.warning(f"⚠️ Unbalanced profile (alignment: {alignment:.2f})")
                else:
                    st.info("ℹ️ No psychological assessment data available for this employee")
                
                st.markdown("---")
                
                # Detailed info in two columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Performance Metrics")
                    st.write(f"**Performance Score**: {emp['performance_score']:.1f}")
                    st.write(f"**Behavior Average**: {emp['behavior_avg']:.1f}")
                    st.write(f"**Combined Score**: {emp['combined_score']:.1f}")
                    st.write(f"**Score Difference**: {emp['score_difference']:.1f}")
                    
                    # Balance indicator
                    if abs(emp['score_difference']) < 5:
                        st.success("✅ **Excellent Balance**")
                    elif abs(emp['score_difference']) < 10:
                        st.warning("⚠️ **Acceptable Balance**")
                    else:
                        st.error("❌ **Needs Balance**")
                    
                    st.write(f"**High Performer**: {'✅ Yes' if emp['high_performer'] else '❌ No'}")
                    st.write(f"**Perf/Beh Ratio**: {emp['perf_beh_ratio']:.2f}")
                
                with col2:
                    st.markdown("### 📅 Employment Info")
                    st.write(f"**Tenure**: {emp['tenure_years']:.1f} years")
                    
                    # Tenure category
                    if emp['tenure_years'] < 3:
                        st.info("👶 Junior (< 3 years)")
                    elif emp['tenure_years'] <= 7:
                        st.success("🎯 Mid-level (3-7 years) - Optimal!")
                    else:
                        st.warning("👴 Senior (> 7 years)")
                    
                    st.write(f"**Gender**: {emp.get('gender', 'N/A')}")
                    st.write(f"**Marital Status**: {emp.get('marital_status', 'N/A')}")
                    st.write(f"**Permanent**: {emp.get('is_permanent', 'N/A')}")
                
                st.markdown("---")
                
                # Psychological Assessment Section
                if 'psychological_score' in emp and emp['psychological_score'] > 0:
                    st.markdown("### 🧠 Psychological Assessment")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("🧠 Overall", f"{emp.get('psychological_score', 0):.1f}")
                        
                        # Psychological level indicator
                        if emp.get('psychological_score', 0) > 75:
                            st.success("✅ Strong")
                        elif emp.get('psychological_score', 0) > 60:
                            st.info("⚠️ Good")
                        else:
                            st.warning("❌ Needs Development")
                    
                    with col2:
                        st.metric("🔥 Drive", f"{emp.get('drive_score', 0):.1f}")
                        st.metric("💪 Mental Strength", f"{emp.get('mental_strength_score', 0):.1f}")
                    
                    with col3:
                        st.metric("🔄 Adaptability", f"{emp.get('adaptability_score', 0):.1f}")
                        st.metric("🤝 Collaboration", f"{emp.get('collaboration_score', 0):.1f}")
                    
                    # Leadership Potential
                    st.markdown("#### 👑 Leadership Potential")
                    leadership = emp.get('leadership_potential', 0)
                    st.progress(leadership / 100)
                    
                    if leadership > 80:
                        st.success(f"✅ **Very High Leadership Potential** ({leadership:.1f}/100)")
                    elif leadership > 70:
                        st.info(f"⚠️ **High Leadership Potential** ({leadership:.1f}/100)")
                    elif leadership > 60:
                        st.warning(f"💡 **Moderate Leadership Potential** ({leadership:.1f}/100)")
                    else:
                        st.error(f"❌ **Low Leadership Potential** ({leadership:.1f}/100)")
                    
                    st.markdown("---")
                
                # Why this probability?
                st.markdown("### 💡 Why This Probability?")
                
                reasons = []
                
                # Tenure factor
                if 3 <= emp['tenure_years'] <= 7:
                    reasons.append("✅ **Optimal tenure** (3-7 years) - Major positive factor!")
                elif emp['tenure_years'] < 3:
                    reasons.append("⚠️ **Short tenure** (< 3 years) - Needs more experience")
                else:
                    reasons.append("⚠️ **Long tenure** (> 7 years) - May prefer current role")
                
                # Balance factor
                if abs(emp['score_difference']) < 5:
                    reasons.append("✅ **Excellent balance** (gap < 5) - Well-rounded profile!")
                elif abs(emp['score_difference']) < 10:
                    reasons.append("⚠️ **Acceptable balance** (gap 5-10) - Minor imbalance")
                else:
                    reasons.append("❌ **Poor balance** (gap > 10) - Too specialized")
                
                # Performance range
                if 75 <= emp['performance_score'] <= 85:
                    reasons.append("✅ **Optimal performance range** (75-85) - Proven promotion zone!")
                elif emp['performance_score'] > 90:
                    reasons.append("⚠️ **Very high performance** (> 90) - Already at peak")
                elif emp['performance_score'] < 60:
                    reasons.append("❌ **Low performance** (< 60) - Needs improvement")
                else:
                    reasons.append("⚠️ **Developing performance** (60-75) - Room for growth")
                
                # High performer
                if emp['high_performer']:
                    reasons.append("✅ **High performer** (> 85) - Strong candidate")
                
                # Psychological factors (if available)
                if 'psychological_score' in emp and emp['psychological_score'] > 0:
                    if emp['psychological_score'] > 75:
                        reasons.append("✅ **Strong psychological profile** (> 75) - Mentally prepared!")
                    elif emp['psychological_score'] > 60:
                        reasons.append("⚠️ **Good psychological profile** (60-75) - Acceptable readiness")
                    else:
                        reasons.append("❌ **Weak psychological profile** (< 60) - Needs mental preparation")
                    
                    if emp.get('drive_score', 0) > 75:
                        reasons.append("✅ **High drive** (> 75) - Very motivated for growth!")
                    
                    if emp.get('adaptability_score', 0) > 75:
                        reasons.append("✅ **High adaptability** (> 75) - Ready for change!")
                    
                    if emp.get('leadership_potential', 0) > 75:
                        reasons.append("✅ **High leadership potential** (> 75) - Future leader!")
                    
                    if emp.get('mental_strength_score', 0) < 60:
                        reasons.append("⚠️ **Low mental strength** (< 60) - May need support under pressure")
                
                for reason in reasons:
                    st.markdown(reason)
                
                st.markdown("---")
                
                # Close button at bottom
                if st.button("❌ Close", key="close_modal_bottom", use_container_width=True):
                    st.session_state['show_modal'] = False
                    st.rerun()

# ============================================================================
# TAB 2: ALL CANDIDATES LIST
# ============================================================================
with tab2:
    st.markdown("### 📋 All Promotion Candidates")
    
    # Filter candidates
    if show_all:
        df_display = df
        st.info(f"📋 Showing all {len(df_display):,} employees")
    else:
        df_display = df[df['promotion_probability'] >= min_probability]
        st.success(f"✅ Found {len(df_display):,} candidates with probability ≥ {min_probability:.0%}")
    
    if len(df_display) == 0:
        st.warning("No candidates found. Try lowering the minimum probability threshold.")
    else:
        # Display candidates
        for idx, row in df_display.head(100).iterrows():
            prob = row['promotion_probability']
            
            # Color coding
            if prob >= 0.7:
                card_class = "high-potential"
                badge = "🌟 High Potential"
                color = "#11998e"
            elif prob >= 0.5:
                card_class = "medium-potential"
                badge = "⭐ Medium Potential"
                color = "#f093fb"
            else:
                card_class = "info-box"
                badge = "💡 Low Potential"
                color = "#95a5a6"
            
            # Card with better styling
            emp_name = row.get('name', 'N/A')
            emp_id = row.get('employee_id_hash', 'N/A')
            
            with st.container():
                # Header row
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"### {emp_name}")
                    st.caption(f"🆔 {emp_id[:20]}...")
                
                with col2:
                    if st.button("👁️ Details", key=f"btn_{idx}", use_container_width=True):
                        # Find position in dataframe
                        st.session_state['selected_employee'] = df.index.get_loc(idx)
                        st.session_state['show_detail_all'] = idx
                        st.rerun()
                
                # Badge and probability
                st.markdown(f"**{badge}** | Probability: **{prob:.1%}**")
                st.progress(prob)
                
                # Metrics in compact row
                col_a, col_b, col_c, col_d = st.columns(4)
                col_a.metric("📅 Tenure", f"{row['tenure_years']:.1f} yrs")
                col_b.metric("📊 Performance", f"{row['performance_score']:.0f}")
                col_c.metric("🎯 Behavior", f"{row['behavior_avg']:.0f}")
                col_d.metric("⭐ Combined", f"{row['combined_score']:.0f}")
                
                # Show detail if this employee is selected
                if st.session_state.get('show_detail_all') == idx:
                    with st.container():
                        st.markdown("#### 📋 Detailed Information")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Performance Breakdown**")
                            st.write(f"• Score Difference: **{row['score_difference']:.1f}**")
                            st.write(f"• Perf/Beh Ratio: **{row['perf_beh_ratio']:.2f}**")
                            st.write(f"• High Performer: **{'Yes' if row['high_performer'] else 'No'}**")
                        
                        with col2:
                            st.markdown("**Personal Info**")
                            st.write(f"• Gender: **{row.get('gender', 'N/A')}**")
                            st.write(f"• Marital: **{row.get('marital_status', 'N/A')}**")
                            st.write(f"• Status: **{row.get('is_permanent', 'N/A')}**")
                        
                        if st.button("❌ Close", key=f"close_{idx}"):
                            st.session_state['show_detail_all'] = None
                            st.rerun()
                
                st.markdown("---")

# ============================================================================
# TAB 3: EMPLOYEE DETAIL ANALYSIS
# ============================================================================
with tab3:
    st.markdown("### 🔍 Employee Detail Analysis")
    
    # Employee selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Check if employee selected from list
        if 'selected_employee' in st.session_state:
            default_idx = st.session_state['selected_employee']
        else:
            default_idx = 0
        
        employee_options = df.apply(
            lambda x: f"{x.get('name', 'N/A')} - {x.get('employee_id_hash', 'N/A')} (Prob: {x['promotion_probability']:.1%})", 
            axis=1
        ).tolist()
        
        selected_employee = st.selectbox(
            "Select Employee:",
            options=range(len(df)),
            format_func=lambda x: employee_options[x],
            index=default_idx if default_idx < len(df) else 0
        )
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Get selected employee data
    emp = df.iloc[selected_employee]
    
    # Employee header
    st.markdown(f"## {emp.get('name', 'Employee')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Basic Information**")
        st.write(f"**ID**: {emp.get('employee_id_hash', 'N/A')}")
        st.write(f"**Tenure**: {emp['tenure_years']:.1f} years ({emp['tenure_category']})")
        st.write(f"**Gender**: {emp.get('gender', 'N/A')}")
        st.write(f"**Status**: {'Permanent' if emp['is_permanent_encoded'] == 1 else 'Contract'}")
    
    with col2:
        st.markdown("**Performance Metrics**")
        st.write(f"**Performance Score**: {emp['performance_score']:.0f}")
        st.write(f"**Behavioral Score**: {emp['behavior_avg']:.0f}")
        st.write(f"**Combined Score**: {emp['combined_score']:.0f}")
        st.write(f"**Rating**: {emp.get('performance_rating', 'N/A')}")
    
    with col3:
        st.markdown("**Promotion Analysis**")
        prob = emp['promotion_probability']
        st.write(f"**Probability**: {prob:.1%}")
        st.write(f"**Prediction**: {'✅ Recommended' if prob >= 0.5 else '❌ Not Recommended'}")
        st.write(f"**Category**: {'🌟 High' if prob >= 0.7 else '⭐ Medium' if prob >= 0.5 else '💡 Low'}")
    
    # Probability gauge
    st.markdown("### 📊 Promotion Probability")
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prob * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Promotion Probability (%)", 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#ffcccc'},
                {'range': [30, 50], 'color': '#ffffcc'},
                {'range': [50, 70], 'color': '#ccffcc'},
                {'range': [70, 100], 'color': '#99ff99'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Spider/Radar Chart - COMPETENCY PROFILE
    st.markdown("### 🕸️ Competency Profile (Spider Chart)")
    
    # Normalize scores to 0-100 scale
    categories = [
        'Performance\nScore',
        'Behavioral\nScore',
        'Tenure\n(normalized)',
        'Combined\nScore',
        'Performance/\nBehavior Ratio'
    ]
    
    # Normalize tenure to 0-100 (assuming max 20 years)
    tenure_normalized = min(emp['tenure_years'] / 20 * 100, 100)
    
    # Normalize ratio (assuming range 0.5-2.0 maps to 0-100)
    ratio_value = emp.get('perf_beh_ratio', emp['performance_score'] / (emp['behavior_avg'] + 0.1))
    ratio_normalized = min(max((ratio_value - 0.5) / 1.5 * 100, 0), 100)
    
    values = [
        emp['performance_score'],
        emp['behavior_avg'],
        tenure_normalized,
        emp['combined_score'],
        ratio_normalized
    ]
    
    # Create spider chart
    fig_spider = go.Figure()
    
    fig_spider.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Employee Profile',
        line=dict(color='#667eea', width=2),
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    # Add benchmark (average of all employees)
    avg_ratio = df.get('perf_beh_ratio', df['performance_score'] / (df['behavior_avg'] + 0.1)).mean()
    avg_values = [
        df['performance_score'].mean(),
        df['behavior_avg'].mean(),
        min(df['tenure_years'].mean() / 20 * 100, 100),
        df['combined_score'].mean(),
        min(max((avg_ratio - 0.5) / 1.5 * 100, 0), 100)
    ]
    
    fig_spider.add_trace(go.Scatterpolar(
        r=avg_values,
        theta=categories,
        fill='toself',
        name='Company Average',
        line=dict(color='#95a5a6', width=2, dash='dash'),
        fillcolor='rgba(149, 165, 166, 0.1)'
    ))
    
    fig_spider.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            )
        ),
        showlegend=True,
        title="Employee vs Company Average",
        height=500
    )
    
    st.plotly_chart(fig_spider, use_container_width=True)
    
    # Strengths and Development Areas
    st.markdown("### 💪 Strengths & Development Areas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌟 Strengths:**")
        strengths = []
        
        if emp['performance_score'] > df['performance_score'].quantile(0.75):
            strengths.append("✅ High performance score")
        if emp['behavior_avg'] > df['behavior_avg'].quantile(0.75):
            strengths.append("✅ Excellent behavioral competencies")
        if emp['tenure_years'] >= 3 and emp['tenure_years'] <= 7:
            strengths.append("✅ Optimal tenure range")
        if emp['combined_score'] > df['combined_score'].quantile(0.75):
            strengths.append("✅ Strong overall profile")
        
        if strengths:
            for s in strengths:
                st.write(s)
        else:
            st.write("💡 Developing competencies")
    
    with col2:
        st.markdown("**📈 Development Areas:**")
        developments = []
        
        if emp['performance_score'] < df['performance_score'].quantile(0.25):
            developments.append("⚠️ Performance score needs improvement")
        if emp['behavior_avg'] < df['behavior_avg'].quantile(0.25):
            developments.append("⚠️ Behavioral competencies need development")
        if emp['tenure_years'] > 10:
            developments.append("💡 Long tenure - consider new challenges")
        if abs(emp['score_difference']) > 20:
            developments.append("⚠️ Large gap between performance and behavior")
        
        if developments:
            for d in developments:
                st.write(d)
        else:
            st.write("✅ Well-balanced profile")
    
    # Recommendations
    st.markdown("### 💡 HR Recommendations")
    
    if prob >= 0.7:
        st.success(f"""
        **🌟 High Potential Candidate**
        
        This employee shows strong potential for promotion with {prob:.1%} probability.
        
        **Recommended Actions:**
        - ✅ Include in promotion shortlist
        - ✅ Assign leadership development program
        - ✅ Provide mentorship opportunities
        - ✅ Consider for high-impact projects
        - ✅ Schedule promotion discussion within 3 months
        """)
    elif prob >= 0.5:
        st.info(f"""
        **⭐ Medium Potential Candidate**
        
        This employee has moderate promotion potential ({prob:.1%}).
        
        **Recommended Actions:**
        - 💡 Identify specific development areas
        - 💡 Provide targeted training
        - 💡 Set clear performance goals
        - 💡 Re-evaluate in 6 months
        - 💡 Consider for stretch assignments
        """)
    else:
        st.warning(f"""
        **💡 Development Focus Needed**
        
        This employee currently has lower promotion probability ({prob:.1%}).
        
        **Recommended Actions:**
        - 📚 Focus on skill development
        - 📚 Provide regular feedback and coaching
        - 📚 Set incremental improvement goals
        - 📚 Monitor progress quarterly
        - 📚 Identify and address performance gaps
        """)
# ============================================================================
# TAB 4: AI INSIGHTS
# ============================================================================
with tab4:
    st.markdown("### 🤖 AI-Powered Insights & Analysis")
    st.caption("Advanced AI features for deeper candidate analysis")
    
    if not AI_AVAILABLE:
        st.error("❌ AI predictor utilities not available. Please check installation.")
    else:
        # Select employee for AI analysis
        st.markdown("#### Select Employee for AI Analysis")
        
        employee_options = [f"{row['name']} ({row['promotion_probability']:.1%})" 
                          for idx, row in df.head(20).iterrows()]
        
        selected_emp_str = st.selectbox(
            "Choose an employee:",
            options=employee_options,
            key="ai_employee_select"
        )
        
        # Get selected employee index
        selected_idx = employee_options.index(selected_emp_str)
        selected_row = df.iloc[selected_idx]
        
        st.markdown("---")
        
        # Create AI analysis sections with clear grouping
        st.markdown("#### 🎯 Pilih Jenis Analisis:")
        st.caption("**Machine Learning Analysis** = Analisis cepat berbasis model | **Gemini AI** = Analisis mendalam dengan bahasa natural")
        
        if GEMINI_AVAILABLE:
            ai_tab1, ai_tab2, ai_tab3 = st.tabs([
                "📊 ML: Confidence & Readiness",
                "🎯 ML: Feature & Similarity Analysis",
                "🤖 Gemini AI: Analisis Mendalam"
            ])
            # Create sub-tabs for ML Analysis tab 2
            ai_tab2_sub1 = ai_tab2_sub2 = ai_tab2_sub3 = None
        else:
            ai_tab1, ai_tab2 = st.tabs([
                "📊 ML: Confidence & Readiness",
                "🎯 ML: Feature & Similarity Analysis"
            ])
            ai_tab3 = None
            ai_tab2_sub1 = ai_tab2_sub2 = ai_tab2_sub3 = None
        
        # Prepare features for AI analysis - use same features as predict_promotion
        original_features = [
            'tenure_years',
            'performance_score',
            'behavior_avg',
            'perf_beh_ratio',
            'combined_score',
            'score_difference',
            'high_performer',
            'gender_encoded',
            'marital_status_encoded',
            'is_permanent_encoded',
            'tenure_category_encoded',
            'performance_level_encoded',
            'behavioral_level_encoded',
            'performance_rating_encoded'
        ]
        
        psychological_features = [
            'psychological_score',
            'drive_score',
            'mental_strength_score',
            'adaptability_score',
            'collaboration_score',
            'leadership_potential',
            'psychological_level_encoded',
            'psych_perf_ratio',
            'psych_behavior_ratio',
            'holistic_balance',
            'high_psychological',
            'high_drive',
            'high_adaptability',
            'high_leadership'
        ]
        
        # Check if psychological features exist
        has_psychological = all(col in df.columns for col in psychological_features)
        
        if has_psychological:
            feature_cols = original_features + psychological_features
        else:
            feature_cols = original_features
        
        # Only use features that exist in df
        feature_cols = [col for col in feature_cols if col in df.columns]
        
        # Validate features match model expectations
        try:
            X = df[feature_cols]
            
            # Check if model has feature_names_in_ attribute
            if hasattr(model, 'feature_names_in_'):
                expected_features = list(model.feature_names_in_)
                
                # Ensure features match exactly
                if set(feature_cols) != set(expected_features):
                    st.warning(f"⚠️ Feature mismatch detected. Using model's expected features.")
                    # Use only features that model expects and are available
                    feature_cols = [f for f in expected_features if f in df.columns]
                    X = df[feature_cols]
                    
                    # Reorder to match model's expected order
                    X = X[expected_features]
        except Exception as e:
            st.error(f"❌ Error preparing features: {str(e)}")
            st.info("💡 Please ensure data has been processed through feature engineering.")
            X = None
        
        # AI Tab 1: Confidence & Readiness
        with ai_tab1:
            st.markdown("### 🎯 Prediction Confidence & Readiness Analysis")
            
            if X is None:
                st.error("Cannot perform AI analysis - feature preparation failed.")
            else:
                try:
                    # Get confidence scores
                    _, probabilities, confidence = ai_predictor.predict_with_confidence(
                        model, scaler, X
                    )
                except Exception as e:
                    st.error(f"❌ Prediction error: {str(e)}")
                    st.info("💡 This may be due to feature mismatch. Please check model compatibility.")
                    probabilities = None
                    confidence = None
                
                if probabilities is not None and confidence is not None:
                    emp_prob = probabilities[selected_idx]
                    emp_confidence = confidence[selected_idx]
                    
                    # Display confidence
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Promotion Probability", f"{emp_prob:.1%}")
                    
                    with col2:
                        conf_level, conf_color = ai_predictor.get_confidence_level(emp_confidence)
                        st.metric("AI Confidence", f"{emp_confidence:.1%}", 
                                 delta=conf_level, delta_color="normal")
                    
                    with col3:
                        readiness = ai_predictor.calculate_readiness_scores(selected_row)
                        st.metric("Overall Readiness", f"{readiness['overall']:.1%}")
                    
                    st.markdown("---")
                    
                    # Readiness breakdown
                    st.markdown("#### 📊 Readiness Breakdown")
                    
                    readiness_data = {
                        'Dimension': ['Performance', 'Behavior', 'Psychological', 'Leadership'],
                        'Score': [
                            readiness['performance'],
                            readiness['behavior'],
                            readiness['psychological'],
                            readiness['leadership']
                        ]
                    }
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=readiness_data['Dimension'],
                            y=readiness_data['Score'],
                            marker_color=['#3498db', '#2ecc71', '#9b59b6', '#f39c12'],
                            text=[f"{s:.1%}" for s in readiness_data['Score']],
                            textposition='auto'
                        )
                    ])
                    
                    fig.update_layout(
                        title="Readiness Scores by Dimension",
                        yaxis_title="Readiness Score",
                        yaxis=dict(range=[0, 1], tickformat='.0%'),
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Readiness level
                    st.info(f"**Readiness Level**: {readiness['level']}")
                    
                    # Natural language explanation
                    st.markdown("#### 💬 AI Explanation")
                    feature_contrib = ai_predictor.get_feature_contributions(model, X, selected_idx)
                    explanation = ai_predictor.generate_natural_language_explanation(
                        selected_row, emp_prob, feature_contrib
                    )
                    st.markdown(explanation)
        
        # AI Tab 2: ML Feature & Similarity Analysis (with sub-tabs)
        with ai_tab2:
            st.markdown("### 🎯 Machine Learning Analysis")
            st.caption("Analisis berbasis model ML untuk understanding faktor-faktor kunci")
            
            # Create sub-tabs for different ML analyses
            ml_sub1, ml_sub2, ml_sub3 = st.tabs([
                "📊 Feature Contribution",
                "👥 Similar Candidates",
                "🔮 What-If Scenarios"
            ])
            
            # ML Sub-tab 1: Feature Contribution
            with ml_sub1:
                st.markdown("#### 📊 Analisis Kontribusi Faktor")
            
            if X is None:
                st.error("Cannot perform feature analysis - feature preparation failed.")
            else:
                try:
                    # Get feature contributions
                    feature_contrib = ai_predictor.get_feature_contributions(model, X, selected_idx)
                except Exception as e:
                    st.error(f"❌ Error analyzing features: {str(e)}")
                    feature_contrib = None
                
                if feature_contrib is not None:
                    # Display top 10 features
                    st.markdown("#### Top 10 Contributing Features")
                    
                    top_10_features = feature_contrib.head(10)
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            y=[ai_predictor.format_feature_name(f) for f in top_10_features['feature']],
                            x=top_10_features['contribution'],
                            orientation='h',
                            marker_color='#3498db',
                            text=[f"{c:.1%}" for c in top_10_features['contribution']],
                            textposition='auto'
                        )
                    ])
                    
                    fig.update_layout(
                        title="Feature Contributions to Prediction",
                        xaxis_title="Contribution",
                        yaxis_title="Feature",
                        height=500,
                        xaxis=dict(tickformat='.0%')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Feature details table
                    st.markdown("#### 📋 Feature Details")
                    
                    display_df = top_10_features.copy()
                    display_df['feature'] = display_df['feature'].apply(ai_predictor.format_feature_name)
                    display_df['contribution'] = display_df['contribution'].apply(lambda x: f"{x:.2%}")
                    display_df['value'] = display_df['value'].apply(lambda x: f"{x:.2f}")
                    
                    st.dataframe(
                        display_df[['feature', 'value', 'contribution']],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # AI Recommendations
                    st.markdown("#### 💡 AI-Powered Recommendations")
                    
                    # Get emp_prob from selected_row if not available
                    if 'promotion_probability' in selected_row:
                        emp_prob_for_rec = selected_row['promotion_probability']
                    else:
                        emp_prob_for_rec = 0.5
                    
                    recommendations = ai_predictor.generate_ai_recommendations(
                        feature_contrib, emp_prob_for_rec
                    )
                    
                    for rec in recommendations[:5]:
                        with st.expander(f"{rec['icon']} {rec['feature']} - {rec['impact']} Impact"):
                            st.markdown(f"**Recommendation**: {rec['text']}")
                            st.markdown(f"**Action**: {rec['action']}")
                            st.progress(rec['priority'])
                            st.caption(f"Priority Score: {rec['priority']:.2f}")
        
        # AI Tab 3: Similar Candidates
        with ai_tab3:
            st.markdown("### 👥 Similar Candidate Analysis")
            st.caption("Find candidates with similar profiles using AI similarity matching")
            
            if X is None:
                st.error("Cannot perform similarity analysis - feature preparation failed.")
            else:
                try:
                    # Find similar candidates
                    similar_df = ai_predictor.find_similar_candidates(
                        scaler, X, selected_idx, df, top_n=5
                    )
                except Exception as e:
                    st.error(f"❌ Error finding similar candidates: {str(e)}")
                    similar_df = None
                
                if similar_df is not None and len(similar_df) > 0:
                    st.markdown(f"#### Top 5 Candidates Similar to **{selected_row['name']}**")
                    
                    for idx, (_, sim_row) in enumerate(similar_df.iterrows(), 1):
                        similarity = sim_row['similarity_score']
                        
                        with st.expander(f"#{idx} {sim_row['name']} - {similarity:.1%} similarity"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Promotion Prob", f"{sim_row['promotion_probability']:.1%}")
                                st.metric("Performance", f"{sim_row['performance_score']:.1f}")
                            
                            with col2:
                                st.metric("Behavior", f"{sim_row['behavior_avg']:.1f}")
                                if 'psychological_score' in sim_row:
                                    st.metric("Psychological", f"{sim_row['psychological_score']:.1f}")
                            
                            with col3:
                                st.metric("Tenure", f"{sim_row['tenure_years']:.1f}y")
                                if 'leadership_potential' in sim_row:
                                    st.metric("Leadership", f"{sim_row['leadership_potential']:.1f}")
                            
                            # Similarity visualization
                            st.progress(similarity)
                            st.caption(f"Similarity Score: {similarity:.2%}")
                    
                    # Comparison chart
                    st.markdown("#### 📊 Profile Comparison")
                    
                    comparison_features = ['performance_score', 'behavior_avg', 
                                         'psychological_score', 'leadership_potential']
                    
                    comparison_data = {
                        'Feature': [],
                        'Selected': [],
                        'Similar Avg': []
                    }
                    
                    for feat in comparison_features:
                        if feat in selected_row and feat in similar_df.columns:
                            comparison_data['Feature'].append(feat.replace('_', ' ').title())
                            comparison_data['Selected'].append(selected_row[feat])
                            comparison_data['Similar Avg'].append(similar_df[feat].mean())
                    
                    if comparison_data['Feature']:
                        fig = go.Figure(data=[
                            go.Bar(name='Selected Employee', 
                                  x=comparison_data['Feature'], 
                                  y=comparison_data['Selected'],
                                  marker_color='#3498db'),
                            go.Bar(name='Similar Candidates (Avg)', 
                                  x=comparison_data['Feature'], 
                                  y=comparison_data['Similar Avg'],
                                  marker_color='#95a5a6')
                        ])
                        
                        fig.update_layout(
                            title="Profile Comparison: Selected vs Similar Candidates",
                            yaxis_title="Score",
                            barmode='group',
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
        
        # What-If Scenarios (removed - ai_tab4 not defined)
        # This section has been removed to fix the NameError
        if False:  # Disabled section
            st.markdown("### 🔮 What-If Scenario Analysis")
            st.caption("Explore how changes in specific factors affect promotion probability")
            
            st.info("💡 **How it works**: Select a feature and adjust its value to see the predicted impact on promotion probability.")
            
            # Select feature for what-if
            what_if_features = [
                'performance_score', 'behavior_avg', 'psychological_score',
                'drive_score', 'leadership_potential', 'adaptability_score',
                'mental_strength_score', 'collaboration_score'
            ]
            
            if X is None:
                st.error("Cannot perform what-if analysis - feature preparation failed.")
            else:
                available_features = [f for f in what_if_features if f in X.columns]
                
                if available_features:
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        selected_feature = st.selectbox(
                            "Select feature to modify:",
                            options=available_features,
                            format_func=ai_predictor.format_feature_name
                        )
                    
                    with col2:
                        current_value = selected_row[selected_feature]
                        st.metric("Current Value", f"{current_value:.1f}")
                
                    # Value slider
                    new_value = st.slider(
                        "Adjust value:",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(current_value),
                        step=1.0
                    )
                    
                    # Calculate what-if
                    try:
                        X_single = X.iloc[[selected_idx]]
                        original_prob, new_prob, change = ai_predictor.predict_what_if_scenario(
                            model, scaler, X_single, selected_feature, new_value
                        )
                    except Exception as e:
                        st.error(f"❌ Error calculating what-if scenario: {str(e)}")
                        original_prob = new_prob = change = None
                
                    # Display results
                    if original_prob is not None:
                        st.markdown("#### 📊 Prediction Impact")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Original Probability", f"{original_prob:.1%}")
                        
                        with col2:
                            st.metric("New Probability", f"{new_prob:.1%}", 
                                     delta=f"{change:+.1%}")
                        
                        with col3:
                            impact = "High" if abs(change) > 0.1 else "Medium" if abs(change) > 0.05 else "Low"
                            st.metric("Impact Level", impact)
                
                        # Visualization
                        fig = go.Figure()
                        
                        fig.add_trace(go.Bar(
                            x=['Original', 'Modified'],
                            y=[original_prob, new_prob],
                            marker_color=['#3498db', '#2ecc71' if change > 0 else '#e74c3c'],
                            text=[f"{original_prob:.1%}", f"{new_prob:.1%}"],
                            textposition='auto'
                        ))
                        
                        fig.update_layout(
                            title=f"Impact of Changing {ai_predictor.format_feature_name(selected_feature)}",
                            yaxis_title="Promotion Probability",
                            yaxis=dict(range=[0, 1], tickformat='.0%'),
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                
                        # Interpretation
                        if change > 0.05:
                            st.success(f"✅ Increasing {ai_predictor.format_feature_name(selected_feature)} from {current_value:.1f} to {new_value:.1f} would **significantly increase** promotion probability by {change:.1%}.")
                        elif change > 0:
                            st.info(f"⚠️ Increasing {ai_predictor.format_feature_name(selected_feature)} from {current_value:.1f} to {new_value:.1f} would **moderately increase** promotion probability by {change:.1%}.")
                        elif change < -0.05:
                            st.error(f"❌ Decreasing {ai_predictor.format_feature_name(selected_feature)} from {current_value:.1f} to {new_value:.1f} would **significantly decrease** promotion probability by {change:.1%}.")
                        elif change < 0:
                            st.warning(f"⚠️ Decreasing {ai_predictor.format_feature_name(selected_feature)} from {current_value:.1f} to {new_value:.1f} would **moderately decrease** promotion probability by {change:.1%}.")
                        else:
                            st.info("No significant change in promotion probability.")
                else:
                    st.warning("No features available for what-if analysis.")
        
        # AI Tab 3: Gemini AI Analysis
        if ai_tab3 is not None:
            with ai_tab3:
                st.markdown("### 🤖 Gemini AI-Powered Analysis")
                st.caption("Advanced natural language analysis powered by Google Gemini AI")
                
                if not GEMINI_AVAILABLE:
                    st.error("❌ Gemini AI not available. Please configure GEMINI_API_KEY in .env file.")
                    st.info("💡 Get your free API key from: https://makersuite.google.com/app/apikey")
                else:
                    # Create sub-tabs for different Gemini AI features
                    gemini_tab1, gemini_tab2, gemini_tab3 = st.tabs([
                        "📝 Analisis Komprehensif",
                        "💡 Rencana Pengembangan",
                        "🔍 Penjelasan Prediksi"
                    ])
                    
                    # Gemini Tab 1: Comprehensive Analysis
                    with gemini_tab1:
                        st.markdown("#### 📝 Analisis Komprehensif Berbasis AI")
                        st.caption("✨ Powered by Google Gemini 2.5 Flash | Bahasa Indonesia")
                        
                        if st.button("🤖 Generate Analisis Lengkap", key="gen_analysis", type="primary"):
                            with st.spinner("🤖 Gemini AI sedang menganalisis profil karyawan..."):
                                # Get ML confidence if available
                                ml_conf = None
                                if 'probabilities' in locals() and probabilities is not None:
                                    ml_conf = confidence[selected_idx] if confidence is not None else None
                                
                                analysis = gemini_helper.generate_employee_analysis(
                                    selected_row.to_dict(),
                                    ml_confidence=ml_conf
                                )
                                
                                st.markdown("---")
                                st.markdown(analysis)
                                st.markdown("---")
                                st.caption("✨ Dihasilkan oleh Google Gemini AI | Berdasarkan data Machine Learning")
                        else:
                            st.info("👆 Klik tombol di atas untuk menghasilkan analisis AI komprehensif dalam Bahasa Indonesia")
                    
                    # Gemini Tab 2: Development Plan
                    with gemini_tab2:
                        st.markdown("#### 💡 Rencana Pengembangan Personal")
                        st.caption("✨ Rekomendasi personal berbasis AI & data ML | Bahasa Indonesia")
                        
                        if st.button("🤖 Generate Rencana Pengembangan", key="gen_dev_plan", type="primary"):
                            with st.spinner("🤖 Gemini AI sedang membuat rencana pengembangan personal..."):
                                # Get feature contributions
                                if X is not None:
                                    try:
                                        feature_contrib = ai_predictor.get_feature_contributions(model, X, selected_idx)
                                        feature_list = [
                                            {
                                                'feature': row['feature'],
                                                'contribution': row['contribution']
                                            }
                                            for _, row in feature_contrib.head(5).iterrows()
                                        ]
                                    except:
                                        feature_list = []
                                else:
                                    feature_list = []
                                
                                # Get ML confidence
                                ml_conf = None
                                if 'probabilities' in locals() and probabilities is not None:
                                    ml_conf = confidence[selected_idx] if confidence is not None else None
                                
                                recommendations = gemini_helper.generate_personalized_recommendations(
                                    selected_row.to_dict(),
                                    feature_list,
                                    ml_confidence=ml_conf
                                )
                                
                                st.markdown("---")
                                st.markdown(recommendations)
                                st.markdown("---")
                                st.caption("✨ Dihasilkan oleh Gemini AI | Berdasarkan faktor ML dengan kontribusi tertinggi")
                        else:
                            st.info("👆 Klik tombol di atas untuk menghasilkan rencana pengembangan yang spesifik dan terukur")
                    
                    # Gemini Tab 3: Prediction Explanation
                    with gemini_tab3:
                        st.markdown("#### 🔍 Penjelasan Prediksi ML")
                        st.caption("✨ Penjelasan natural language tentang hasil prediksi | Bahasa Indonesia")
                        
                        if st.button("🤖 Jelaskan Prediksi", key="gen_explanation", type="primary"):
                            with st.spinner("🤖 Gemini AI sedang menjelaskan hasil prediksi..."):
                                # Get feature contributions
                                if X is not None:
                                    try:
                                        feature_contrib = ai_predictor.get_feature_contributions(model, X, selected_idx)
                                        feature_list = [
                                            {
                                                'feature': row['feature'],
                                                'contribution': row['contribution']
                                            }
                                            for _, row in feature_contrib.head(5).iterrows()
                                        ]
                                    except:
                                        feature_list = []
                                else:
                                    feature_list = []
                                
                                explanation = gemini_helper.explain_prediction(
                                    selected_row.to_dict(),
                                    feature_list
                                )
                                
                                st.markdown("---")
                                st.markdown(explanation)
                                st.markdown("---")
                                st.caption("✨ Dihasilkan oleh Gemini AI | Penjelasan berbasis data ML")
                        else:
                            st.info("👆 Klik tombol di atas untuk mendapatkan penjelasan lengkap tentang prediksi ML")


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p><strong>MPCIM Thesis Project</strong> - HR Decision Support System</p>
    <p>Deni Sulaeman | Master Program in Information Systems</p>
</div>
""", unsafe_allow_html=True)
