"""
Knowledge Graph Explorer Page with Gemini AI
=============================================
Interactive exploration of MPCIM Knowledge Graph
Enhanced with Google Gemini AI for intelligent insights
"""

import streamlit as st
import sys
from pathlib import Path
import os

# Add parent directory to path
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

from app.services.job_matching_service import get_job_matching_service
from app.visualizations.knowledge_graph_viz import create_interactive_graph, create_job_focused_graph
import streamlit.components.v1 as components

# Gemini AI integration
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    st.warning("⚠️ Google Generative AI not installed. Install with: pip install google-generativeai")

# Page config
st.set_page_config(
    page_title="Knowledge Graph - MPCIM",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #718096;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🗺️ Knowledge Graph - Decision Support</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Supporting HR decisions with skill-based insights and career path analysis</div>', unsafe_allow_html=True)

# Gemini AI Helper Functions
def init_gemini():
    """Initialize Gemini AI with API key"""
    if not GEMINI_AVAILABLE:
        return None
    
    # Try to get API key from environment or session state
    api_key = os.getenv('GEMINI_API_KEY') or st.session_state.get('gemini_api_key')
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-2.5-flash')  # Updated to latest model
        except Exception as e:
            st.error(f"Failed to initialize Gemini: {str(e)}")
            return None
    return None

def query_gemini_about_kg(question, employee_data, kg_stats):
    """Query Gemini AI about Knowledge Graph data"""
    model = init_gemini()
    
    if not model:
        return None
    
    # Calculate actual statistics from data
    avg_performance = employee_data['performance_score'].mean() if 'performance_score' in employee_data.columns else 0
    avg_behavioral = employee_data['behavior_avg'].mean() if 'behavior_avg' in employee_data.columns else 0
    avg_readiness = employee_data['promotion_readiness_enhanced'].mean() if 'promotion_readiness_enhanced' in employee_data.columns else 0
    
    # Prepare context with strict instructions
    context = f"""
    Anda adalah asisten analisis HR yang ahli dalam menganalisis data karyawan untuk promosi dan perencanaan suksesi.
    
    PENTING - ATURAN KETAT:
    1. HANYA gunakan data yang diberikan di bawah ini
    2. JANGAN membuat asumsi atau data fiktif
    3. Jika data tidak cukup, katakan "Data tidak tersedia"
    4. Gunakan BAHASA INDONESIA untuk semua jawaban
    5. Berikan jawaban yang SINGKAT dan PADAT (maksimal 200 kata)
    6. Fokus pada FAKTA dari data, bukan spekulasi
    
    DATA AKTUAL:
    - Total Karyawan: {kg_stats.get('employees', 0)}
    - Rata-rata Performance: {avg_performance:.1f}/100
    - Rata-rata Behavioral: {avg_behavioral:.1f}/100
    - Rata-rata Promotion Readiness: {avg_readiness:.1%}
    - Total Skills: {kg_stats.get('skills', 0)}
    - Job Levels: {kg_stats.get('jobs', 0)}
    
    SAMPLE DATA (5 karyawan pertama):
    {employee_data.head(5)[['employee_id_hash', 'performance_score', 'behavior_avg', 'promotion_readiness_enhanced']].to_string() if all(col in employee_data.columns for col in ['employee_id_hash', 'performance_score', 'behavior_avg', 'promotion_readiness_enhanced']) else 'Data tidak lengkap'}
    
    PERTANYAAN: {question}
    
    FORMAT JAWABAN:
    1. Jawaban langsung (1-2 kalimat)
    2. Data pendukung (angka spesifik dari data)
    3. Rekomendasi aksi (jika relevan, maksimal 3 poin)
    
    CONTOH JAWABAN YANG BAIK:
    "Berdasarkan data, terdapat 5 karyawan dengan promotion readiness > 80%. 
    
    Data:
    - Employee A123: 88.7% readiness
    - Employee B456: 85.4% readiness
    
    Rekomendasi:
    1. Prioritaskan Employee A123 untuk promosi
    2. Siapkan development plan untuk Employee B456
    3. Review dalam 3 bulan"
    
    JANGAN LAKUKAN:
    ❌ Membuat data fiktif
    ❌ Menyebutkan nama karyawan yang tidak ada di data
    ❌ Memberikan persentase yang tidak dihitung dari data
    ❌ Jawaban panjang dan bertele-tele
    ❌ Menggunakan bahasa Inggris
    
    Jawab sekarang dengan mengikuti aturan di atas:
    """
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_employee_with_gemini(employee_data, employee_id):
    """Get AI-powered analysis for specific employee"""
    model = init_gemini()
    
    if not model:
        return None
    
    prompt = f"""
    Anda adalah HR analyst yang menganalisis kesiapan promosi karyawan.
    
    ATURAN KETAT:
    1. Gunakan BAHASA INDONESIA
    2. Hanya analisis DATA yang diberikan
    3. Jawaban SINGKAT dan PADAT (maksimal 250 kata)
    4. Berikan penilaian OBJEKTIF berdasarkan angka
    
    DATA KARYAWAN:
    ID: {employee_id}
    
    Skor Kinerja:
    - Performance: {employee_data.get('performance_score', 0):.1f}/100
    - Behavioral: {employee_data.get('behavior_avg', 0):.1f}/100
    - Psychological: {employee_data.get('psychological_score', 0):.1f}/100
    - Masa Kerja: {employee_data.get('tenure_years', 0):.0f} tahun
    
    Analisis Skills:
    - Total Skills: {employee_data.get('skill_count', 0)}
    - Proficiency Rata-rata: {employee_data.get('skill_avg_proficiency', 0):.2f}/5.0
    - High-Value Skills: {employee_data.get('high_value_skill_count', 0)}
    - Skill Gap: {employee_data.get('skill_gap_ratio', 0):.1%}
    - Skills Terpenuhi: {employee_data.get('skills_met', 0)}
    
    Kesiapan Karir:
    - Readiness Level Berikutnya: {employee_data.get('next_level_skill_readiness', 0):.1%}
    - Potensi Karir: {employee_data.get('career_progression_potential', 0):.1%}
    - Overall Readiness: {employee_data.get('promotion_readiness_enhanced', 0):.1%}
    
    FORMAT JAWABAN:
    
    **Status:** [Siap/Perlu Pengembangan/Belum Siap]
    
    **Kekuatan:**
    1. [Berdasarkan skor tertinggi]
    2. [Berdasarkan data]
    3. [Berdasarkan data]
    
    **Area Pengembangan:**
    1. [Berdasarkan skor terendah]
    2. [Berdasarkan gap analysis]
    3. [Berdasarkan data]
    
    **Rekomendasi:**
    - [Aksi spesifik 1]
    - [Aksi spesifik 2]
    - Timeline: [X bulan berdasarkan gap]
    
    Analisis sekarang:
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def generate_career_path_with_gemini(employee_data, target_level):
    """Generate personalized career path using Gemini"""
    model = init_gemini()
    
    if not model:
        return None
    
    prompt = f"""
    Anda adalah HR development specialist yang membuat rencana pengembangan karir.
    
    ATURAN KETAT:
    1. Gunakan BAHASA INDONESIA
    2. Berdasarkan DATA karyawan yang diberikan
    3. Rencana REALISTIS (12 bulan)
    4. Format TERSTRUKTUR dan JELAS
    5. Maksimal 300 kata
    
    DATA KARYAWAN SAAT INI:
    - Performance: {employee_data.get('performance_score', 0):.1f}/100
    - Total Skills: {employee_data.get('skill_count', 0)}
    - Proficiency: {employee_data.get('skill_avg_proficiency', 0):.2f}/5.0
    - Skill Gap: {employee_data.get('skill_gap_ratio', 0):.1%}
    - Career Readiness: {employee_data.get('career_progression_potential', 0):.1%}
    
    TARGET POSISI: {target_level}
    
    FORMAT RENCANA PENGEMBANGAN (12 Bulan):
    
    **Fase 1 (Bulan 1-3): Fondasi**
    - Skill yang dikembangkan: [Berdasarkan gap terbesar]
    - Program training: [Spesifik dan realistis]
    - Target: [Terukur]
    
    **Fase 2 (Bulan 4-6): Penguatan**
    - Skill yang dikembangkan: [Lanjutan]
    - Program training: [Spesifik]
    - Target: [Terukur]
    
    **Fase 3 (Bulan 7-9): Praktik**
    - Penugasan: [Berdasarkan target posisi]
    - Mentoring: [Ya/Tidak, dengan siapa]
    - Target: [Terukur]
    
    **Fase 4 (Bulan 10-12): Evaluasi**
    - Assessment: [Apa yang diukur]
    - Kriteria sukses: [Spesifik]
    - Keputusan: [Promosi/Lanjut development]
    
    **Investasi:**
    - Waktu: [X jam/minggu]
    - Biaya estimasi: [Rp X juta]
    
    **Probabilitas Sukses:** [X%] berdasarkan gap saat ini
    
    Buat rencana sekarang:
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Load service
@st.cache_resource
def load_service():
    return get_job_matching_service()

service = load_service()

if not service.graph:
    st.error("⚠️ Knowledge Graph not loaded. Please run build_graph.py first.")
    st.stop()

# Get statistics
stats = service.get_statistics()

# Statistics cards
st.markdown("### 📊 Graph Statistics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stats.get('total_nodes', 0):,}</div>
        <div class="stat-label">Total Nodes</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <div class="stat-number">{stats.get('employees', 0):,}</div>
        <div class="stat-label">Employees</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="stat-number">{stats.get('jobs', 0)}</div>
        <div class="stat-label">Job Levels</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <div class="stat-number">{stats.get('skills', 0)}</div>
        <div class="stat-label">Skills</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
        <div class="stat-number">{stats.get('qualified_matches', 0):,}</div>
        <div class="stat-label">Qualified Matches</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Gemini AI Setup in Sidebar
with st.sidebar:
    st.markdown("### 🤖 Gemini AI Assistant")
    
    if GEMINI_AVAILABLE:
        # API Key input
        if 'gemini_api_key' not in st.session_state:
            st.session_state.gemini_api_key = ''
        
        api_key_input = st.text_input(
            "Gemini API Key",
            value=st.session_state.gemini_api_key,
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey"
        )
        
        if api_key_input:
            st.session_state.gemini_api_key = api_key_input
            st.success("✅ API Key configured")
        else:
            st.info("💡 Enter your Gemini API key to enable AI features")
        
        st.markdown("---")
        st.caption("🤖 AI Features:")
        st.caption("• Natural language queries")
        st.caption("• Employee analysis")
        st.caption("• Career path planning")
        st.caption("• Skill gap insights")
    else:
        st.warning("⚠️ Install google-generativeai")
        st.code("pip install google-generativeai", language="bash")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Decision Support", 
    "🤖 AI Assistant", 
    "💼 Job-Focused View", 
    "🌐 Full Graph", 
    "📖 Guide"
])

