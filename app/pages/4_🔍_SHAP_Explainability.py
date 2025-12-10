"""
MPCIM Dashboard - SHAP Explainability Page
Author: Deni Sulaeman
Date: November 24, 2025

Model explainability using SHAP (SHapley Additive exPlanations) values.
Provides interpretable insights into model predictions.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import joblib
from PIL import Image

# Page config
st.set_page_config(
    page_title="SHAP Explainability - MPCIM",
    page_icon="🔍",
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
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1.5rem;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #28a745;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔍 Model Explainability with SHAP</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="info-box">
    <h3>📖 What is SHAP?</h3>
    <p><strong>SHAP (SHapley Additive exPlanations)</strong> adalah metode untuk menjelaskan prediksi model machine learning 
    dengan menghitung kontribusi setiap fitur terhadap prediksi individual.</p>
    <ul>
        <li><strong>Positive SHAP value</strong>: Fitur meningkatkan probabilitas promosi</li>
        <li><strong>Negative SHAP value</strong>: Fitur menurunkan probabilitas promosi</li>
        <li><strong>Magnitude</strong>: Seberapa besar pengaruh fitur tersebut</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Paths
repo_root = Path(__file__).resolve().parents[2]
shap_dir = repo_root / 'results' / 'shap_analysis'
data_dir = repo_root / 'data' / 'processed'

# Check if SHAP analysis exists
if not shap_dir.exists():
    st.error("⚠️ SHAP analysis belum dijalankan. Silakan jalankan script: `scripts/analysis/13_shap_analysis.py`")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Global Importance", 
    "💧 Individual Explanations", 
    "🔗 Feature Interactions",
    "📈 Importance Comparison",
    "📄 Summary Report"
])

# ============================================================================
# TAB 1: GLOBAL IMPORTANCE
# ============================================================================
with tab1:
    st.markdown('<div class="sub-header">Global Feature Importance</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Visualisasi ini menunjukkan fitur mana yang paling berpengaruh terhadap prediksi model secara keseluruhan.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### SHAP Summary Plot")
        st.markdown("Menunjukkan distribusi SHAP values untuk setiap fitur:")
        
        summary_plot = shap_dir / '01_shap_summary_plot.png'
        if summary_plot.exists():
            img = Image.open(summary_plot)
            st.image(img, use_container_width=True)
        else:
            st.warning("Summary plot tidak ditemukan")
    
    with col2:
        st.markdown("#### SHAP Bar Plot")
        st.markdown("Mean absolute SHAP values (rata-rata pengaruh):")
        
        bar_plot = shap_dir / '02_shap_bar_plot.png'
        if bar_plot.exists():
            img = Image.open(bar_plot)
            st.image(img, use_container_width=True)
        else:
            st.warning("Bar plot tidak ditemukan")
    
    # Feature importance table
    st.markdown("#### 📋 Feature Importance Table")
    
    importance_csv = shap_dir / 'feature_importance_comparison.csv'
    if importance_csv.exists():
        df_importance = pd.read_csv(importance_csv)
        
        # Sort by SHAP importance
        df_importance = df_importance.sort_values('SHAP Importance', ascending=False)
        
        # Format for display
        df_display = df_importance[['Feature', 'SHAP Importance', 'Native Importance']].head(15)
        df_display['SHAP Importance'] = df_display['SHAP Importance'].round(4)
        df_display['Native Importance'] = df_display['Native Importance'].round(4)
        df_display['Rank'] = range(1, len(df_display) + 1)
        df_display = df_display[['Rank', 'Feature', 'SHAP Importance', 'Native Importance']]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df_importance.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Importance Table",
            data=csv,
            file_name="feature_importance_comparison.csv",
            mime="text/csv"
        )
    else:
        st.warning("Feature importance table tidak ditemukan")
    
    # Key insights
    st.markdown("""
    <div class="success-box">
        <h4>💡 Key Insights</h4>
        <ul>
            <li><strong>Tenure</strong> adalah fitur paling berpengaruh (40-50% kontribusi)</li>
            <li><strong>Behavioral score</strong> memberikan kontribusi signifikan (4-6%)</li>
            <li><strong>Performance score</strong> berkontribusi dalam kombinasi dengan fitur lain (3-5%)</li>
            <li>Fitur engineered (combined_score, ratios) menambah nilai prediktif (5-8%)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: INDIVIDUAL EXPLANATIONS
