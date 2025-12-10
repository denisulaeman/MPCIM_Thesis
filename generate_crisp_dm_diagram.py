"""
Generate CRISP-DM Framework Adaptation Diagram
Circular layout with Data at center (similar to standard CRISP-DM visualization)
Customized for MPCIM Employee Promotion Prediction Research
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import os
import numpy as np

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.axis('off')

# Color scheme - matching reference image
color_circle_bg = '#D6E4F0'
color_phase_box = '#5B9BD5'
color_text = 'white'
color_arrow = '#2C3E50'
color_data = '#FFD700'  # Gold for data cylinder
color_cloud = '#4DA6FF'  # Blue for cloud

# Large circular background
background_circle = Circle((0, 0), 5.5, 
                          facecolor=color_circle_bg, 
                          edgecolor='#2C3E50', 
                          linewidth=2,
                          alpha=0.3)
ax.add_patch(background_circle)

# Center - Data cylinder and cloud
center_x, center_y = 0, 0

# Draw data cylinder (3D effect)
cylinder_width = 1.2
cylinder_height = 1.5

# Cylinder body (yellow)
cylinder_body = Rectangle((center_x - cylinder_width/2, center_y - cylinder_height/2), 
                         cylinder_width, cylinder_height,
                         facecolor=color_data, 
                         edgecolor='#2C3E50', 
                         linewidth=2)
ax.add_patch(cylinder_body)

# Top ellipse
from matplotlib.patches import Ellipse
cylinder_top = Ellipse((center_x, center_y + cylinder_height/2), 
                       cylinder_width, 0.3,
                       facecolor=color_data, 
                       edgecolor='#2C3E50', 
                       linewidth=2)
ax.add_patch(cylinder_top)

# Horizontal lines on cylinder
for i in range(3):
    y_line = center_y - cylinder_height/2 + (i + 1) * cylinder_height/4
    ax.plot([center_x - cylinder_width/2, center_x + cylinder_width/2], 
           [y_line, y_line], 
           color='#2C3E50', linewidth=1.5)

ax.text(center_x, center_y, 'Data', 
        ha='center', va='center', fontsize=11, fontweight='bold', color='#2C3E50')

# Cloud below cylinder
cloud_x = center_x
cloud_y = center_y - 1.2

# Cloud made of circles
cloud_circles = [
    (cloud_x - 0.3, cloud_y, 0.35),
    (cloud_x + 0.3, cloud_y, 0.35),
    (cloud_x, cloud_y + 0.2, 0.4),
    (cloud_x - 0.5, cloud_y - 0.1, 0.25),
    (cloud_x + 0.5, cloud_y - 0.1, 0.25),
]

for cx, cy, radius in cloud_circles:
    cloud_circle = Circle((cx, cy), radius, 
                         facecolor=color_cloud, 
                         edgecolor='none', 
                         alpha=0.8)
    ax.add_patch(cloud_circle)

# Define positions for 6 phases in circular arrangement (evenly spaced)
radius = 4.0
phases_data = [
    ('Business\nUnderstanding', 90),
    ('Data\nUnderstanding', 30),
    ('Data\nPreparation', 330),
    ('Modeling', 270),
    ('Evaluation', 210),
    ('Deployment', 150),
]

# Draw phases
phase_positions = {}
for i, (name, angle) in enumerate(phases_data):
    angle_rad = np.radians(angle)
    x = center_x + radius * np.cos(angle_rad)
    y = center_y + radius * np.sin(angle_rad)
    
    # Phase box (rounded rectangle) - consistent size
    box_width = 1.9
    box_height = 0.75
    phase_box = FancyBboxPatch((x - box_width/2, y - box_height/2), 
                              box_width, box_height,
                              boxstyle="round,pad=0.1", 
                              edgecolor='#34495E', 
                              facecolor=color_phase_box, 
                              linewidth=1.5)
    ax.add_patch(phase_box)
    
    # Phase name (white text, bold)
    ax.text(x, y, name, 
            ha='center', va='center', fontsize=11, fontweight='bold', color=color_text)
    
    phase_positions[i] = (x, y, angle)

# Draw main cycle arrows (clockwise: BU -> DU -> DP -> M -> E -> D -> BU)
cycle_order = [0, 1, 2, 3, 4, 5]
for i in range(len(cycle_order)):
    start_idx = cycle_order[i]
    end_idx = cycle_order[(i + 1) % len(cycle_order)]
    
    start_x, start_y, start_angle = phase_positions[start_idx]
    end_x, end_y, end_angle = phase_positions[end_idx]
    
    # Calculate arrow start and end points on the outer edge of circle
    # Place arrows on the circular path between phases
    mid_angle = (start_angle + end_angle) / 2
    if start_angle == 90 and end_angle == 30:  # BU to DU
        mid_angle = 60
    elif start_angle == 30 and end_angle == 330:  # DU to DP
        mid_angle = 0
    elif start_angle == 330 and end_angle == 270:  # DP to M
        mid_angle = 300
    elif start_angle == 270 and end_angle == 210:  # M to E
        mid_angle = 240
    elif start_angle == 210 and end_angle == 150:  # E to D
        mid_angle = 180
    elif start_angle == 150 and end_angle == 90:  # D to BU
        mid_angle = 120
    
    # Arrow on outer circle
    arrow_radius = 4.8
    mid_rad = np.radians(mid_angle)
    arrow_x = center_x + arrow_radius * np.cos(mid_rad)
    arrow_y = center_y + arrow_radius * np.sin(mid_rad)
    
    # Direction perpendicular to radius (tangent to circle)
    arrow_angle = mid_angle - 90  # Tangent direction (clockwise)
    arrow_dx = 0.3 * np.cos(np.radians(arrow_angle))
    arrow_dy = 0.3 * np.sin(np.radians(arrow_angle))
    
    # Draw arrow
    arrow = FancyArrowPatch((arrow_x - arrow_dx, arrow_y - arrow_dy), 
                           (arrow_x + arrow_dx, arrow_y + arrow_dy),
                           arrowstyle='->', 
                           mutation_scale=30, 
                           linewidth=3, 
                           color=color_arrow)
    ax.add_patch(arrow)

# Draw bidirectional arrows between specific phases
# Business Understanding <-> Data Understanding
bu_x, bu_y, _ = phase_positions[0]
du_x, du_y, _ = phase_positions[1]
arrow1 = FancyArrowPatch((bu_x + 0.7, bu_y - 0.3), (du_x - 0.7, du_y + 0.3),
                        arrowstyle='<->', 
                        mutation_scale=22, 
                        linewidth=2.5, 
                        color=color_arrow)
ax.add_patch(arrow1)

# Data Preparation <-> Modeling
dp_x, dp_y, _ = phase_positions[2]
mod_x, mod_y, _ = phase_positions[3]
arrow2 = FancyArrowPatch((dp_x - 0.3, dp_y - 0.4), (mod_x + 0.3, mod_y + 0.4),
                        arrowstyle='<->', 
                        mutation_scale=22, 
                        linewidth=2.5, 
                        color=color_arrow)
ax.add_patch(arrow2)

# Footer
ax.text(0, -5.8, 'CRISP-DM Framework Adapted for MPCIM Research', 
        ha='center', va='center', fontsize=10, fontweight='bold', color=color_arrow)

plt.tight_layout()

# Save the figure
output_dir = 'results'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'crisp_dm_adaptation.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ CRISP-DM Adaptation diagram saved to: {output_path}")
print(f"   Resolution: 300 DPI (publication quality)")
print(f"   File size: ~{os.path.getsize(output_path) / 1024:.1f} KB")

# Also save high-res version
output_path_hires = os.path.join(output_dir, 'crisp_dm_adaptation_hires.png')
plt.savefig(output_path_hires, dpi=600, bbox_inches='tight', facecolor='white')
print(f"✅ High-res version saved to: {output_path_hires}")

plt.close()