# ============================================================================
# TAB 1: DECISION SUPPORT
# ============================================================================
with tab1:
    st.markdown("### 🎯 HR Decision Support System")
    st.caption("Skill-based insights to support promotion and succession planning decisions")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h4 style="margin: 0; color: white;">💡 How Knowledge Graph Supports HR Decisions</h4>
        <p style="margin: 10px 0 0 0; opacity: 0.95;">
        Knowledge Graph menyediakan <strong>skill-based analysis</strong> untuk membantu HR mempertimbangkan:
        </p>
        <ul style="margin: 10px 0 0 20px; opacity: 0.95;">
            <li><strong>Skill Gap Analysis</strong> - Apakah kandidat memiliki skills yang dibutuhkan?</li>
            <li><strong>Career Readiness</strong> - Seberapa siap untuk promosi ke level berikutnya?</li>
            <li><strong>Development Needs</strong> - Skills apa yang perlu dikembangkan?</li>
            <li><strong>Alternative Candidates</strong> - Siapa kandidat alternatif dengan skill serupa?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Employee lookup
    st.markdown("#### 🔍 Analyze Employee for Promotion Decision")
    
    # Load employee data
    import pandas as pd
    data_path = repo_root / "data" / "final" / "integrated_full_dataset.csv"
    
    if data_path.exists():
        df = pd.read_csv(data_path)
        
        # Employee selector
        employee_options = df['employee_id_hash'].unique()
        selected_employee = st.selectbox(
            "Select Employee ID",
            options=employee_options,
            key="emp_decision_support"
        )
        
        if selected_employee:
            # Get employee data
            emp_data = df[df['employee_id_hash'] == selected_employee].iloc[0]
            
            # Display employee overview
            st.markdown("##### 📋 Employee Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Performance Score", f"{emp_data.get('performance_score', 0):.1f}")
            with col2:
                st.metric("Behavioral Score", f"{emp_data.get('behavior_avg', 0):.1f}")
            with col3:
                st.metric("Psychological Score", f"{emp_data.get('psychological_score', 0):.1f}")
            with col4:
                st.metric("Tenure", f"{emp_data.get('tenure_years', 0):.0f} years")
            
            st.markdown("---")
            
            # Skill Analysis
            st.markdown("##### 🎯 Skill-Based Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Current Skills Status**")
                
                # Skill metrics
                skill_count = emp_data.get('skill_count', 0)
                skill_avg = emp_data.get('skill_avg_proficiency', 0)
                high_value_skills = emp_data.get('high_value_skill_count', 0)
                
                st.info(f"""
                **Total Skills**: {skill_count}  
                **Average Proficiency**: {skill_avg:.2f}/5.0  
                **High-Value Skills**: {high_value_skills}
                """)
                
                # Skill gap
                skill_gap = emp_data.get('skill_gap_ratio', 0)
                skills_met = emp_data.get('skills_met', 0)
                skills_exceeded = emp_data.get('skills_exceeded', 0)
                
                if skill_gap < 0.2:
                    gap_status = "🟢 Excellent - Minimal gap"
                    gap_color = "success"
                elif skill_gap < 0.4:
                    gap_status = "🟡 Good - Some development needed"
                    gap_color = "warning"
                else:
                    gap_status = "🔴 Needs Development"
                    gap_color = "error"
                
                if gap_color == "success":
                    st.success(f"""
                    **Skill Gap Analysis**  
                    {gap_status}  
                    Gap Ratio: {skill_gap:.2%}  
                    Skills Met: {skills_met}  
                    Skills Exceeded: {skills_exceeded}
                    """)
                elif gap_color == "warning":
                    st.warning(f"""
                    **Skill Gap Analysis**  
                    {gap_status}  
                    Gap Ratio: {skill_gap:.2%}  
                    Skills Met: {skills_met}  
                    Skills Exceeded: {skills_exceeded}
                    """)
                else:
                    st.error(f"""
                    **Skill Gap Analysis**  
                    {gap_status}  
                    Gap Ratio: {skill_gap:.2%}  
                    Skills Met: {skills_met}  
                    Skills Exceeded: {skills_exceeded}
                    """)
            
            with col2:
                st.markdown("**Career Readiness**")
                
                # Career readiness metrics
                next_level_readiness = emp_data.get('next_level_skill_readiness', 0)
                career_potential = emp_data.get('career_progression_potential', 0)
                promotion_readiness = emp_data.get('promotion_readiness_enhanced', 0)
                
                # Readiness status
                if next_level_readiness >= 0.8:
                    readiness_status = "🟢 Ready for Promotion"
                    readiness_color = "success"
                elif next_level_readiness >= 0.6:
                    readiness_status = "🟡 Nearly Ready"
                    readiness_color = "warning"
                else:
                    readiness_status = "🔴 Not Ready Yet"
                    readiness_color = "error"
                
                if readiness_color == "success":
                    st.success(f"""
                    **Next Level Readiness**  
                    {readiness_status}  
                    Skill Readiness: {next_level_readiness:.1%}  
                    Career Potential: {career_potential:.1%}  
                    Overall Readiness: {promotion_readiness:.1%}
                    """)
                elif readiness_color == "warning":
                    st.warning(f"""
                    **Next Level Readiness**  
                    {readiness_status}  
                    Skill Readiness: {next_level_readiness:.1%}  
                    Career Potential: {career_potential:.1%}  
                    Overall Readiness: {promotion_readiness:.1%}
                    """)
                else:
                    st.error(f"""
                    **Next Level Readiness**  
                    {readiness_status}  
                    Skill Readiness: {next_level_readiness:.1%}  
                    Career Potential: {career_potential:.1%}  
                    Overall Readiness: {promotion_readiness:.1%}
                    """)
                
                # Development recommendations
                st.info("""
                **💡 Development Focus**  
                Based on skill gap analysis:
                - Focus on technical skills
                - Develop leadership capabilities
                - Gain cross-functional experience
                """)
            
            st.markdown("---")
            
            # HR Decision Support
            st.markdown("##### 🎯 HR Decision Recommendation")
            
            # Calculate overall recommendation
            perf_score = emp_data.get('performance_score', 0)
            behav_score = emp_data.get('behavior_avg', 0)
            skill_readiness = next_level_readiness
            
            # Decision logic
            if perf_score >= 80 and behav_score >= 80 and skill_readiness >= 0.8:
                decision = "✅ **STRONGLY RECOMMEND** for promotion"
                decision_color = "success"
                reasoning = """
                **Reasoning:**
                - Excellent performance and behavioral scores
                - High skill readiness for next level
                - Minimal skill gap
                - Strong career progression potential
                
                **Action:** Proceed with promotion process
                """
            elif perf_score >= 70 and behav_score >= 70 and skill_readiness >= 0.6:
                decision = "⚠️ **CONSIDER** with development plan"
                decision_color = "warning"
                reasoning = """
                **Reasoning:**
                - Good performance and behavioral scores
                - Moderate skill readiness
                - Some skill gaps to address
                
                **Action:** 
                1. Create 3-6 month development plan
                2. Focus on skill gap areas
                3. Re-evaluate after development period
                """
            else:
                decision = "❌ **NOT RECOMMENDED** at this time"
                decision_color = "error"
                reasoning = """
                **Reasoning:**
                - Performance or behavioral scores below threshold
                - Significant skill gaps
                - Not ready for next level responsibilities
                
                **Action:**
                1. Focus on current role performance
                2. Develop required skills
                3. Consider for future opportunities
                """
            
            if decision_color == "success":
                st.success(decision)
                st.markdown(reasoning)
            elif decision_color == "warning":
                st.warning(decision)
                st.markdown(reasoning)
            else:
                st.error(decision)
                st.markdown(reasoning)
            
            # Alternative candidates
            st.markdown("---")
            st.markdown("##### 👥 Alternative Candidates (Similar Profile)")
            
            # Find similar employees based on available columns
            # Try different job level column names
            job_level_col = None
            for col in ['job_level_encoded', 'job_level', 'level_group', 'group_job_level']:
                if col in df.columns:
                    job_level_col = col
                    break
            
            if job_level_col:
                current_level = emp_data.get(job_level_col, 0)
                similar_employees = df[
                    (df[job_level_col] == current_level) & 
                    (df['employee_id_hash'] != selected_employee)
                ].head(5)
                
                if len(similar_employees) > 0:
                    # Build dataframe with available columns
                    alt_data = {
                        'Employee ID': similar_employees['employee_id_hash'],
                        'Performance': similar_employees['performance_score'].round(1),
                        'Behavioral': similar_employees['behavior_avg'].round(1)
                    }
                    
                    # Add optional columns if available
                    if 'next_level_skill_readiness' in similar_employees.columns:
                        alt_data['Skill Readiness'] = (similar_employees['next_level_skill_readiness'] * 100).round(1).astype(str) + '%'
                    
                    if 'promotion_readiness_enhanced' in similar_employees.columns:
                        alt_data['Promotion Readiness'] = (similar_employees['promotion_readiness_enhanced'] * 100).round(1).astype(str) + '%'
                    
                    alt_df = pd.DataFrame(alt_data)
                    
                    st.dataframe(alt_df, use_container_width=True, hide_index=True)
                    st.caption("💡 Consider these alternatives if primary candidate is not selected")
                else:
                    st.info("No alternative candidates found at same level")
            else:
                st.warning("⚠️ Job level information not available in dataset")
    
    else:
        st.warning("⚠️ Employee data not found. Please ensure integrated_full_dataset.csv exists.")

