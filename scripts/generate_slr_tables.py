"""
Generate SLR Tables as Images for IEEE Paper
Author: Deni Sulaeman
Date: December 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# Output directory
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results', 'slr_diagrams')
os.makedirs(output_dir, exist_ok=True)

# Set style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 9


def create_table_2a():
    """TABLE II-A: Comparison of Employee Promotion Prediction Studies"""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.axis('off')
    
    # Data
    headers = ['Author (Year)', 'Dataset\nSize', 'Dimensions Used', 'Algorithm', 'Best\nAUC-ROC', 'Explainability']
    data = [
        ['Alqahtani & Almaleh (2022)', '54,808', 'Performance only', 'XGBoost, RF', '0.84', 'None'],
        ['Jafor et al. (2023)', '8,000', 'Performance only', 'AdaBoost', '0.87', 'None'],
        ['Shafie et al. (2023)', '14,999', 'Performance + Demographics', 'RF, SVM', '0.82', 'None'],
        ['Ilwani & Nassreddine (2023)', '1,470', 'Performance only', 'XGBoost', '0.78', 'None'],
        ['Wang et al. (2024)', '10,000', 'Performance + Demographics', 'Ensemble', '0.85', 'Partial'],
        ['Bhattacharya et al. (2023)', '5,000', 'Performance only', 'RF, XGBoost', '0.81', 'LIME, SHAP'],
        ['This Study (MPCIM)', '1,000', 'Perf + Behav + Psychological', 'RF, XGBoost, NN', '0.901', 'SHAP + AI Narratives'],
    ]
    
    # Colors
    header_color = '#4472C4'
    row_colors = ['#FFFFFF', '#F2F2F2']
    highlight_color = '#FFF2CC'
    
    # Create table
    table = ax.table(
        cellText=data,
        colLabels=headers,
        loc='center',
        cellLoc='center',
        colWidths=[0.22, 0.08, 0.20, 0.15, 0.08, 0.15]
    )
    
    # Style
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.8)
    
    # Header style
    for j in range(len(headers)):
        table[(0, j)].set_facecolor(header_color)
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    
    # Row style
    for i in range(1, len(data) + 1):
        for j in range(len(headers)):
            if i == len(data):  # Last row (This Study)
                table[(i, j)].set_facecolor(highlight_color)
                table[(i, j)].set_text_props(fontweight='bold')
            else:
                table[(i, j)].set_facecolor(row_colors[i % 2])
    
    ax.set_title('TABLE II-A: COMPARISON OF EMPLOYEE PROMOTION PREDICTION STUDIES (2020-2025)', 
                 fontsize=12, fontweight='bold', pad=20, color='#2C3E50')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_table_IIA_promotion_studies.png'), dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.savefig(os.path.join(output_dir, '02_table_IIA_promotion_studies.pdf'), 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ TABLE II-A saved")


def create_table_2b():
    """TABLE II-B: Multi-Dimensional Assessment Approaches"""
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.axis('off')
    
    headers = ['Author (Year)', 'Dimensions', 'Method', 'Key Finding']
    data = [
        ['Aljbour et al. (2022)', 'Multiple (SLR)', 'Systematic Review', 'Multi-level framework needed'],
        ['Zhang & Yuan (2022)', 'Competency + AI', 'Neural Network', '18% improvement over single-dim'],
        ['Liu (2021)', 'Psychology + Competence', 'Mixed Methods', 'Psychological factors critical'],
        ['Mujtaba & Mubarik (2022)', 'Green competencies + Talent', 'Structural Equation', 'Sustainable behavior mediates'],
        ['This Study (MPCIM)', 'Perf + Behav + Psychological', 'ML + XAI', '24.6% improvement'],
    ]
    
    header_color = '#70AD47'
    row_colors = ['#FFFFFF', '#E2EFDA']
    highlight_color = '#FFF2CC'
    
    table = ax.table(
        cellText=data,
        colLabels=headers,
        loc='center',
        cellLoc='center',
        colWidths=[0.22, 0.22, 0.18, 0.30]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.8)
    
    for j in range(len(headers)):
        table[(0, j)].set_facecolor(header_color)
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    
    for i in range(1, len(data) + 1):
        for j in range(len(headers)):
            if i == len(data):
                table[(i, j)].set_facecolor(highlight_color)
                table[(i, j)].set_text_props(fontweight='bold')
            else:
                table[(i, j)].set_facecolor(row_colors[i % 2])
    
    ax.set_title('TABLE II-B: MULTI-DIMENSIONAL ASSESSMENT APPROACHES IN TALENT MANAGEMENT', 
                 fontsize=12, fontweight='bold', pad=20, color='#2C3E50')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_table_IIB_multidim_assessment.png'), dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.savefig(os.path.join(output_dir, '03_table_IIB_multidim_assessment.pdf'), 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ TABLE II-B saved")


def create_table_2c():
    """TABLE II-C: Explainable AI Applications in HR"""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.axis('off')
    
    headers = ['Author (Year)', 'HR Application', 'XAI Technique', 'Key Contribution']
    data = [
        ['Marín Díaz et al. (2023)', 'Employee Attrition', 'SHAP + AHP', 'Strategic HR decision-making'],
        ['Das et al. (2022)', 'Employee Attrition', 'SHAP + LIME', 'Feature explanation framework'],
        ['Abonamah et al. (2022)', 'Attrition Prediction', 'XAI Computational', 'Mid-size company application'],
        ['Al Akasheh et al. (2024)', 'Employee Turnover', 'KG + XAI', 'Knowledge graph integration'],
        ['Baum et al. (2023)', 'AI Adoption in HR', 'XAI Impact Study', 'Explanation enhances adoption'],
        ['Langer & König (2022)', 'HR Decision Support', 'XAI Framework', 'Applied XAI taxonomy for HR'],
        ['This Study (MPCIM)', 'Promotion Prediction', 'SHAP + AI Narratives', 'First multi-dim promotion XAI'],
    ]
    
    header_color = '#FFC000'
    row_colors = ['#FFFFFF', '#FFF2CC']
    highlight_color = '#FCE4D6'
    
    table = ax.table(
        cellText=data,
        colLabels=headers,
        loc='center',
        cellLoc='center',
        colWidths=[0.22, 0.18, 0.18, 0.32]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.8)
    
    for j in range(len(headers)):
        table[(0, j)].set_facecolor(header_color)
        table[(0, j)].set_text_props(color='#2C3E50', fontweight='bold')
    
    for i in range(1, len(data) + 1):
        for j in range(len(headers)):
            if i == len(data):
                table[(i, j)].set_facecolor(highlight_color)
                table[(i, j)].set_text_props(fontweight='bold')
            else:
                table[(i, j)].set_facecolor(row_colors[i % 2])
    
    ax.set_title('TABLE II-C: EXPLAINABLE AI APPLICATIONS IN HR (2020-2025)', 
                 fontsize=12, fontweight='bold', pad=20, color='#2C3E50')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_table_IIC_xai_applications.png'), dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.savefig(os.path.join(output_dir, '04_table_IIC_xai_applications.pdf'), 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ TABLE II-C saved")


def create_table_2d():
    """TABLE II-D: Knowledge Graph Applications in HR"""
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.axis('off')
    
    headers = ['Author (Year)', 'Application', 'Graph Components', 'Key Achievement']
    data = [
        ['Qin et al. (2025)', 'Talent Analytics Survey', 'Comprehensive', 'AI techniques taxonomy'],
        ['Yang et al. (2023)', 'Course Recommendation', 'Skill-Job-Course', 'Explainable recommendations'],
        ['Konstantinidis et al. (2022)', 'Talent Matching', 'Skills-People-Jobs', 'Unsupervised skill extraction'],
        ['Yang & Shen (2025)', 'Competency Prediction', 'Skill-Competency', 'HR management integration'],
        ['This Study (MPCIM)', 'Skill Gap Analysis', 'Employee-Skill-Job', 'Interactive visualization'],
    ]
    
    header_color = '#7030A0'
    row_colors = ['#FFFFFF', '#E4DFEC']
    highlight_color = '#FFF2CC'
    
    table = ax.table(
        cellText=data,
        colLabels=headers,
        loc='center',
        cellLoc='center',
        colWidths=[0.24, 0.20, 0.20, 0.28]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.8)
    
    for j in range(len(headers)):
        table[(0, j)].set_facecolor(header_color)
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    
    for i in range(1, len(data) + 1):
        for j in range(len(headers)):
            if i == len(data):
                table[(i, j)].set_facecolor(highlight_color)
                table[(i, j)].set_text_props(fontweight='bold')
            else:
                table[(i, j)].set_facecolor(row_colors[i % 2])
    
    ax.set_title('TABLE II-D: KNOWLEDGE GRAPH APPLICATIONS IN HR/TALENT ANALYTICS', 
                 fontsize=12, fontweight='bold', pad=20, color='#2C3E50')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_table_IID_knowledge_graph.png'), dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.savefig(os.path.join(output_dir, '05_table_IID_knowledge_graph.pdf'), 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ TABLE II-D saved")


def create_table_2e():
    """TABLE II-E: Research Gap Analysis"""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.axis('off')
    
    headers = ['Gap ID', 'Research Gap', 'Literature Status', 'MPCIM Contribution']
    data = [
        ['G1', 'Single-dimension approach dominates', '85% use performance-only', '[OK] 3-dimensional integration'],
        ['G2', 'Psychological assessment not integrated', '0% systematic integration', '[OK] 9 psychological features'],
        ['G3', 'Limited explainability in promotion', '14% implement XAI', '[OK] SHAP + AI narratives'],
        ['G4', 'No AI-generated narratives for HR', '0% use natural language', '[OK] Gemini/OpenAI integration'],
        ['G5', 'Lack of production-ready tools', 'Mostly prototypes', '[OK] 6-page Streamlit dashboard'],
        ['G6', 'Knowledge graph not utilized', 'Emerging research', '[OK] Interactive KG visualization'],
    ]
    
    header_color = '#C00000'
    row_colors = ['#FFFFFF', '#F2F2F2']
    contribution_color = '#E2EFDA'
    
    table = ax.table(
        cellText=data,
        colLabels=headers,
        loc='center',
        cellLoc='center',
        colWidths=[0.08, 0.30, 0.25, 0.28]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.8)
    
    for j in range(len(headers)):
        table[(0, j)].set_facecolor(header_color)
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    
    for i in range(1, len(data) + 1):
        for j in range(len(headers)):
            if j == 3:  # MPCIM Contribution column
                table[(i, j)].set_facecolor(contribution_color)
                table[(i, j)].set_text_props(color='#006600', fontweight='bold')
            else:
                table[(i, j)].set_facecolor(row_colors[i % 2])
        table[(i, 0)].set_text_props(fontweight='bold')  # Gap ID bold
    
    ax.set_title('TABLE II-E: RESEARCH GAP ANALYSIS AND MPCIM CONTRIBUTION', 
                 fontsize=12, fontweight='bold', pad=20, color='#2C3E50')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_table_IIE_research_gaps.png'), dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.savefig(os.path.join(output_dir, '06_table_IIE_research_gaps.pdf'), 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ TABLE II-E saved")


def create_research_positioning_matrix():
    """Research Positioning Matrix Visualization - Clean Version"""
    fig, ax = plt.subplots(figsize=(12, 9))
    
    # Create grid
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    
    # Quadrant backgrounds
    ax.fill([0, 2, 2, 0], [0, 0, 2, 2], color='#FFE6E6', alpha=0.5)  # Low-Low (bottom-left)
    ax.fill([2, 4, 4, 2], [0, 0, 2, 2], color='#FFF2E6', alpha=0.5)  # Low-High (bottom-right)
    ax.fill([0, 2, 2, 0], [2, 2, 4, 4], color='#E6F2FF', alpha=0.5)  # High-Low (top-left)
    ax.fill([2, 4, 4, 2], [2, 2, 4, 4], color='#E6FFE6', alpha=0.5)  # High-High (top-right - Target)
    
    # Quadrant lines
    ax.axhline(y=2, color='gray', linestyle='--', linewidth=1.5)
    ax.axvline(x=2, color='gray', linestyle='--', linewidth=1.5)
    
    # Studies data: (name, x=dimensions, y=explainability, color, label_offset_x, label_offset_y)
    studies = [
        ('Alqahtani [10]', 0.6, 0.6, '#4472C4', 0.12, 0.08),
        ('Jafor [11]', 0.75, 0.85, '#4472C4', 0.12, 0.08),
        ('Shafie [12]', 1.5, 0.55, '#70AD47', 0.12, 0.08),
        ('Ilwani [13]', 0.55, 0.35, '#4472C4', 0.12, -0.15),
        ('Wang [14]', 1.5, 1.3, '#70AD47', 0.12, 0.08),
        ('Bhattacharya [15]', 1.2, 2.4, '#FFC000', 0.12, 0.08),
    ]
    
    # Plot existing studies
    for name, x, y, color, off_x, off_y in studies:
        ax.scatter(x, y, s=180, c=color, edgecolors='black', linewidth=1.2, zorder=5)
        ax.annotate(name, (x, y), xytext=(x + off_x, y + off_y), fontsize=9, ha='left')
    
    # Plot MPCIM (special - star marker)
    mpcim_x, mpcim_y = 3.3, 3.4
    ax.scatter(mpcim_x, mpcim_y, s=500, c='#ED7D31', edgecolors='black', 
               linewidth=2, zorder=10, marker='*')
    ax.annotate('MPCIM\n(This Study)', (mpcim_x, mpcim_y), 
               xytext=(mpcim_x - 0.55, mpcim_y - 0.45), 
               fontsize=11, fontweight='bold', color='#ED7D31', ha='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                        edgecolor='#ED7D31', linewidth=1.5))
    
    # Quadrant labels (positioned in corners, no overlap)
    # Top-left quadrant
    ax.text(0.15, 3.75, 'High Explainability\nSingle Dimension', 
            ha='left', va='top', fontsize=10, color='#4472C4', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Top-right quadrant (Research Gap area)
    ax.text(3.85, 3.85, 'RESEARCH GAP', ha='right', va='top', fontsize=11, 
            color='#006600', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#90EE90', 
                     edgecolor='#006600', linewidth=2))
    
    # Bottom-left quadrant
    ax.text(0.15, 0.15, 'Low Explainability\nSingle Dimension', 
            ha='left', va='bottom', fontsize=10, color='#C00000', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Bottom-right quadrant
    ax.text(3.85, 0.15, 'Low Explainability\nMulti Dimension', 
            ha='right', va='bottom', fontsize=10, color='#B8860B', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Axis labels
    ax.set_xlabel('Assessment Dimensions', fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylabel('Explainability Level', fontsize=13, fontweight='bold', labelpad=10)
    
    # Custom tick positions and labels
    ax.set_xticks([1, 1.75, 3])
    ax.set_xticklabels(['Single\n(Performance Only)', 'Dual\n(Perf + Demog)', 'Multi (3+)\n(Perf + Behav + Psych)'],
                       fontsize=10)
    ax.set_yticks([0.7, 2, 3.3])
    ax.set_yticklabels(['None', 'Partial\n(Feature Importance)', 'Full\n(SHAP + AI Narratives)'],
                       fontsize=10)
    
    # Title
    ax.set_title('Fig. 1: Research Positioning Matrix\nMPCIM in Employee Promotion Prediction Literature', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Legend (positioned outside overlap area)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#4472C4', 
               markersize=12, markeredgecolor='black', label='Single-dimension'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#70AD47', 
               markersize=12, markeredgecolor='black', label='Dual-dimension'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFC000', 
               markersize=12, markeredgecolor='black', label='With partial XAI'),
        Line2D([0], [0], marker='*', color='w', markerfacecolor='#ED7D31', 
               markersize=18, markeredgecolor='black', label='MPCIM (This Study)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, 
              framealpha=0.95, edgecolor='gray')
    
    # Add grid for better readability
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '07_research_positioning_matrix.png'), dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.savefig(os.path.join(output_dir, '07_research_positioning_matrix.pdf'), 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Research Positioning Matrix saved")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Generating SLR Tables for IEEE Paper")
    print("="*60 + "\n")
    
    create_table_2a()
    create_table_2b()
    create_table_2c()
    create_table_2d()
    create_table_2e()
    create_research_positioning_matrix()
    
    print("\n" + "="*60)
    print(f"All tables saved to: {output_dir}")
    print("="*60)
    print("\nGenerated files:")
    print("  1. 02_table_IIA_promotion_studies.png/pdf")
    print("  2. 03_table_IIB_multidim_assessment.png/pdf")
    print("  3. 04_table_IIC_xai_applications.png/pdf")
    print("  4. 05_table_IID_knowledge_graph.png/pdf")
    print("  5. 06_table_IIE_research_gaps.png/pdf")
    print("  6. 07_research_positioning_matrix.png/pdf")
