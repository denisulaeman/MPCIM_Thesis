"""
Generate Clean PRISMA 2020 Flow Diagram
Author: Deni Sulaeman
Date: December 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import os

# Output directory
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results', 'slr_diagrams')
os.makedirs(output_dir, exist_ok=True)

# Set style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

def create_prisma_diagram():
    """Create PRISMA 2020 Flow Diagram - Clean Professional Design"""
    fig, ax = plt.subplots(figsize=(11, 13))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 13)
    ax.axis('off')
    
    # Colors
    c_blue = '#4472C4'
    c_green = '#70AD47'  
    c_yellow = '#FFC000'
    c_orange = '#ED7D31'
    c_red = '#C00000'
    c_gray = '#404040'
    
    def box(x, y, w, h, text, edge_color=c_gray, fill_color='white', 
            fontsize=9, bold=False, text_color='black', lw=1.5):
        """Draw a rounded box with text"""
        rect = FancyBboxPatch((x, y), w, h,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor=fill_color, edgecolor=edge_color, linewidth=lw)
        ax.add_patch(rect)
        weight = 'bold' if bold else 'normal'
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fontsize, fontweight=weight, color=text_color,
                wrap=True)
    
    def arrow_down(x, y1, y2):
        """Draw downward arrow"""
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(arrowstyle='-|>', color=c_gray, lw=1.5))
    
    def arrow_right(x1, x2, y):
        """Draw rightward arrow"""
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='-|>', color=c_red, lw=1.5))
    
    # ============ TITLE ============
    ax.text(5.5, 12.6, 'PRISMA 2020 Flow Diagram', fontsize=16, fontweight='bold',
            ha='center', va='center', color=c_gray)
    ax.text(5.5, 12.2, 'Systematic Review: ML for Employee Promotion Prediction', 
            fontsize=10, ha='center', va='center', color='#666666', style='italic')
    
    # ============ IDENTIFICATION ============
    # Section background
    id_bg = FancyBboxPatch((0.5, 9.8), 10, 2.2,
                           boxstyle="round,pad=0.02,rounding_size=0.15",
                           facecolor=c_blue, alpha=0.12, edgecolor=c_blue, linewidth=2)
    ax.add_patch(id_bg)
    
    # Section title inside box
    ax.text(5.5, 11.7, 'IDENTIFICATION', fontsize=12, fontweight='bold',
            ha='center', va='center', color=c_blue)
    
    # Database boxes - row
    dbs = [('IEEE Xplore\n(n=82)', 1.2), ('ScienceDirect\n(n=125)', 3.0), 
           ('ACM DL\n(n=58)', 4.8), ('Springer\n(n=98)', 6.6), ('Google Scholar\n(n=124)', 8.4)]
    for txt, x in dbs:
        box(x, 10.6, 1.6, 0.8, txt, edge_color=c_blue, fontsize=8)
    
    # Total identified
    box(2.5, 10.0, 6, 0.5, 'Records identified from databases (n = 487)',
        edge_color=c_blue, fill_color='#DCE6F1', fontsize=10, bold=True)
    
    arrow_down(5.5, 9.9, 9.2)
    
    # ============ SCREENING ============
    # Section background
    scr_bg = FancyBboxPatch((0.5, 6.8), 10, 2.2,
                            boxstyle="round,pad=0.02,rounding_size=0.15",
                            facecolor=c_green, alpha=0.12, edgecolor=c_green, linewidth=2)
    ax.add_patch(scr_bg)
    
    # Section title
    ax.text(5.5, 8.7, 'SCREENING', fontsize=12, fontweight='bold',
            ha='center', va='center', color=c_green)
    
    # Duplicates removed (top)
    box(1.3, 8.0, 3.8, 0.5, 'Duplicates removed (n = 145)',
        edge_color=c_green, fontsize=9)
    
    arrow_down(3.2, 7.9, 7.6)
    
    # Records screened
    box(1.3, 7.1, 3.8, 0.5, 'Records screened (n = 342)',
        edge_color=c_green, fill_color='#E2EFDA', fontsize=10, bold=True)
    
    # Arrow to excluded
    arrow_right(5.2, 6.0, 7.35)
    
    # Excluded records
    box(6.0, 7.1, 4.0, 0.5, 'Records excluded (n = 248)',
        edge_color=c_red, fill_color='#F8D7DA', fontsize=9, text_color=c_red)
    
    arrow_down(3.2, 7.0, 6.2)
    
    # ============ ELIGIBILITY ============
    # Section background
    elig_bg = FancyBboxPatch((0.5, 3.8), 10, 2.2,
                             boxstyle="round,pad=0.02,rounding_size=0.15",
                             facecolor=c_yellow, alpha=0.15, edgecolor=c_yellow, linewidth=2)
    ax.add_patch(elig_bg)
    
    # Section title
    ax.text(5.5, 5.7, 'ELIGIBILITY', fontsize=12, fontweight='bold',
            ha='center', va='center', color='#B8860B')
    
    # Full-text assessed
    box(1.3, 4.6, 3.8, 0.7, 'Full-text articles assessed\nfor eligibility (n = 94)',
        edge_color=c_yellow, fill_color='#FFF2CC', fontsize=10, bold=True)
    
    # Arrow to excluded
    arrow_right(5.2, 6.0, 4.95)
    
    # Full-text excluded with reasons
    excl_box = FancyBboxPatch((6.0, 4.0), 4.0, 1.5,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor='#F8D7DA', edgecolor=c_red, linewidth=1.5)
    ax.add_patch(excl_box)
    ax.text(8.0, 5.15, 'Full-text excluded (n = 56)', fontsize=9, fontweight='bold',
            ha='center', va='center', color=c_red)
    ax.text(8.0, 4.75, '• Not empirical study (n=18)', fontsize=8,
            ha='center', va='center', color='#800000')
    ax.text(8.0, 4.45, '• No ML methods (n=22)', fontsize=8,
            ha='center', va='center', color='#800000')
    ax.text(8.0, 4.15, '• Low quality score (n=16)', fontsize=8,
            ha='center', va='center', color='#800000')
    
    arrow_down(3.2, 4.5, 3.4)
    
    # ============ INCLUDED ============
    # Section background
    inc_bg = FancyBboxPatch((0.5, 0.4), 10, 2.8,
                            boxstyle="round,pad=0.02,rounding_size=0.15",
                            facecolor=c_orange, alpha=0.12, edgecolor=c_orange, linewidth=2)
    ax.add_patch(inc_bg)
    
    # Section title
    ax.text(5.5, 2.9, 'INCLUDED', fontsize=12, fontweight='bold',
            ha='center', va='center', color=c_orange)
    
    # Studies included
    box(1.5, 1.9, 8, 0.6, 'Studies included in systematic review (n = 38)',
        edge_color=c_orange, fill_color='#FCE4D6', fontsize=11, bold=True)
    
    arrow_down(5.5, 1.8, 1.5)
    
    # Category boxes
    cats = [
        ('Promotion\nPrediction ML\n(n=14)', 1.2, c_blue),
        ('Multi-dim\nAssessment\n(n=10)', 3.4, c_green),
        ('Explainable\nAI for HR\n(n=9)', 5.6, '#B8860B'),
        ('Knowledge\nGraph\n(n=5)', 7.8, '#7030A0')
    ]
    for txt, x, color in cats:
        box(x, 0.55, 2.0, 0.9, txt, edge_color=color, fontsize=8, bold=True, text_color=color)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_prisma_flow_diagram.png'), dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.savefig(os.path.join(output_dir, '01_prisma_flow_diagram.pdf'), 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ PRISMA Flow Diagram saved")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Generating Clean PRISMA Diagram")
    print("="*50 + "\n")
    create_prisma_diagram()
    print(f"\nSaved to: {output_dir}")
