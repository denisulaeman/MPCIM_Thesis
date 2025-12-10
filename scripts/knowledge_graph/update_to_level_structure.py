"""
Update All References from Job Position to Job Level
=====================================================
This script updates all files to use the new level-based structure
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re

print("=" * 80)
print("UPDATING TO LEVEL-BASED STRUCTURE")
print("=" * 80)
print()

repo_root = Path(__file__).resolve().parents[2]

# ============================================================================
# 1. UPDATE EMPLOYEE DATASET - ADD CURRENT_LEVEL COLUMN
# ============================================================================

print("1. Updating Employee Dataset...")

# Load main dataset
dataset_path = repo_root / "data" / "final" / "sample_dataset_1000_balanced.csv"
df = pd.read_csv(dataset_path)

print(f"   ✓ Loaded {len(df)} employees")

# Add current_level column based on performance, tenure, and leadership
def assign_level(row):
    """Assign level based on employee metrics"""
    perf = row['performance_score']
    tenure = row['tenure_years']
    leadership = row['leadership_potential']
    has_promo = row['has_promotion']
    
    # Direktur level (top performers with long tenure)
    if perf >= 95 and tenure >= 10 and leadership >= 90:
        return "Direktur"
    
    # Senior Manager level
    elif perf >= 90 and tenure >= 8 and leadership >= 82:
        return "Senior Manager"
    
    # Manager level
    elif perf >= 85 and tenure >= 5 and leadership >= 75:
        return "Manager"
    
    # Senior Officer level
    elif perf >= 75 and tenure >= 3 and leadership >= 65:
        return "Senior Officer"
    
    # Officer level
    elif perf >= 65 and tenure >= 1 and leadership >= 55:
        return "Officer"
    
    # Non Staff (entry level)
    else:
        return "Non Staff"

df['current_level'] = df.apply(assign_level, axis=1)

# Save updated dataset
df.to_csv(dataset_path, index=False)

print(f"   ✓ Added 'current_level' column")
print(f"   ✓ Level distribution:")

level_counts = df['current_level'].value_counts().sort_index()
for level, count in level_counts.items():
    print(f"      - {level}: {count} employees")

print(f"   ✓ Saved to: {dataset_path}")
print()

# ============================================================================
# 2. UPDATE TEMPLATE FILES
# ============================================================================

print("2. Updating Template Files...")

# Update TEMPLATE_EMPLOYEE_DATA.csv
template_path = repo_root / "templates" / "TEMPLATE_EMPLOYEE_DATA.csv"

if template_path.exists():
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Replace current_position with current_level
    content = content.replace('current_position', 'current_level')
    
    # Update example values
    content = content.replace(',Staff\n', ',Officer\n')
    content = content.replace(',Manager\n', ',Manager\n')
    content = content.replace(',Supervisor\n', ',Senior Officer\n')
    
    with open(template_path, 'w') as f:
        f.write(content)
    
    print(f"   ✓ Updated: {template_path}")

print()

# ============================================================================
# 3. CREATE LEVEL MAPPING REFERENCE
# ============================================================================

print("3. Creating Level Mapping Reference...")

level_mapping = {
    "Non Staff": {
        "order": 1,
        "min_tenure": 0,
        "max_tenure": 2,
        "min_performance": 50,
        "min_behavior": 50,
        "min_psychological": 50,
        "min_leadership": 40,
        "description": "Entry level - learning phase"
    },
    "Officer": {
        "order": 2,
        "min_tenure": 1,
        "max_tenure": 4,
        "min_performance": 65,
        "min_behavior": 65,
        "min_psychological": 60,
        "min_leadership": 55,
        "description": "Independent contributor"
    },
    "Senior Officer": {
        "order": 3,
        "min_tenure": 3,
        "max_tenure": 7,
        "min_performance": 75,
        "min_behavior": 75,
        "min_psychological": 70,
        "min_leadership": 65,
        "description": "Senior level with mentoring"
    },
    "Manager": {
        "order": 4,
        "min_tenure": 5,
        "max_tenure": 10,
        "min_performance": 85,
        "min_behavior": 82,
        "min_psychological": 78,
        "min_leadership": 75,
        "description": "Team leadership & management"
    },
    "Senior Manager": {
        "order": 5,
        "min_tenure": 8,
        "max_tenure": 15,
        "min_performance": 90,
        "min_behavior": 88,
        "min_psychological": 85,
        "min_leadership": 82,
        "description": "Strategic management"
    },
    "Direktur": {
        "order": 6,
        "min_tenure": 10,
        "max_tenure": 25,
        "min_performance": 95,
        "min_behavior": 92,
        "min_psychological": 90,
        "min_leadership": 90,
        "description": "Executive leadership"
    }
}

# Save as JSON for reference
import json
mapping_path = repo_root / "data" / "knowledge_graph" / "level_mapping.json"
with open(mapping_path, 'w') as f:
    json.dump(level_mapping, f, indent=2)

print(f"   ✓ Created level mapping reference")
print(f"   ✓ Saved to: {mapping_path}")
print()

# ============================================================================
# 4. UPDATE DOCUMENTATION
# ============================================================================

print("4. Updating Documentation...")

# Files to update
doc_files = [
    repo_root / "README.md",
    repo_root / "THESIS_PROPOSAL.md",
    repo_root / "IMPLEMENTATION_COMPLETE.md",
]

replacements = [
    ("job position", "job level"),
    ("Job Position", "Job Level"),
    ("JOB POSITION", "JOB LEVEL"),
    ("current_position", "current_level"),
    ("Junior Staff", "Non Staff"),
    ("Staff →", "Officer →"),
    ("Senior Staff", "Senior Officer"),
]

for doc_path in doc_files:
    if doc_path.exists():
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for old, new in replacements:
                content = content.replace(old, new)
            
            if content != original_content:
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✓ Updated: {doc_path.name}")
        except Exception as e:
            print(f"   ⚠️ Could not update {doc_path.name}: {e}")

print()

# ============================================================================
# 5. SUMMARY
# ============================================================================

print("=" * 80)
print("✅ UPDATE COMPLETE!")
print("=" * 80)
print()

print("Summary of Changes:")
print(f"  ✓ Employee dataset updated with 'current_level' column")
print(f"  ✓ Level distribution:")
for level, count in level_counts.items():
    print(f"      - {level}: {count} employees")
print()
print(f"  ✓ Template files updated")
print(f"  ✓ Level mapping reference created")
print(f"  ✓ Documentation updated")
print()

print("Level Structure (6 Levels):")
for level, info in level_mapping.items():
    print(f"  {info['order']}. {level}")
    print(f"     - Tenure: {info['min_tenure']}-{info['max_tenure']} years")
    print(f"     - Performance: {info['min_performance']}+")
    print(f"     - Leadership: {info['min_leadership']}+")
    print(f"     - {info['description']}")
print()

print("Next Steps:")
print("  1. Rebuild Knowledge Graph:")
print("     python scripts/knowledge_graph/build_graph.py")
print()
print("  2. Run tests:")
print("     python scripts/testing/test_knowledge_graph.py")
print()
print("  3. Launch app:")
print("     streamlit run app/Home.py")
print()

print("All references to 'job position' have been replaced with 'job level'!")
