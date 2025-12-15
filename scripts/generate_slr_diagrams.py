"""
Generate SLR (Systematic Literature Review) Diagrams for IEEE Paper
Author: Deni Sulaeman
Date: December 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Create output directory
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results', 'slr_diagrams')
os.makedirs(output_dir, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def create_prisma_diagram():
    """Create PRISMA Flow Diagram for SLR - Clean Professional Design"""
    fig, ax = plt.subplots(figsize=(11, 13))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 13)
    ax.axis('off')
    
    # Professional Colors
    colors = {
        'identification': '#1E88E5',  # Blue
        'screening': '#43A047',       # Green
        'eligibility': '#FB8C00',     # Orange
        'included': '#E53935',        # Red
        'excluded': '#757575',        # Gray
        'arrow': '#37474F',           # Dark gray
        'text': '#212121',            # Almost black
        'white': '#FFFFFF'
    }
    
    # Title
    ax.text(5.5, 12.5, 'PRISMA 2020 Flow Diagram', 
            fontsize=16, fontweight='bold', ha='center', va='center', color=colors['text'])
    ax.text(5.5, 12.1, 'Systematic Literature Review - Employee Promotion Prediction', 
            fontsize=10, ha='center', va='center', color='#616161')
    
    # =================================================================
    # PHASE LABELS (Left side - vertical)
    # =================================================================
    phase_labels = [
        ('IDENTIFICATION', 10.3, colors['identification']),
        ('SCREENING', 7.8, colors['screening']),
        ('ELIGIBILITY', 5.3, colors['eligibility']),
        ('INCLUDED', 2.2, colors['included']),
    ]
    
    for label, y, color in phase_labels:
        ax.text(0.15, y, label, fontsize=9, fontweight='bold', rotation=90,
                ha='center', va='center', color=color)
        # Vertical line
        ax.plot([0.35, 0.35], [y-1, y+1], color=color, linewidth=3, solid_capstyle='round')
    
    # =================================================================
    # IDENTIFICATION SECTION
    # =================================================================
    # Main box
    main_box_1 = FancyBboxPatch((1, 9.5), 9, 2,
                                boxstyle="round,pad=0.03,rounding_size=0.2",
                                facecolor=colors['identification'], alpha=0.08,
                                edgecolor=colors['identification'], linewidth=2)
    ax.add_patch(main_box_1)
    
    # Database search description
    ax.text(5.5, 11.1, 'Records identified through database searching',
            fontsize=11, fontweight='bold', ha='center', va='center', color=colors['text'])
    
    # Database row
    databases = ['IEEE Xplore', 'ScienceDirect', 'ACM DL', 'Springer', 'Google Scholar']
    counts = [82, 125, 58, 98, 124]
    x_positions = [1.8, 3.6, 5.5, 7.4, 9.2]
    
    for db, n, x in zip(databases, counts, x_positions):
        # Small box for each database
        db_box = FancyBboxPatch((x-0.7, 10.1), 1.4, 0.7,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=colors['white'],
                                edgecolor=colors['identification'], linewidth=1)
        ax.add_patch(db_box)
        ax.text(x, 10.55, db, fontsize=7, ha='center', va='center', fontweight='bold')
        ax.text(x, 10.25, f'(n={n})', fontsize=7, ha='center', va='center', color='#616161')
    
    # Total box
    total_box = FancyBboxPatch((3.5, 9.65), 4, 0.55,
                               boxstyle="round,pad=0.02,rounding_size=0.1",
                               facecolor=colors['identification'], alpha=0.2,
                               edgecolor=colors['identification'], linewidth=1.5)
    ax.add_patch(total_box)
    ax.text(5.5, 9.92, 'Total Records Identified: n = 487',
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Arrow down
    ax.annotate('', xy=(5.5, 9), xytext=(5.5, 9.6),
                arrowprops=dict(arrowstyle='-|>', color=colors['arrow'], lw=2.5,
                               mutation_scale=15))
    
    # =================================================================
    # SCREENING SECTION
    # =================================================================
    main_box_2 = FancyBboxPatch((1, 7), 9, 1.8,
                                boxstyle="round,pad=0.03,rounding_size=0.2",
                                facecolor=colors['screening'], alpha=0.08,
                                edgecolor=colors['screening'], linewidth=2)
    ax.add_patch(main_box_2)
    
    # Left: After duplicates
    left_box = FancyBboxPatch((1.5, 7.35), 3.2, 1.1,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor=colors['white'],
                              edgecolor=colors['screening'], linewidth=1.5)
    ax.add_patch(left_box)
    ax.text(3.1, 8.05, 'Records after duplicates', fontsize=9, ha='center', va='center')
    ax.text(3.1, 7.75, 'removed', fontsize=9, ha='center', va='center')
    ax.text(3.1, 7.45, 'n = 342', fontsize=10, fontweight='bold', ha='center', va='center',
            color=colors['screening'])
    
    # Arrow to excluded
    ax.annotate('', xy=(5.2, 7.9), xytext=(4.8, 7.9),
                arrowprops=dict(arrowstyle='-|>', color=colors['excluded'], lw=1.5,
                               mutation_scale=12))
    
    # Right: Excluded
    right_box = FancyBboxPatch((5.4, 7.35), 4.2, 1.1,
                               boxstyle="round,pad=0.02,rounding_size=0.1",
                               facecolor=colors['excluded'], alpha=0.1,
                               edgecolor=colors['excluded'], linewidth=1.5)
    ax.add_patch(right_box)
    ax.text(7.5, 8.05, 'Records excluded', fontsize=9, ha='center', va='center',
            color=colors['excluded'], fontweight='bold')
    ax.text(7.5, 7.75, '(Not relevant by title/abstract)', fontsize=8, ha='center', va='center',
            color='#616161')
    ax.text(7.5, 7.45, 'n = 248', fontsize=10, fontweight='bold', ha='center', va='center',
            color=colors['excluded'])
    
    # Arrow down
    ax.annotate('', xy=(3.1, 6.5), xytext=(3.1, 7.3),
                arrowprops=dict(arrowstyle='-|>', color=colors['arrow'], lw=2.5,
                               mutation_scale=15))
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 3: ELIGIBILITY
    # ═══════════════════════════════════════════════════════════════
    phase_y = 4.8
    
    # Phase background
    draw_box(0.5, phase_y, 11, 1.8, colors['eligibility'], '', alpha=0.1)
    ax.text(0.8, phase_y + 1.55, 'ELIGIBILITY', fontsize=11, fontweight='bold',
            ha='left', va='top', color=colors['eligibility'])
    
    # Left box - Full-text assessed
    draw_content_box(1.5, phase_y + 0.4, 3.8, 0.9, colors['eligibility'],
                    'Full-text articles assessed\nfor eligibility (n = 94)', fontsize=9)
    
    # Right box - Excluded with reasons
    excl_box2 = FancyBboxPatch((6.8, phase_y + 0.15), 4, 1.4,
                               boxstyle="round,pad=0.02,rounding_size=0.1",
                               facecolor=colors['excluded'], alpha=0.1,
                               edgecolor=colors['excluded'], linewidth=1.5)
    ax.add_patch(excl_box2)
    ax.text(8.8, phase_y + 0.85, 'Full-text articles excluded (n = 56)\n'
                                  '• Not empirical study (n=18)\n'
                                  '• No ML methods used (n=22)\n'
                                  '• Low quality score (n=16)',
            fontsize=8, ha='center', va='center', color=colors['excluded'])
    
    # Arrow to excluded
    ax.annotate('', xy=(6.7, phase_y + 0.85), xytext=(5.4, phase_y + 0.85),
                arrowprops=dict(arrowstyle='-|>', color=colors['excluded'], lw=1.5,
                               mutation_scale=12))
    
    # Arrow down from eligibility
    ax.annotate('', xy=(3.4, 4.0), xytext=(3.4, 4.7),
                arrowprops=dict(arrowstyle='-|>', color=colors['arrow'], lw=2,
                               mutation_scale=15))
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 4: INCLUDED
    # ═══════════════════════════════════════════════════════════════
    phase_y = 1.0
    
    # Phase background
    draw_box(0.5, phase_y, 11, 2.8, colors['included'], '', alpha=0.1)
    ax.text(0.8, phase_y + 2.55, 'INCLUDED', fontsize=11, fontweight='bold',
            ha='left', va='top', color=colors['included'])
    
    # Main included box
    inc_box = FancyBboxPatch((2.5, phase_y + 1.7), 7, 0.7,
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor=colors['included'], alpha=0.2,
                             edgecolor=colors['included'], linewidth=2)
    ax.add_patch(inc_box)
    ax.text(6, phase_y + 2.05, 'Studies included in qualitative synthesis (n = 38)',
            fontsize=11, fontweight='bold', ha='center', va='center', color=colors['text_dark'])
    
    # Category boxes - evenly distributed
    categories = [
        ('Promotion\nPrediction\nwith ML\n(n=14)', 1.7),
        ('Multi-dim\nAssessment\nFrameworks\n(n=10)', 4.4),
        ('Explainable\nAI for HR\nDecisions\n(n=9)', 7.1),
        ('Knowledge\nGraph for\nSkills\n(n=5)', 9.8)
    ]
    
    cat_width = 2.2
    cat_height = 1.1
    cat_y = phase_y + 0.25
    
    for cat_text, x in categories:
        cat_box = FancyBboxPatch((x - cat_width/2, cat_y), cat_width, cat_height,
                                 boxstyle="round,pad=0.02,rounding_size=0.1",
                                 facecolor='white', edgecolor=colors['included'], linewidth=1.2)
        ax.add_patch(cat_box)
        ax.text(x, cat_y + cat_height/2, cat_text, fontsize=8, ha='center', va='center',
                color=colors['text_dark'])
    
    # Arrows from main to categories
    for cat_text, x in categories:
        ax.annotate('', xy=(x, cat_y + cat_height), xytext=(x, phase_y + 1.65),
                   arrowprops=dict(arrowstyle='-|>', color=colors['included'], lw=1,
                                  mutation_scale=10, alpha=0.7))
    
    # ═══════════════════════════════════════════════════════════════
    # LEGEND
    # ═══════════════════════════════════════════════════════════════
    legend_x = 9.8
    legend_y = 0.15
    ax.text(legend_x, legend_y + 0.6, 'Legend:', fontsize=9, fontweight='bold', va='bottom')
    
    legend_items = [
        (colors['identification'], 'Identification'),
        (colors['screening'], 'Screening'),
        (colors['eligibility'], 'Eligibility'),
        (colors['included'], 'Included'),
    ]
    
    for i, (color, label) in enumerate(legend_items):
        rect_x = legend_x
        rect_y = legend_y + 0.35 - i * 0.32
        ax.add_patch(plt.Rectangle((rect_x, rect_y), 0.25, 0.2, 
                                   facecolor=color, alpha=0.5, edgecolor='black', linewidth=0.5))
        ax.text(rect_x + 0.35, rect_y + 0.1, label, fontsize=7, va='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_prisma_flow_diagram.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(output_dir, '01_prisma_flow_diagram.pdf'), bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ PRISMA Flow Diagram saved")


def create_research_gap_matrix():
    """Create Research Gap Positioning Matrix"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Data for studies
    studies = {
        'Alqahtani (2022) [10]': (1, 1, 'o', '#4472C4', 100),
        'Jafor (2023) [11]': (1, 1.2, 'o', '#4472C4', 100),
        'Shafie (2023) [12]': (1.5, 1, 's', '#70AD47', 100),
        'Ilwani (2023) [13]': (1, 0.8, 'o', '#4472C4', 100),
        'Wang (2024) [14]': (1.5, 1.5, 's', '#70AD47', 100),
        'Bhattacharya (2023) [15]': (1, 2.5, 'D', '#FFC000', 120),
        'MPCIM (This Study)': (3, 3, '*', '#ED7D31', 400)
    }
    
    # Plot studies
    for name, (x, y, marker, color, size) in studies.items():
        ax.scatter(x, y, marker=marker, c=color, s=size, edgecolors='black', linewidth=1.5, zorder=5)
        
        # Add labels with offset
        offset_x = 0.15 if x < 2.5 else -0.15
        offset_y = 0.15
        ha = 'left' if x < 2.5 else 'right'
        
        if name == 'MPCIM (This Study)':
            ax.annotate(name, (x, y), xytext=(x+0.2, y+0.2), fontsize=11, fontweight='bold',
                       color='#ED7D31', ha='left',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF2E6', edgecolor='#ED7D31'))
        else:
            ax.annotate(name, (x, y), xytext=(x+offset_x, y+offset_y), fontsize=9, ha=ha)
    
    # Add quadrant labels
    ax.text(1.25, 0.3, 'Low Explainability\nSingle Dimension', fontsize=10, ha='center', 
            va='center', style='italic', color='gray')
    ax.text(2.75, 0.3, 'Low Explainability\nMulti-Dimension', fontsize=10, ha='center',
            va='center', style='italic', color='gray')
    ax.text(1.25, 3.5, 'High Explainability\nSingle Dimension', fontsize=10, ha='center',
            va='center', style='italic', color='gray')
    ax.text(2.75, 3.5, 'High Explainability\nMulti-Dimension\n(RESEARCH GAP)', fontsize=10, ha='center',
            va='center', style='italic', color='#ED7D31', fontweight='bold')
    
    # Add quadrant dividers
    ax.axhline(y=2, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax.axvline(x=2, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    # Highlight research gap area
    from matplotlib.patches import Rectangle
    gap_rect = Rectangle((2, 2), 1.5, 2, linewidth=2, edgecolor='#ED7D31', 
                          facecolor='#ED7D31', alpha=0.1, linestyle='--')
    ax.add_patch(gap_rect)
    
    # Labels
    ax.set_xlabel('Assessment Dimensions', fontsize=12, fontweight='bold')
    ax.set_ylabel('Explainability Level', fontsize=12, fontweight='bold')
    ax.set_title('Research Gap Analysis: Positioning of MPCIM Framework\nin Employee Promotion Prediction Literature', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Axis settings
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0, 4)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Single\n(Performance)', 'Dual\n(Perf + Behavioral)', 'Multi (3+)\n(Perf + Behav + Psych)'])
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['None', 'Partial\n(Feature Importance)', 'Full\n(SHAP + AI Narratives)'])
    
    # Legend
    legend_elements = [
        plt.scatter([], [], marker='o', c='#4472C4', s=100, edgecolors='black', label='Single-dimension studies'),
        plt.scatter([], [], marker='s', c='#70AD47', s=100, edgecolors='black', label='Dual-dimension studies'),
        plt.scatter([], [], marker='D', c='#FFC000', s=100, edgecolors='black', label='With partial XAI'),
        plt.scatter([], [], marker='*', c='#ED7D31', s=300, edgecolors='black', label='MPCIM (This Study)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_research_gap_matrix.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(output_dir, '02_research_gap_matrix.pdf'), bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Research Gap Matrix saved")


def create_literature_comparison_chart():
    """Create bar chart comparing literature approaches"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Chart 1: AUC-ROC Comparison
    ax1 = axes[0]
    studies = ['Alqahtani\n(2022)', 'Jafor\n(2023)', 'Shafie\n(2023)', 'Ilwani\n(2023)', 
               'Wang\n(2024)', 'Bhattacharya\n(2023)', 'MPCIM\n(This Study)']
    auc_scores = [0.84, 0.87, 0.82, 0.78, 0.85, 0.81, 0.901]
    colors = ['#4472C4', '#4472C4', '#4472C4', '#4472C4', '#4472C4', '#4472C4', '#ED7D31']
    
    bars1 = ax1.bar(studies, auc_scores, color=colors, edgecolor='black', linewidth=1)
    ax1.axhline(y=0.901, color='#ED7D31', linestyle='--', alpha=0.7, label='MPCIM Performance')
    
    # Add value labels
    for bar, score in zip(bars1, auc_scores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{score:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax1.set_ylabel('AUC-ROC Score', fontsize=11, fontweight='bold')
    ax1.set_title('AUC-ROC Performance Comparison', fontsize=12, fontweight='bold')
    ax1.set_ylim(0.7, 1.0)
    ax1.tick_params(axis='x', rotation=0)
    
    # Add improvement annotation
    ax1.annotate('24.6%\nimprovement', xy=(6, 0.901), xytext=(5, 0.95),
                fontsize=10, ha='center', fontweight='bold', color='#ED7D31',
                arrowprops=dict(arrowstyle='->', color='#ED7D31'))
    
    # Chart 2: Feature Categories
    ax2 = axes[1]
    categories = ['Single-dim\n(Performance)', 'Dual-dim\n(Perf+Demog)', 'Multi-dim\n(3+ dimensions)', 
                  'With XAI', 'With AI\nNarratives']
    existing_lit = [12, 2, 0, 2, 0]
    mpcim = [0, 0, 1, 1, 1]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars2 = ax2.bar(x - width/2, existing_lit, width, label='Existing Literature (n=14)', 
                    color='#4472C4', edgecolor='black')
    bars3 = ax2.bar(x + width/2, mpcim, width, label='MPCIM (This Study)', 
                    color='#ED7D31', edgecolor='black')
    
    ax2.set_ylabel('Number of Studies', fontsize=11, fontweight='bold')
    ax2.set_title('Research Approach Distribution', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, fontsize=9)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_ylim(0, 15)
    
    # Add value labels
    for bar in bars2:
        if bar.get_height() > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9)
    for bar in bars3:
        if bar.get_height() > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9, color='#ED7D31')
    
    plt.suptitle('Systematic Literature Review: Comparison with Existing Studies', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_literature_comparison.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(output_dir, '03_literature_comparison.pdf'), bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Literature Comparison Chart saved")


def create_gap_analysis_table():
    """Create visual gap analysis table"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')
    
    # Table data
    gaps = [
        ['G1', 'Single-dimension approach dominates', '85% use performance-only', '✓ 3-dimensional integration', 'Addressed'],
        ['G2', 'Psychological assessment not integrated', '0% systematic integration', '✓ 9 psychological features', 'Addressed'],
        ['G3', 'Limited explainability in promotion', '14% implement any XAI', '✓ SHAP + AI narratives', 'Addressed'],
        ['G4', 'No AI-generated narratives for HR', '0% use natural language', '✓ Gemini/OpenAI integration', 'Addressed'],
        ['G5', 'Lack of production-ready tools', 'Mostly prototypes', '✓ 6-page Streamlit dashboard', 'Addressed'],
        ['G6', 'Knowledge graph not utilized', 'Emerging research', '✓ Interactive KG visualization', 'Addressed'],
    ]
    
    # Create table
    table = ax.table(
        cellText=gaps,
        colLabels=['Gap ID', 'Research Gap', 'Literature Status', 'MPCIM Contribution', 'Status'],
        loc='center',
        cellLoc='center',
        colWidths=[0.08, 0.28, 0.22, 0.28, 0.1]
    )
    
    # Style table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2)
    
    # Header styling
    for i in range(5):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(color='white', fontweight='bold')
    
    # Row styling
    for row in range(1, 7):
        table[(row, 0)].set_facecolor('#E6F2FF')
        table[(row, 0)].set_text_props(fontweight='bold')
        table[(row, 3)].set_facecolor('#E6FFE6')
        table[(row, 3)].set_text_props(color='#006600')
        table[(row, 4)].set_facecolor('#90EE90')
        table[(row, 4)].set_text_props(fontweight='bold', color='#006600')
    
    ax.set_title('Research Gap Analysis: MPCIM Contributions to Literature', 
                 fontsize=14, fontweight='bold', pad=20, y=0.95)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_gap_analysis_table.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(output_dir, '04_gap_analysis_table.pdf'), bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Gap Analysis Table saved")


def create_timeline_chart():
    """Create timeline of relevant publications"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Data
    papers = [
        (2020, 'Fallucchi et al.', 'ML for Attrition', '#4472C4'),
        (2021, 'Liu', 'Psychology + Competence', '#70AD47'),
        (2021, 'Pradipta et al.', 'SMOTE Review', '#9966FF'),
        (2022, 'Alqahtani & Almaleh', 'Promotion Prediction', '#4472C4'),
        (2022, 'Zhang & Yuan', 'Multi-dim Competency', '#70AD47'),
        (2022, 'Aljbour et al.', 'TM Framework (SLR)', '#70AD47'),
        (2022, 'Das et al.', 'XAI Attrition', '#FFC000'),
        (2022, 'Kavzoglu & Teke', 'RF vs XGBoost', '#9966FF'),
        (2022, 'Konstantinidis et al.', 'KG Talent Matching', '#C00000'),
        (2023, 'Jafor et al.', 'AdaBoost Promotion', '#4472C4'),
        (2023, 'Shafie et al.', 'Hybrid Sampling', '#4472C4'),
        (2023, 'Ilwani & Nassreddine', 'XGBoost Promotion', '#4472C4'),
        (2023, 'Bhattacharya et al.', 'XAI Promotion', '#FFC000'),
        (2023, 'Marín Díaz et al.', 'SHAP HR', '#FFC000'),
        (2023, 'Yang et al.', 'KG Course Rec', '#C00000'),
        (2023, 'Wongvorachan et al.', 'SMOTE Comparison', '#9966FF'),
        (2024, 'Wang et al.', 'Ensemble Promotion', '#4472C4'),
        (2024, 'Al Akasheh et al.', 'KG + XAI Turnover', '#C00000'),
        (2025, 'Qin et al.', 'AI Talent Survey', '#C00000'),
        (2025, 'MPCIM (This Study)', 'Multi-dim + XAI + KG', '#ED7D31'),
    ]
    
    # Create timeline
    years = [p[0] for p in papers]
    y_positions = list(range(len(papers)))
    
    # Color by category
    for i, (year, author, topic, color) in enumerate(papers):
        ax.barh(i, 0.8, left=year-0.4, color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.text(year, i, f'{author}', fontsize=8, ha='center', va='center', fontweight='bold')
        ax.text(year + 0.6, i, f'{topic}', fontsize=8, ha='left', va='center')
    
    # Highlight MPCIM
    ax.barh(len(papers)-1, 0.8, left=2024.6, color='#ED7D31', alpha=1, edgecolor='black', linewidth=2)
    
    # Settings
    ax.set_xlim(2019.5, 2026)
    ax.set_ylim(-0.5, len(papers)-0.5)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_title('Timeline of Relevant Publications (2020-2025)', fontsize=14, fontweight='bold')
    ax.set_yticks([])
    
    # Legend
    legend_elements = [
        mpatches.Patch(color='#4472C4', alpha=0.7, label='Promotion Prediction'),
        mpatches.Patch(color='#70AD47', alpha=0.7, label='Multi-dimensional Assessment'),
        mpatches.Patch(color='#FFC000', alpha=0.7, label='Explainable AI'),
        mpatches.Patch(color='#9966FF', alpha=0.7, label='ML Methods'),
        mpatches.Patch(color='#C00000', alpha=0.7, label='Knowledge Graph'),
        mpatches.Patch(color='#ED7D31', label='MPCIM (This Study)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_publication_timeline.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(output_dir, '05_publication_timeline.pdf'), bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Publication Timeline saved")


def create_contribution_summary():
    """Create visual summary of MPCIM contributions"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(6, 9.5, 'MPCIM Framework: Key Contributions', fontsize=16, fontweight='bold',
            ha='center', va='center')
    ax.text(6, 9, 'Addressing Research Gaps in Employee Promotion Prediction', fontsize=12,
            ha='center', va='center', style='italic')
    
    # Main contributions (hexagons)
    contributions = [
        (3, 7, 'Multi-dimensional\nAssessment', '3 Dimensions:\nPerformance\nBehavioral\nPsychological', '#4472C4'),
        (9, 7, 'Explainable AI', 'SHAP Analysis\n+ AI Narratives\n(Gemini/OpenAI)', '#70AD47'),
        (3, 4, 'Feature\nEngineering', '34 Features:\n9 Psychological\n8 Engineered\n7 Encoded', '#FFC000'),
        (9, 4, 'Production\nDashboard', '6-Page Streamlit\nInteractive UI\nReal-time Prediction', '#9966FF'),
        (6, 2, 'Knowledge\nGraph', '45 Skills\nEmployee-Skill-Job\nRelationships', '#C00000'),
    ]
    
    for x, y, title, desc, color in contributions:
        # Circle
        circle = plt.Circle((x, y), 1.3, facecolor=color, alpha=0.3, edgecolor=color, linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y+0.4, title, fontsize=11, fontweight='bold', ha='center', va='center')
        ax.text(x, y-0.4, desc, fontsize=8, ha='center', va='center')
    
    # Center result
    center_circle = plt.Circle((6, 5.5), 1.5, facecolor='#ED7D31', alpha=0.4, 
                                edgecolor='#ED7D31', linewidth=3)
    ax.add_patch(center_circle)
    ax.text(6, 5.8, 'MPCIM', fontsize=14, fontweight='bold', ha='center', va='center', color='#ED7D31')
    ax.text(6, 5.2, 'AUC-ROC: 0.901\n(+24.6%)', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Connecting lines
    connections = [(3, 7), (9, 7), (3, 4), (9, 4), (6, 2)]
    for x, y in connections:
        ax.annotate('', xy=(6, 5.5), xytext=(x, y),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=1, alpha=0.5))
    
    # Bottom text
    ax.text(6, 0.5, 'First framework integrating multi-dimensional assessment with full explainability in promotion prediction',
            fontsize=10, ha='center', va='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF2E6', edgecolor='#ED7D31'))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_contribution_summary.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(output_dir, '06_contribution_summary.pdf'), bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Contribution Summary saved")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Generating SLR Diagrams for IEEE Paper")
    print("="*60 + "\n")
    
    create_prisma_diagram()
    create_research_gap_matrix()
    create_literature_comparison_chart()
    create_gap_analysis_table()
    create_timeline_chart()
    create_contribution_summary()
    
    print("\n" + "="*60)
    print(f"All diagrams saved to: {output_dir}")
    print("="*60)
    print("\nGenerated files:")
    print("  1. 01_prisma_flow_diagram.png/pdf")
    print("  2. 02_research_gap_matrix.png/pdf")
    print("  3. 03_literature_comparison.png/pdf")
    print("  4. 04_gap_analysis_table.png/pdf")
    print("  5. 05_publication_timeline.png/pdf")
    print("  6. 06_contribution_summary.png/pdf")
