"""
Create Sample Data for Knowledge Graph - BY LEVEL
==================================================
Generate positions by level structure for MPCIM Knowledge Graph
New Structure: Non Staff, Officer, Senior Officer, Manager, Senior Manager, Direktur
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 80)
print("CREATING SAMPLE DATA FOR KNOWLEDGE GRAPH - BY LEVEL")
print("=" * 80)
print()

# Setup paths
repo_root = Path(__file__).resolve().parents[2]
kg_data_dir = repo_root / "data" / "knowledge_graph"
kg_data_dir.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. JOB POSITIONS - BY LEVEL STRUCTURE
# ============================================================================

print("1. Creating Job Positions by Level...")

# New level structure
jobs = [
    # NON STAFF LEVEL
    {
        "job_id": "L001",
        "job_title": "Non Staff",
        "department": "IT",
        "level": "Non Staff",
        "min_performance": 50,
        "min_behavior": 50,
        "min_psychological": 50,
        "min_leadership": 40,
        "min_tenure": 0,
        "max_tenure": 2
    },
    {
        "job_id": "L002",
        "job_title": "Non Staff",
        "department": "HR",
        "level": "Non Staff",
        "min_performance": 50,
        "min_behavior": 55,
        "min_psychological": 50,
        "min_leadership": 40,
        "min_tenure": 0,
        "max_tenure": 2
    },
    {
        "job_id": "L003",
        "job_title": "Non Staff",
        "department": "Finance",
        "level": "Non Staff",
        "min_performance": 50,
        "min_behavior": 50,
        "min_psychological": 50,
        "min_leadership": 40,
        "min_tenure": 0,
        "max_tenure": 2
    },
    
    # OFFICER LEVEL
    {
        "job_id": "L004",
        "job_title": "Officer",
        "department": "IT",
        "level": "Officer",
        "min_performance": 65,
        "min_behavior": 65,
        "min_psychological": 60,
        "min_leadership": 55,
        "min_tenure": 1,
        "max_tenure": 4
    },
    {
        "job_id": "L005",
        "job_title": "Officer",
        "department": "HR",
        "level": "Officer",
        "min_performance": 65,
        "min_behavior": 70,
        "min_psychological": 60,
        "min_leadership": 55,
        "min_tenure": 1,
        "max_tenure": 4
    },
    {
        "job_id": "L006",
        "job_title": "Officer",
        "department": "Finance",
        "level": "Officer",
        "min_performance": 70,
        "min_behavior": 65,
        "min_psychological": 60,
        "min_leadership": 55,
        "min_tenure": 1,
        "max_tenure": 4
    },
    {
        "job_id": "L007",
        "job_title": "Officer",
        "department": "Operations",
        "level": "Officer",
        "min_performance": 65,
        "min_behavior": 68,
        "min_psychological": 60,
        "min_leadership": 55,
        "min_tenure": 1,
        "max_tenure": 4
    },
    
    # SENIOR OFFICER LEVEL
    {
        "job_id": "L008",
        "job_title": "Senior Officer",
        "department": "IT",
        "level": "Senior Officer",
        "min_performance": 75,
        "min_behavior": 75,
        "min_psychological": 70,
        "min_leadership": 65,
        "min_tenure": 3,
        "max_tenure": 7
    },
    {
        "job_id": "L009",
        "job_title": "Senior Officer",
        "department": "HR",
        "level": "Senior Officer",
        "min_performance": 75,
        "min_behavior": 78,
        "min_psychological": 70,
        "min_leadership": 65,
        "min_tenure": 3,
        "max_tenure": 7
    },
    {
        "job_id": "L010",
        "job_title": "Senior Officer",
        "department": "Finance",
        "level": "Senior Officer",
        "min_performance": 78,
        "min_behavior": 75,
        "min_psychological": 70,
        "min_leadership": 65,
        "min_tenure": 3,
        "max_tenure": 7
    },
    {
        "job_id": "L011",
        "job_title": "Senior Officer",
        "department": "Operations",
        "level": "Senior Officer",
        "min_performance": 75,
        "min_behavior": 77,
        "min_psychological": 70,
        "min_leadership": 65,
        "min_tenure": 3,
        "max_tenure": 7
    },
    
    # MANAGER LEVEL
    {
        "job_id": "L012",
        "job_title": "Manager",
        "department": "IT",
        "level": "Manager",
        "min_performance": 85,
        "min_behavior": 82,
        "min_psychological": 78,
        "min_leadership": 75,
        "min_tenure": 5,
        "max_tenure": 10
    },
    {
        "job_id": "L013",
        "job_title": "Manager",
        "department": "HR",
        "level": "Manager",
        "min_performance": 85,
        "min_behavior": 85,
        "min_psychological": 78,
        "min_leadership": 75,
        "min_tenure": 5,
        "max_tenure": 10
    },
    {
        "job_id": "L014",
        "job_title": "Manager",
        "department": "Finance",
        "level": "Manager",
        "min_performance": 88,
        "min_behavior": 82,
        "min_psychological": 78,
        "min_leadership": 75,
        "min_tenure": 5,
        "max_tenure": 10
    },
    {
        "job_id": "L015",
        "job_title": "Manager",
        "department": "Operations",
        "level": "Manager",
        "min_performance": 85,
        "min_behavior": 83,
        "min_psychological": 78,
        "min_leadership": 75,
        "min_tenure": 5,
        "max_tenure": 10
    },
    
    # SENIOR MANAGER LEVEL
    {
        "job_id": "L016",
        "job_title": "Senior Manager",
        "department": "IT",
        "level": "Senior Manager",
        "min_performance": 90,
        "min_behavior": 88,
        "min_psychological": 85,
        "min_leadership": 82,
        "min_tenure": 8,
        "max_tenure": 15
    },
    {
        "job_id": "L017",
        "job_title": "Senior Manager",
        "department": "HR",
        "level": "Senior Manager",
        "min_performance": 90,
        "min_behavior": 90,
        "min_psychological": 85,
        "min_leadership": 82,
        "min_tenure": 8,
        "max_tenure": 15
    },
    {
        "job_id": "L018",
        "job_title": "Senior Manager",
        "department": "Finance",
        "level": "Senior Manager",
        "min_performance": 92,
        "min_behavior": 88,
        "min_psychological": 85,
        "min_leadership": 82,
        "min_tenure": 8,
        "max_tenure": 15
    },
    {
        "job_id": "L019",
        "job_title": "Senior Manager",
        "department": "Operations",
        "level": "Senior Manager",
        "min_performance": 90,
        "min_behavior": 89,
        "min_psychological": 85,
        "min_leadership": 82,
        "min_tenure": 8,
        "max_tenure": 15
    },
    
    # DIREKTUR LEVEL
    {
        "job_id": "L020",
        "job_title": "Direktur",
        "department": "IT",
        "level": "Direktur",
        "min_performance": 95,
        "min_behavior": 92,
        "min_psychological": 90,
        "min_leadership": 90,
        "min_tenure": 10,
        "max_tenure": 25
    },
    {
        "job_id": "L021",
        "job_title": "Direktur",
        "department": "HR",
        "level": "Direktur",
        "min_performance": 95,
        "min_behavior": 95,
        "min_psychological": 90,
        "min_leadership": 90,
        "min_tenure": 10,
        "max_tenure": 25
    },
    {
        "job_id": "L022",
        "job_title": "Direktur",
        "department": "Finance",
        "level": "Direktur",
        "min_performance": 95,
        "min_behavior": 92,
        "min_psychological": 90,
        "min_leadership": 90,
        "min_tenure": 10,
        "max_tenure": 25
    },
    {
        "job_id": "L023",
        "job_title": "Direktur",
        "department": "Operations",
        "level": "Direktur",
        "min_performance": 95,
        "min_behavior": 93,
        "min_psychological": 90,
        "min_leadership": 90,
        "min_tenure": 10,
        "max_tenure": 25
    },
]

df_jobs = pd.DataFrame(jobs)
jobs_path = kg_data_dir / "jobs.csv"
df_jobs.to_csv(jobs_path, index=False)

print(f"   ✓ Created {len(jobs)} positions across 6 levels")
print(f"   ✓ Levels: Non Staff, Officer, Senior Officer, Manager, Senior Manager, Direktur")
print(f"   ✓ Saved to: {jobs_path}")
print()

# ============================================================================
# 2. SKILLS
# ============================================================================

print("2. Creating Skills...")

skills = []

# Technical Skills (20)
technical_skills = [
    ("S001", "Python Programming", "Technical", 5),
    ("S002", "Data Analysis", "Technical", 5),
    ("S003", "SQL Database", "Technical", 4),
    ("S004", "Machine Learning", "Technical", 4),
    ("S005", "Web Development", "Technical", 3),
    ("S006", "Cloud Computing", "Technical", 4),
    ("S007", "DevOps", "Technical", 3),
    ("S008", "Cybersecurity", "Technical", 4),
    ("S009", "Network Administration", "Technical", 3),
    ("S010", "System Design", "Technical", 4),
    ("S011", "API Development", "Technical", 3),
    ("S012", "Mobile Development", "Technical", 3),
    ("S013", "Data Visualization", "Technical", 3),
    ("S014", "Excel Advanced", "Technical", 4),
    ("S015", "ERP Systems", "Technical", 4),
    ("S016", "Business Intelligence", "Technical", 4),
    ("S017", "Statistical Analysis", "Technical", 4),
    ("S018", "Financial Modeling", "Technical", 5),
    ("S019", "Accounting Software", "Technical", 4),
    ("S020", "Process Automation", "Technical", 3),
]

for skill_id, name, category, importance in technical_skills:
    skills.append({
        "skill_id": skill_id,
        "skill_name": name,
        "category": category,
        "importance": importance
    })

# Soft Skills (15)
soft_skills = [
    ("S021", "Communication", "Soft", 5),
    ("S022", "Teamwork", "Soft", 5),
    ("S023", "Problem Solving", "Soft", 5),
    ("S024", "Critical Thinking", "Soft", 5),
    ("S025", "Time Management", "Soft", 4),
    ("S026", "Adaptability", "Soft", 4),
    ("S027", "Creativity", "Soft", 3),
    ("S028", "Emotional Intelligence", "Soft", 4),
    ("S029", "Conflict Resolution", "Soft", 4),
    ("S030", "Presentation Skills", "Soft", 4),
    ("S031", "Negotiation", "Soft", 4),
    ("S032", "Customer Service", "Soft", 3),
    ("S033", "Attention to Detail", "Soft", 4),
    ("S034", "Work Ethics", "Soft", 5),
    ("S035", "Stress Management", "Soft", 3),
]

for skill_id, name, category, importance in soft_skills:
    skills.append({
        "skill_id": skill_id,
        "skill_name": name,
        "category": category,
        "importance": importance
    })

# Leadership Skills (10)
leadership_skills = [
    ("S036", "Team Leadership", "Leadership", 5),
    ("S037", "Strategic Thinking", "Leadership", 5),
    ("S038", "Decision Making", "Leadership", 5),
    ("S039", "Change Management", "Leadership", 4),
    ("S040", "Mentoring & Coaching", "Leadership", 4),
    ("S041", "Project Management", "Leadership", 5),
    ("S042", "Budget Management", "Leadership", 4),
    ("S043", "Stakeholder Management", "Leadership", 5),
    ("S044", "Performance Management", "Leadership", 4),
    ("S045", "Vision Setting", "Leadership", 5),
]

for skill_id, name, category, importance in leadership_skills:
    skills.append({
        "skill_id": skill_id,
        "skill_name": name,
        "category": category,
        "importance": importance
    })

df_skills = pd.DataFrame(skills)
skills_path = kg_data_dir / "skills.csv"
df_skills.to_csv(skills_path, index=False)

print(f"   ✓ Created {len(skills)} skills")
print(f"   ✓ Technical: 20, Soft: 15, Leadership: 10")
print(f"   ✓ Saved to: {skills_path}")
print()

# ============================================================================
# 3. JOB-SKILL REQUIREMENTS
# ============================================================================

print("3. Creating Job-Skill Requirements...")

job_skill_reqs = []

# Define skill requirements per level
level_skill_mapping = {
    "Non Staff": {
        "technical": [("S001", 1), ("S003", 1), ("S014", 2)],
        "soft": [("S021", 2), ("S022", 2), ("S025", 2), ("S034", 3)],
        "leadership": []
    },
    "Officer": {
        "technical": [("S001", 2), ("S002", 2), ("S003", 2), ("S014", 3)],
        "soft": [("S021", 3), ("S022", 3), ("S023", 3), ("S025", 3), ("S034", 4)],
        "leadership": []
    },
    "Senior Officer": {
        "technical": [("S001", 3), ("S002", 3), ("S003", 3), ("S014", 4), ("S016", 3)],
        "soft": [("S021", 4), ("S022", 4), ("S023", 4), ("S024", 3), ("S025", 4), ("S034", 4)],
        "leadership": [("S036", 2), ("S041", 2)]
    },
    "Manager": {
        "technical": [("S002", 4), ("S016", 4)],
        "soft": [("S021", 5), ("S022", 4), ("S023", 5), ("S024", 4), ("S028", 4), ("S034", 5)],
        "leadership": [("S036", 4), ("S037", 4), ("S038", 4), ("S041", 4), ("S043", 4)]
    },
    "Senior Manager": {
        "technical": [("S016", 4)],
        "soft": [("S021", 5), ("S023", 5), ("S024", 5), ("S028", 5), ("S034", 5)],
        "leadership": [("S036", 5), ("S037", 5), ("S038", 5), ("S039", 4), ("S041", 5), ("S043", 5), ("S044", 4)]
    },
    "Direktur": {
        "technical": [],
        "soft": [("S021", 5), ("S023", 5), ("S024", 5), ("S028", 5), ("S031", 5), ("S034", 5)],
        "leadership": [("S036", 5), ("S037", 5), ("S038", 5), ("S039", 5), ("S040", 5), ("S041", 5), ("S043", 5), ("S044", 5), ("S045", 5)]
    }
}

for job in jobs:
    job_id = job["job_id"]
    level = job["level"]
    department = job["department"]
    
    # Get base skills for this level
    if level in level_skill_mapping:
        skill_mapping = level_skill_mapping[level]
        
        # Add technical skills
        for skill_id, min_prof in skill_mapping["technical"]:
            job_skill_reqs.append({
                "job_id": job_id,
                "skill_id": skill_id,
                "min_proficiency": min_prof
            })
        
        # Add soft skills
        for skill_id, min_prof in skill_mapping["soft"]:
            job_skill_reqs.append({
                "job_id": job_id,
                "skill_id": skill_id,
                "min_proficiency": min_prof
            })
        
        # Add leadership skills
        for skill_id, min_prof in skill_mapping["leadership"]:
            job_skill_reqs.append({
                "job_id": job_id,
                "skill_id": skill_id,
                "min_proficiency": min_prof
            })
        
        # Add department-specific skills
        if department == "IT":
            if level in ["Officer", "Senior Officer"]:
                job_skill_reqs.append({"job_id": job_id, "skill_id": "S006", "min_proficiency": 2})
            if level in ["Senior Officer", "Manager", "Senior Manager"]:
                job_skill_reqs.append({"job_id": job_id, "skill_id": "S010", "min_proficiency": 3})
        
        elif department == "Finance":
            if level in ["Officer", "Senior Officer", "Manager"]:
                job_skill_reqs.append({"job_id": job_id, "skill_id": "S018", "min_proficiency": 3})
                job_skill_reqs.append({"job_id": job_id, "skill_id": "S019", "min_proficiency": 3})
        
        elif department == "HR":
            if level in ["Officer", "Senior Officer", "Manager"]:
                job_skill_reqs.append({"job_id": job_id, "skill_id": "S040", "min_proficiency": 3})
                job_skill_reqs.append({"job_id": job_id, "skill_id": "S044", "min_proficiency": 3})

df_job_skills = pd.DataFrame(job_skill_reqs)
job_skills_path = kg_data_dir / "job_skill_requirements.csv"
df_job_skills.to_csv(job_skills_path, index=False)

print(f"   ✓ Created {len(job_skill_reqs)} job-skill requirements")
print(f"   ✓ Saved to: {job_skills_path}")
print()

# ============================================================================
# 4. EMPLOYEE-SKILL MAPPINGS
# ============================================================================

print("4. Creating Employee-Skill Mappings...")

# Load employee data
employee_data_path = repo_root / "data" / "final" / "sample_dataset_1000_balanced.csv"
df_employees = pd.read_csv(employee_data_path)

print(f"   ✓ Loaded {len(df_employees)} employees")

employee_skills = []

np.random.seed(42)

for idx, emp in df_employees.iterrows():
    emp_id = emp['employee_id_hash']
    perf_score = emp['performance_score']
    tenure = emp['tenure_years']
    
    # Determine number of skills based on performance and tenure
    if perf_score >= 90:
        num_skills = np.random.randint(10, 15)
        avg_proficiency = 4.5
    elif perf_score >= 80:
        num_skills = np.random.randint(8, 12)
        avg_proficiency = 3.5
    elif perf_score >= 70:
        num_skills = np.random.randint(6, 10)
        avg_proficiency = 2.5
    else:
        num_skills = np.random.randint(5, 8)
        avg_proficiency = 2.0
    
    # Adjust for tenure
    if tenure > 8:
        num_skills += 2
        avg_proficiency += 0.5
    elif tenure > 5:
        num_skills += 1
        avg_proficiency += 0.3
    
    # Select random skills
    selected_skills = np.random.choice(df_skills['skill_id'].values, 
                                      size=min(num_skills, len(df_skills)), 
                                      replace=False)
    
    for skill_id in selected_skills:
        # Generate proficiency with some randomness
        proficiency = int(np.clip(
            np.random.normal(avg_proficiency, 0.8),
            1, 5
        ))
        
        employee_skills.append({
            "employee_id": emp_id,
            "skill_id": skill_id,
            "proficiency": proficiency
        })

df_emp_skills = pd.DataFrame(employee_skills)
emp_skills_path = kg_data_dir / "employee_skills.csv"
df_emp_skills.to_csv(emp_skills_path, index=False)

print(f"   ✓ Created {len(employee_skills)} employee-skill mappings")
print(f"   ✓ Average skills per employee: {len(employee_skills)/len(df_employees):.1f}")
print(f"   ✓ Saved to: {emp_skills_path}")
print()

# ============================================================================
# 5. DEPARTMENTS
# ============================================================================

print("5. Creating Departments...")

departments = [
    {"dept_id": "D001", "dept_name": "IT", "total_positions": 6},
    {"dept_id": "D002", "dept_name": "HR", "total_positions": 5},
    {"dept_id": "D003", "dept_name": "Finance", "total_positions": 6},
    {"dept_id": "D004", "dept_name": "Operations", "total_positions": 6},
]

df_depts = pd.DataFrame(departments)
depts_path = kg_data_dir / "departments.csv"
df_depts.to_csv(depts_path, index=False)

print(f"   ✓ Created {len(departments)} departments")
print(f"   ✓ Saved to: {depts_path}")
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("✅ SAMPLE DATA CREATION COMPLETE!")
print("=" * 80)
print()

print("Summary:")
print(f"  • Positions: {len(jobs)} (across 6 levels)")
print(f"  • Levels: Non Staff, Officer, Senior Officer, Manager, Senior Manager, Direktur")
print(f"  • Skills: {len(skills)} (Technical: 20, Soft: 15, Leadership: 10)")
print(f"  • Job-Skill Requirements: {len(job_skill_reqs)}")
print(f"  • Employee-Skill Mappings: {len(employee_skills)}")
print(f"  • Departments: {len(departments)}")
print()

print("Files created:")
print(f"  ✓ {jobs_path}")
print(f"  ✓ {skills_path}")
print(f"  ✓ {job_skills_path}")
print(f"  ✓ {emp_skills_path}")
print(f"  ✓ {depts_path}")
print()

print("Next: Run build_graph.py to create the Knowledge Graph!")
