"""
Generate MPCIM Framework Architecture Diagram
Creates a professional PNG diagram for the IEEE paper
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(12, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis('off')

# Color scheme
color_header = '#2C3E50'
color_layer = '#3498DB'
color_component = '#E8F4F8'
color_text = '#2C3E50'
color_arrow = '#7F8C8D'

# Title
title_box = FancyBboxPatch((1, 14.5), 8, 1, 
                           boxstyle="round,pad=0.1", 
                           edgecolor=color_header, 
                           facecolor=color_header, 
                           linewidth=2)
ax.add_patch(title_box)
ax.text(5, 15, 'MPCIM FRAMEWORK ARCHITECTURE', 
        ha='center', va='center', fontsize=18, fontweight='bold', color='white')

# Layer 1: INPUT
y_pos = 13
input_box = FancyBboxPatch((2, y_pos), 6, 0.8, 
                          boxstyle="round,pad=0.05", 
                          edgecolor=color_layer, 
                          facecolor=color_component, 
                          linewidth=2)
ax.add_patch(input_box)
ax.text(5, y_pos+0.4, 'INPUT LAYER', 
        ha='center', va='center', fontsize=12, fontweight='bold', color=color_text)

# Three input dimensions
y_pos = 11.5
box_width = 2.3
box_height = 1.2

# Performance Dimension
perf_box = FancyBboxPatch((1, y_pos), box_width, box_height, 
                         boxstyle="round,pad=0.05", 
                         edgecolor=color_layer, 
                         facecolor=color_component, 
                         linewidth=1.5)
ax.add_patch(perf_box)
ax.text(2.15, y_pos+0.9, 'Performance', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(2.15, y_pos+0.5, 'Dimension', ha='center', va='center', fontsize=9)
ax.text(2.15, y_pos+0.15, '• KPI scores\n• Ratings', ha='center', va='center', fontsize=7)

# Behavioral Dimension
behav_box = FancyBboxPatch((3.85, y_pos), box_width, box_height, 
                          boxstyle="round,pad=0.05", 
                          edgecolor=color_layer, 
                          facecolor=color_component, 
                          linewidth=1.5)
ax.add_patch(behav_box)
ax.text(5, y_pos+0.9, 'Behavioral', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(5, y_pos+0.5, 'Dimension', ha='center', va='center', fontsize=9)
ax.text(5, y_pos+0.15, '• Competencies\n• Values alignment', ha='center', va='center', fontsize=7)

# Psychological Dimension
psych_box = FancyBboxPatch((6.7, y_pos), box_width, box_height, 
                          boxstyle="round,pad=0.05", 
                          edgecolor=color_layer, 
                          facecolor=color_component, 
                          linewidth=1.5)
ax.add_patch(psych_box)
ax.text(7.85, y_pos+0.9, 'Psychological', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(7.85, y_pos+0.5, 'Dimension', ha='center', va='center', fontsize=9)
ax.text(7.85, y_pos+0.15, '• Quick Assessment\n• Leadership', ha='center', va='center', fontsize=7)

# Arrows from inputs to integration
for x_start in [2.15, 5, 7.85]:
    arrow = FancyArrowPatch((x_start, y_pos), (5, y_pos-0.8),
                           arrowstyle='->', mutation_scale=20, 
                           linewidth=1.5, color=color_arrow)
    ax.add_patch(arrow)

# Layer 2: INTEGRATION
y_pos = 9.5
integration_box = FancyBboxPatch((2.5, y_pos), 5, 1, 
                                boxstyle="round,pad=0.05", 
                                edgecolor=color_layer, 
                                facecolor=color_component, 
                                linewidth=2)
ax.add_patch(integration_box)
ax.text(5, y_pos+0.7, 'INTEGRATION LAYER', ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(5, y_pos+0.3, 'Feature Engineering (34 features)', ha='center', va='center', fontsize=9)

# Arrow to prediction
arrow = FancyArrowPatch((5, y_pos), (5, y_pos-0.8),
                       arrowstyle='->', mutation_scale=20, 
                       linewidth=2, color=color_arrow)
ax.add_patch(arrow)

# Layer 3: PREDICTION
y_pos = 7.5
prediction_box = FancyBboxPatch((2.5, y_pos), 5, 1, 
                               boxstyle="round,pad=0.05", 
                               edgecolor=color_layer, 
                               facecolor=color_component, 
                               linewidth=2)
ax.add_patch(prediction_box)
ax.text(5, y_pos+0.7, 'PREDICTION LAYER', ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(5, y_pos+0.3, 'ML Models (Random Forest, XGBoost, Neural Network)', ha='center', va='center', fontsize=9)

# Arrow to explainability
arrow = FancyArrowPatch((5, y_pos), (5, y_pos-0.8),
                       arrowstyle='->', mutation_scale=20, 
                       linewidth=2, color=color_arrow)
ax.add_patch(arrow)

# Layer 4: EXPLAINABILITY
y_pos = 5.5
explainability_box = FancyBboxPatch((2, y_pos), 6, 1.5, 
                                   boxstyle="round,pad=0.05", 
                                   edgecolor=color_layer, 
                                   facecolor=color_component, 
                                   linewidth=2)
ax.add_patch(explainability_box)
ax.text(5, y_pos+1.2, 'EXPLAINABILITY LAYER', ha='center', va='center', fontsize=11, fontweight='bold')

# Three explainability components
component_y = y_pos + 0.5
ax.text(3, component_y, '• SHAP Analysis\n  (Feature importance)', ha='left', va='center', fontsize=9)
ax.text(5, component_y, '• AI Narrative\n  (Gemini/GPT)', ha='center', va='center', fontsize=9)
ax.text(6.8, component_y, '• Knowledge Graph\n  (Skill gap)', ha='right', va='center', fontsize=9)

# Arrow to output
arrow = FancyArrowPatch((5, y_pos), (5, y_pos-0.8),
                       arrowstyle='->', mutation_scale=20, 
                       linewidth=2, color=color_arrow)
ax.add_patch(arrow)

# OUTPUT
y_pos = 3.5
output_box = FancyBboxPatch((2.5, y_pos), 5, 1.2, 
                           boxstyle="round,pad=0.1", 
                           edgecolor=color_layer, 
                           facecolor=color_component, 
                           linewidth=2)
ax.add_patch(output_box)
ax.text(5, y_pos+0.85, 'OUTPUT', ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(5, y_pos+0.4, 'Transparent Promotion Decision', ha='center', va='center', fontsize=10)

# Key metrics box
y_pos = 1.5
metrics_box = FancyBboxPatch((1.5, y_pos), 7, 1, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#27AE60', 
                            facecolor='#E8F8F5', 
                            linewidth=1.5, linestyle='--')
ax.add_patch(metrics_box)
ax.text(5, y_pos+0.7, 'Performance Metrics', ha='center', va='center', fontsize=10, fontweight='bold', color='#27AE60')
ax.text(5, y_pos+0.3, 'AUC-ROC: 0.901 | Accuracy: 87.4% | F1-Score: 0.500 | 24.6% improvement', 
        ha='center', va='center', fontsize=8)

# Footer
ax.text(5, 0.5, 'MPCIM: Multi-dimensional Performance-Career Integration Model', 
        ha='center', va='center', fontsize=9, style='italic', color=color_text)

# Add layer numbers on the left
layer_labels = [
    (13.4, '1'),
    (10, '2'),
    (8, '3'),
    (6.2, '4'),
]

for y, label in layer_labels:
    ax.text(0.5, y, label, ha='center', va='center', 
            fontsize=14, fontweight='bold', 
            bbox=dict(boxstyle='circle', facecolor=color_layer, edgecolor='none', alpha=0.7),
            color='white')

plt.tight_layout()

# Save the figure
output_dir = 'results'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'mpcim_framework_architecture.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ MPCIM Framework diagram saved to: {output_path}")
print(f"   Resolution: 300 DPI (publication quality)")
print(f"   File size: ~{os.path.getsize(output_path) / 1024:.1f} KB")

# Also save as high-res version for posters
output_path_hires = os.path.join(output_dir, 'mpcim_framework_architecture_hires.png')
plt.savefig(output_path_hires, dpi=600, bbox_inches='tight', facecolor='white')
print(f"✅ High-res version saved to: {output_path_hires}")
print(f"   Resolution: 600 DPI (poster quality)")

plt.close()