# ============================================================================
with tab2:
    st.markdown('<div class="sub-header">Individual Prediction Explanations</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Waterfall plots** menunjukkan bagaimana setiap fitur berkontribusi terhadap prediksi individual.
    Mulai dari base value (rata-rata prediksi), setiap fitur menambah atau mengurangi probabilitas.
    """)
    
    # Case 1: High confidence PROMOTED
    st.markdown("#### Case 1: High Confidence PROMOTED ✅")
    waterfall_promoted = shap_dir / '03_waterfall_promoted.png'
    if waterfall_promoted.exists():
        img = Image.open(waterfall_promoted)
        st.image(img, use_container_width=True)
        
        st.markdown("""
        <div class="info-box">
            <strong>Interpretasi:</strong> Karyawan ini memiliki probabilitas tinggi untuk dipromosikan.
            Fitur-fitur yang mendorong prediksi ini (warna merah) lebih dominan dibanding yang menghambat (warna biru).
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Case 2: High confidence NOT PROMOTED
    st.markdown("#### Case 2: High Confidence NOT PROMOTED ❌")
    waterfall_not = shap_dir / '04_waterfall_not_promoted.png'
    if waterfall_not.exists():
        img = Image.open(waterfall_not)
        st.image(img, use_container_width=True)
        
        st.markdown("""
        <div class="info-box">
            <strong>Interpretasi:</strong> Karyawan ini memiliki probabilitas rendah untuk dipromosikan.
            Fitur-fitur yang menghambat promosi (warna biru) lebih dominan.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Case 3: Borderline
    st.markdown("#### Case 3: Borderline Case ⚖️")
    waterfall_border = shap_dir / '05_waterfall_borderline.png'
    if waterfall_border.exists():
        img = Image.open(waterfall_border)
        st.image(img, use_container_width=True)
        
        st.markdown("""
        <div class="info-box">
            <strong>Interpretasi:</strong> Kasus borderline dimana prediksi mendekati threshold (50%).
            Fitur positif dan negatif hampir seimbang, memerlukan pertimbangan lebih lanjut dari HR.
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive prediction (if data available)
    st.markdown("---")
    st.markdown("#### 🎯 Analyze Your Own Case")
    
    if (data_dir / 'X_test.csv').exists() and (shap_dir / 'shap_values.npy').exists():
        try:
            X_test = pd.read_csv(data_dir / 'X_test.csv')
            
            # Load SHAP values
            shap_values = np.load(shap_dir / 'shap_values.npy')
            
            # Handle 2D or 3D SHAP arrays (for binary classification)
            if len(shap_values.shape) == 3:
                # For binary classification, take values for class 1 (promoted)
                shap_values = shap_values[:, :, 1]
            elif len(shap_values.shape) == 2:
                # Already in correct format
                pass
            else:
                st.error(f"⚠️ Unexpected SHAP values shape: {shap_values.shape}")
                st.stop()
            
            # Verify dimensions match
            if shap_values.shape[1] != X_test.shape[1]:
                st.error(f"⚠️ Dimension mismatch: SHAP ({shap_values.shape[1]} features) vs X_test ({X_test.shape[1]} features)")
                st.info(f"SHAP shape: {shap_values.shape}, X_test shape: {X_test.shape}")
                st.stop()
            
            # Select a case
            case_idx = st.slider("Select test case index:", 0, len(X_test)-1, 0)
        except Exception as e:
            st.error(f"⚠️ Error loading data: {str(e)}")
            st.stop()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Feature Values:**")
            case_data = X_test.iloc[case_idx]
            st.dataframe(case_data.to_frame(name='Value'), use_container_width=True)
        
        with col2:
            st.markdown("**SHAP Values:**")
            # Ensure array lengths match
            shap_vals = shap_values[case_idx]
            if len(shap_vals) != len(X_test.columns):
                st.error(f"⚠️ Array length mismatch: SHAP values ({len(shap_vals)}) vs Features ({len(X_test.columns)})")
                st.stop()
            
            case_shap = pd.DataFrame({
                'Feature': X_test.columns,
                'SHAP Value': shap_vals
            })
            case_shap = case_shap.sort_values('SHAP Value', key=abs, ascending=False)
            
            # Color code
            def color_shap(val):
                color = 'red' if val > 0 else 'blue'
                return f'color: {color}'
            
            st.dataframe(
                case_shap.style.applymap(color_shap, subset=['SHAP Value']),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.warning("⚠️ Test data atau SHAP values tidak ditemukan. Jalankan script SHAP analysis terlebih dahulu.")
        st.info("""
        **Cara menjalankan SHAP analysis:**
        ```bash
        python scripts/analysis/13_shap_analysis.py
        ```
        """)


# ============================================================================
# TAB 3: FEATURE INTERACTIONS
# ============================================================================
with tab3:
    st.markdown('<div class="sub-header">Feature Interactions & Dependencies</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Dependence plots** menunjukkan bagaimana nilai suatu fitur mempengaruhi prediksi,
    dan bagaimana pengaruh tersebut berinteraksi dengan fitur lain (ditunjukkan oleh warna).
    """)
    
    # Display dependence plots
    dependence_plots = sorted(shap_dir.glob('06_dependence_*.png'))
    
    if dependence_plots:
        for i, plot_path in enumerate(dependence_plots):
            if i % 2 == 0:
                cols = st.columns(2)
            
            with cols[i % 2]:
                # Extract feature name from filename
                feature_name = plot_path.stem.split('_', 3)[-1]
                st.markdown(f"#### {feature_name.replace('_', ' ').title()}")
                
                img = Image.open(plot_path)
                st.image(img, use_container_width=True)
    else:
        st.warning("Dependence plots tidak ditemukan")
    
    st.markdown("""
    <div class="info-box">
        <h4>💡 How to Read Dependence Plots</h4>
        <ul>
            <li><strong>X-axis</strong>: Nilai fitur yang dianalisis</li>
            <li><strong>Y-axis</strong>: SHAP value (pengaruh terhadap prediksi)</li>
            <li><strong>Color</strong>: Nilai fitur lain yang berinteraksi</li>
            <li><strong>Trend</strong>: Hubungan non-linear antara fitur dan prediksi</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 4: IMPORTANCE COMPARISON
# ============================================================================
with tab4:
    st.markdown('<div class="sub-header">Native vs SHAP Importance Comparison</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Membandingkan **feature importance** dari model (native) dengan **SHAP importance** (dari prediksi).
    SHAP importance lebih akurat karena menghitung kontribusi aktual terhadap setiap prediksi.
    """)
    
    comparison_plot = shap_dir / '09_importance_comparison.png'
    if comparison_plot.exists():
        img = Image.open(comparison_plot)
        st.image(img, use_container_width=True)
    else:
        st.warning("Comparison plot tidak ditemukan")
    
    # Interactive comparison
    if (shap_dir / 'feature_importance_comparison.csv').exists():
        df_comp = pd.read_csv(shap_dir / 'feature_importance_comparison.csv')
        
        # Normalize
        df_comp['Native (%)'] = (df_comp['Native Importance'] / df_comp['Native Importance'].sum() * 100).round(2)
        df_comp['SHAP (%)'] = (df_comp['SHAP Importance'] / df_comp['SHAP Importance'].sum() * 100).round(2)
        df_comp['Difference (%)'] = (df_comp['SHAP (%)'] - df_comp['Native (%)']).round(2)
        
        # Sort by SHAP importance
        df_comp = df_comp.sort_values('SHAP Importance', ascending=False).head(15)
        
        # Create interactive bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Native Importance',
            x=df_comp['Feature'],
            y=df_comp['Native (%)'],
            marker_color='coral'
        ))
        
        fig.add_trace(go.Bar(
            name='SHAP Importance',
            x=df_comp['Feature'],
            y=df_comp['SHAP (%)'],
            marker_color='steelblue'
        ))
        
        fig.update_layout(
            title='Feature Importance Comparison (Top 15)',
            xaxis_title='Feature',
            yaxis_title='Importance (%)',
            barmode='group',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        st.markdown("#### 📊 Detailed Comparison")
        st.dataframe(
            df_comp[['Feature', 'Native (%)', 'SHAP (%)', 'Difference (%)']],
            use_container_width=True,
            hide_index=True
        )

# ============================================================================
# TAB 5: SUMMARY REPORT
# ============================================================================
with tab5:
    st.markdown('<div class="sub-header">SHAP Analysis Summary Report</div>', unsafe_allow_html=True)
    
    report_path = shap_dir / 'SHAP_ANALYSIS_REPORT.md'
    if report_path.exists():
        with open(report_path, 'r') as f:
            report_content = f.read()
        
        st.markdown(report_content)
        
        # Download button
        st.download_button(
            label="📥 Download Full Report",
            data=report_content,
            file_name="SHAP_ANALYSIS_REPORT.md",
            mime="text/markdown"
        )
    else:
        st.warning("Summary report tidak ditemukan")
    
    # Additional statistics
    st.markdown("---")
    st.markdown("#### 📈 Analysis Statistics")
    
    if (shap_dir / 'shap_values.npy').exists():
        shap_values = np.load(shap_dir / 'shap_values.npy')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Test Samples", f"{shap_values.shape[0]:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Features", shap_values.shape[1])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            mean_abs_shap = np.abs(shap_values).mean()
            st.metric("Mean |SHAP|", f"{mean_abs_shap:.4f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            max_abs_shap = np.abs(shap_values).max()
            st.metric("Max |SHAP|", f"{max_abs_shap:.4f}")
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p><strong>MPCIM Thesis Project</strong> - Model Explainability with SHAP</p>
    <p>Deni Sulaeman | Master Program in Information Systems</p>
</div>
""", unsafe_allow_html=True)