# ============================================================================
# TAB 2: AI ASSISTANT
# ============================================================================
with tab2:
    # Modern header with gradient
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px; text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="color: white; margin: 0; font-size: 2em;">🤖 AI Assistant</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1em;">
            Powered by Google Gemini - Ask anything about your workforce
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if Gemini is configured
    if not GEMINI_AVAILABLE:
        st.error("⚠️ Google Generative AI not installed. Please install: `pip install google-generativeai`")
    elif not (os.getenv('GEMINI_API_KEY') or st.session_state.get('gemini_api_key')):
        st.warning("⚠️ Gemini API key not configured")
        with st.expander("📝 How to configure"):
            st.info("""
            **Option 1: Environment Variable (Recommended)**
            - API key is already in `.env` file
            - Dashboard will auto-load it
            
            **Option 2: Manual Entry**
            1. Get API key from https://makersuite.google.com/app/apikey
            2. Enter in sidebar
            """)
    else:
        # Load employee data for context
        import pandas as pd
        data_path = repo_root / "data" / "final" / "integrated_full_dataset.csv"
        
        if data_path.exists():
            df = pd.read_csv(data_path)
            
            # Quick Insights First (Most Used)
            st.markdown("#### ⚡ Quick Insights")
            st.caption("One-click analysis for common questions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🏆 Top Performers", use_container_width=True, type="primary"):
                    with st.spinner("🤖 Gemini analyzing..."):
                        response = query_gemini_about_kg(
                            "List the top 5 employees with highest promotion readiness scores. Be concise and actionable.",
                            df, stats
                        )
                        if response:
                            st.success("**Analysis Complete:**")
                            st.markdown(response)
            
            with col2:
                if st.button("⚠️ Skill Gaps", use_container_width=True, type="primary"):
                    with st.spinner("🤖 Gemini analyzing..."):
                        response = query_gemini_about_kg(
                            "What are the 3 most critical skill gaps? Be specific and concise.",
                            df, stats
                        )
                        if response:
                            st.success("**Analysis Complete:**")
                            st.markdown(response)
            
            with col3:
                if st.button("🎯 Succession Risks", use_container_width=True, type="primary"):
                    with st.spinner("🤖 Gemini analyzing..."):
                        response = query_gemini_about_kg(
                            "Identify top 3 succession planning risks. Be concise.",
                            df, stats
                        )
                        if response:
                            st.success("**Analysis Complete:**")
                            st.markdown(response)
            
            st.markdown("---")
            
            # Custom Query Section
            st.markdown("#### 💬 Custom Query")
            st.caption("Ask anything about your workforce data")
            
            # Example questions in a cleaner format
            with st.expander("💡 Example Questions", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **Promotion & Performance:**
                    - Who are ready for promotion?
                    - Analyze employee X for role Y
                    - Compare top performers
                    """)
                with col2:
                    st.markdown("""
                    **Skills & Development:**
                    - What skills are missing?
                    - Create development plan
                    - Identify training needs
                    """)
            
            # Query input with better UX
            user_question = st.text_area(
                "Your Question:",
                placeholder="Example: Who are the best candidates for Manager position?",
                height=80,
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                ask_button = st.button("🚀 Ask Gemini", type="primary", use_container_width=True)
            with col2:
                if st.button("🔄 Clear", use_container_width=True):
                    st.rerun()
            with col3:
                st.empty()  # Spacer
            
            if ask_button and user_question:
                with st.spinner("🤖 Gemini is analyzing the Knowledge Graph..."):
                    # Get KG stats
                    kg_stats = {
                        'employees': len(df),
                        'skills': stats.get('skills', 0),
                        'jobs': stats.get('jobs', 0),
                        'qualified_matches': stats.get('qualified_matches', 0)
                    }
                    
                    # Query Gemini
                    response = query_gemini_about_kg(user_question, df, kg_stats)
                    
                    if response:
                        # Clean response display
                        st.success("**✅ Analysis Complete**")
                        with st.container():
                            st.markdown(response)
                        
                        # Compact deep dive options
                        st.markdown("---")
                        with st.expander("🔍 Advanced Analysis Options", expanded=False):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if st.button("📊 Analyze Employee", use_container_width=True):
                                    st.session_state.show_employee_analysis = True
                            
                            with col2:
                                if st.button("🎯 Career Path", use_container_width=True):
                                    st.session_state.show_career_path = True
                        
                        # Employee Analysis
                        if st.session_state.get('show_employee_analysis'):
                            st.markdown("---")
                            st.markdown("##### 👤 Employee Deep Analysis")
                            
                            selected_emp = st.selectbox(
                                "Select Employee",
                                options=df['employee_id_hash'].unique(),
                                key="ai_emp_select"
                            )
                            
                            if st.button("🔍 Analyze", key="analyze_btn"):
                                emp_data = df[df['employee_id_hash'] == selected_emp].iloc[0]
                                
                                with st.spinner("🤖 Analyzing employee..."):
                                    analysis = analyze_employee_with_gemini(emp_data, selected_emp)
                                    
                                    if analysis:
                                        st.markdown("#### 📋 AI Analysis:")
                                        st.markdown(analysis)
                        
                        # Career Path Generation
                        if st.session_state.get('show_career_path'):
                            st.markdown("---")
                            st.markdown("##### 🎯 Career Path Generator")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                selected_emp_path = st.selectbox(
                                    "Select Employee",
                                    options=df['employee_id_hash'].unique(),
                                    key="ai_path_select"
                                )
                            
                            with col2:
                                target_level = st.selectbox(
                                    "Target Position",
                                    options=["Manager", "Senior Manager", "Director", "Senior Director"],
                                    key="target_level"
                                )
                            
                            if st.button("🚀 Generate Plan", key="gen_plan_btn"):
                                emp_data = df[df['employee_id_hash'] == selected_emp_path].iloc[0]
                                
                                with st.spinner("🤖 Creating personalized career path..."):
                                    career_plan = generate_career_path_with_gemini(emp_data, target_level)
                                    
                                    if career_plan:
                                        st.markdown("#### 🗺️ Personalized Career Development Plan:")
                                        st.markdown(career_plan)
                                        
                                        # Download option
                                        st.download_button(
                                            label="📥 Download Plan",
                                            data=career_plan,
                                            file_name=f"career_plan_{selected_emp_path}.txt",
                                            mime="text/plain"
                                        )
                    else:
                        st.error("❌ Failed to get response from Gemini AI. Please try again.")
        
        else:
            st.error("⚠️ Employee data not found. Please check data/final/integrated_full_dataset.csv")

# ============================================================================
# TAB 3: JOB-FOCUSED VIEW
# ============================================================================
with tab3:
    st.markdown("### 💼 Job-Focused Visualization")
    st.caption("View top candidates for a specific position")
    
    # Get all jobs
    all_jobs = service.get_all_jobs()
    
    if not all_jobs:
        st.warning("No jobs found in the graph.")
    else:
        # Job selector
        job_options = {f"{job['job_title']} ({job['department']})": job['job_id'] for job in all_jobs}
        
        selected_job_label = st.selectbox(
            "Select Job Level",
            options=list(job_options.keys()),
            key="job_select"
        )
        
        selected_job_id = job_options[selected_job_label]
        
        # Number of candidates
        top_n = st.slider(
            "Number of Top Candidates",
            min_value=5,
            max_value=20,
            value=10,
            step=1,
            key="top_n"
        )
        
        # Get job details
        job_details = next((j for j in all_jobs if j['job_id'] == selected_job_id), None)
        
        if job_details:
            # Job requirements
            st.markdown("#### 📋 Position Requirements")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Min Performance", f"{job_details['min_performance']:.0f}")
            with col2:
                st.metric("Min Behavior", f"{job_details['min_behavior']:.0f}")
            with col3:
                st.metric("Min Psychological", f"{job_details['min_psychological']:.0f}")
            with col4:
                st.metric("Qualified Candidates", job_details['qualified_candidates'])
            
            st.markdown("---")
            
            # Generate job-focused graph
            with st.spinner("Generating job-focused graph..."):
                html = create_job_focused_graph(
                    service.graph,
                    selected_job_id,
                    top_n=top_n
                )
                
                components.html(html, height=650, scrolling=True)
            
            # Top candidates table
            st.markdown("#### 🏆 Top Candidates Details")
            
            top_candidates = service.get_top_candidates(selected_job_id, top_n=top_n)
            
            if top_candidates:
                import pandas as pd
                
                df_candidates = pd.DataFrame([
                    {
                        'Rank': i+1,
                        'Name': c['name'],
                        'Match Score': f"{c['match_score']:.1f}%",
                        'Performance': f"{c['performance_score']:.1f}",
                        'Behavior': f"{c['behavior_avg']:.1f}",
                        'Psychological': f"{c['psychological_score']:.1f}",
                        'Leadership': f"{c['leadership_potential']:.1f}",
                        'Tenure': f"{c['tenure_years']:.0f}y"
                    }
                    for i, c in enumerate(top_candidates)
                ])
                
                st.dataframe(df_candidates, use_container_width=True, hide_index=True)
            else:
                st.info("No qualified candidates found for this position.")

# ============================================================================
# TAB 4: FULL GRAPH
# ============================================================================
with tab4:
    st.markdown("### 🌐 Interactive Knowledge Graph")
    st.caption("Explore the complete network of employees, jobs, and skills")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get all departments
        departments = set()
        for node_id in service.graph.nodes():
            node_data = service.graph.nodes[node_id]
            if node_data.get('node_type') == 'job':
                departments.add(node_data.get('department', 'Unknown'))
        
        department_filter = st.selectbox(
            "Filter by Department",
            options=["All"] + sorted(list(departments)),
            key="dept_filter_full"
        )
    
    with col2:
        show_employees = st.checkbox("Show Employees", value=True, key="show_emp_full")
    
    with col3:
        max_employees = st.slider(
            "Max Employees to Display",
            min_value=10,
            max_value=100,
            value=50,
            step=10,
            key="max_emp_full"
        )
    
    # Generate graph
    with st.spinner("Generating interactive graph..."):
        html = create_interactive_graph(
            service.graph,
            department_filter=department_filter if department_filter != "All" else None,
            show_employees=show_employees,
            show_jobs=True,
            show_skills=True,
            max_employees=max_employees,
            height="700px"
        )
        
        # Display graph
        components.html(html, height=750, scrolling=True)
    
    # Legend
    st.markdown("---")
    st.markdown("### 📌 Legend")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("🔵 **Employee** - Purple circles")
        st.caption("Size indicates importance")
    
    with col2:
        st.markdown("🟢 **Job Level** - Green boxes")
        st.caption("Hover for requirements")
    
    with col3:
        st.markdown("🔺 **Skill** - Pink triangles")
        st.caption("Hover for category")
    
    with col4:
        st.markdown("⭐ **Department** - Yellow stars")
        st.caption("Organizational units")

# ============================================================================
# TAB 5: GUIDE
# ============================================================================
with tab5:
    st.markdown("### 📖 How to Use Knowledge Graph")
    
    st.markdown("""
    #### 🎯 What is a Knowledge Graph?
    
    A Knowledge Graph is a network of interconnected entities (nodes) and their relationships (edges).
    In MPCIM, it represents:
    - **Employees** and their skills, scores, and qualifications
    - **Job Levels** and their requirements
    - **Skills** and their importance
    - **Relationships** between all these entities
    
    #### 🔍 How to Explore
    
    **Full Graph View**:
    1. Use filters to focus on specific departments
    2. Toggle employee visibility to reduce clutter
    3. Adjust max employees to control graph size
    4. **Hover** over nodes to see details
    5. **Click and drag** to move nodes
    6. **Scroll** to zoom in/out
    
    **Job-Focused View**:
    1. Select a job level from the dropdown
    2. View requirements and qualified candidates count
    3. See top N candidates ranked by match score
    4. Explore the focused graph showing job-candidate relationships
    
    #### 🎨 Visual Elements
    
    **Node Colors**:
    - 🔵 Purple = Employees
    - 🟢 Green = Job Levels
    - 🔺 Pink = Skills
    - ⭐ Yellow = Departments
    
    **Edge Colors & Thickness**:
    - Darker/Thicker = Higher match score or proficiency
    - Lighter/Thinner = Lower match score or proficiency
    
    **Node Sizes**:
    - Larger nodes = More important or higher scores
    - Smaller nodes = Less important or lower scores
    
    #### 💡 Use Cases
    
    1. **Talent Pool Visualization**: See all qualified candidates for a position
    2. **Skill Gap Analysis**: Identify missing skills in the organization
    3. **Career Path Planning**: Explore progression opportunities
    4. **Succession Planning**: Find backup candidates for key positions
    5. **Department Analysis**: Compare talent across departments
    
    #### 🚀 Tips
    
    - Start with **Job-Focused View** for specific insights
    - Use **Full Graph** for exploratory analysis
    - Filter by department to reduce complexity
    - Hover over nodes for detailed information
    - Take screenshots for presentations
    
    #### 📊 Metrics Explained
    
    - **Match Score**: Overall fit (0-100%) based on Performance (30%), Behavioral (25%), Psychological (25%), and Skills (20%)
    - **Qualified Matches**: Number of employee-job pairs with match score ≥ 70%
    - **Proficiency**: Skill level from 1 (beginner) to 5 (expert)
    """)
    
    st.markdown("---")
    st.info("💡 **Pro Tip**: Use this graph to identify high-potential employees and plan their career development!")

# Footer
st.markdown("---")
st.caption("MPCIM Knowledge Graph • Built with NetworkX & Pyvis • © 2025")
