"""
Create Sample Data for Knowledge Graph
=======================================
Generate job positions, skills, and mappings for MPCIM Knowledge Graph
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 80)
print("CREATING SAMPLE DATA FOR KNOWLEDGE GRAPH")
print("=" * 80)
print()

# Setup paths
repo_root = Path(__file__).resolve().parents[2]
kg_data_dir = repo_root / "data" / "knowledge_graph"
kg_data_dir.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. JOB POSITIONS
# ============================================================================

print("1. Creating Job Positions...")

jobs = [
    # Entry Level
    {
        "job_id": "J001",
        "job_title": "Junior Staff",
        "department": "IT",
        "level": "junior",
        "min_performance": 60,
        "min_behavior": 60,
        "min_psychological": 60,
        "min_leadership": 50,
        "min_tenure": 0,
        "max_tenure": 3
    },
    {
        "job_id": "J002",
        "job_title": "Staff",
        "department": "IT",
        "level": "mid",
        "min_performance": 70,
        "min_behavior": 70,
        "min_psychological": 65,
        "min_leadership": 60,
        "min_tenure": 2,
        "max_tenure": 5
    },
    {
        "job_id": "J003",
        "job_title": "Senior Staff",
        "department": "IT",
        "level": "senior",
        "min_performance": 80,
        "min_behavior": 75,
        "min_psychological": 70,
        "min_leadership": 70,
        "min_tenure": 4,
        "max_tenure": 8
    },
    
    # Supervisor Level
    {
        "job_id": "J004",
        "job_title": "Supervisor",
        "department": "IT",
        "level": "supervisor",
        "min_performance": 85,
        "min_behavior": 80,
        "min_psychological": 75,
        "min_leadership": 75,
        "min_tenure": 5,
        "max_tenure": 10
    },
    {
        "job_id": "J005",
        "job_title": "Senior Supervisor",
        "department": "IT",
        "level": "supervisor",
        "min_performance": 88,
        "min_behavior": 82,
        "min_psychological": 78,
        "min_leadership": 78,
        "min_tenure": 6,
        "max_tenure": 12
    },
    
    # Manager Level
    {
        "job_id": "J006",
        "job_title": "Manager",
        "department": "IT",
        "level": "manager",
        "min_performance": 90,
        "min_behavior": 85,
        "min_psychological": 80,
        "min_leadership": 80,
        "min_tenure": 7,
        "max_tenure": 15
    },
    {
        "job_id": "J007",
        "job_title": "Senior Manager",
        "department": "IT",
        "level": "manager",
        "min_performance": 92,
        "min_behavior": 87,
        "min_psychological": 82,
        "min_leadership": 85,
        "min_tenure": 8,
        "max_tenure": 20
    },
    
    # HR Department
    {
        "job_id": "J008",
        "job_title": "HR Staff",
        "department": "HR",
        "level": "mid",
        "min_performance": 70,
        "min_behavior": 75,
        "min_psychological": 70,
        "min_leadership": 60,
        "min_tenure": 2,
        "max_tenure": 5
    },
    {
        "job_id": "J009",
        "job_title": "HR Supervisor",
        "department": "HR",
        "level": "supervisor",
        "min_performance": 85,
        "min_behavior": 85,
        "min_psychological": 80,
        "min_leadership": 75,
        "min_tenure": 5,
        "max_tenure": 10
    },
    {
        "job_id": "J010",
        "job_title": "HR Manager",
        "department": "HR",
        "level": "manager",
        "min_performance": 90,
        "min_behavior": 88,
        "min_psychological": 85,
        "min_leadership": 85,
        "min_tenure": 7,
        "max_tenure": 15
    },
    
    # Finance Department
    {
        "job_id": "J011",
        "job_title": "Finance Staff",
        "department": "Finance",
        "level": "mid",
        "min_performance": 75,
        "min_behavior": 70,
        "min_psychological": 65,
        "min_leadership": 60,
        "min_tenure": 2,
        "max_tenure": 5
    },
    {
        "job_id": "J012",
        "job_title": "Finance Supervisor",
        "department": "Finance",
        "level": "supervisor",
        "min_performance": 85,
        "min_behavior": 80,
        "min_psychological": 75,
        "min_leadership": 75,
        "min_tenure": 5,
        "max_tenure": 10
    },
    {
        "job_id": "J013",
        "job_title": "Finance Manager",
        "department": "Finance",
        "level": "manager",
        "min_performance": 92,
        "min_behavior": 85,
        "min_psychological": 80,
        "min_leadership": 82,
        "min_tenure": 7,
        "max_tenure": 15
    },
    
    # Operations
    {
        "job_id": "J014",
        "job_title": "Operations Supervisor",
        "department": "Operations",
        "level": "supervisor",
        "min_performance": 85,
        "min_behavior": 82,
        "min_psychological": 75,
        "min_leadership": 75,
        "min_tenure": 5,
        "max_tenure": 10
    },
    {
        "job_id": "J015",
        "job_title": "Operations Manager",
        "department": "Operations",
        "level": "manager",
        "min_performance": 90,
        "min_behavior": 85,
        "min_psychological": 80,
        "min_leadership": 82,
        "min_tenure": 7,
        "max_tenure": 15
    }
]

df_jobs = pd.DataFrame(jobs)
df_jobs.to_csv(kg_data_dir / "jobs.csv", index=False)
print(f"   ✓ Created {len(jobs)} job positions")
print()

# ============================================================================
# 2. SKILLS
# ============================================================================

print("2. Creating Skills...")

skills = [
    # Technical Skills
    {"skill_id": "S001", "skill_name": "Python Programming", "category": "Technical", "importance": 5},
    {"skill_id": "S002", "skill_name": "Data Analysis", "category": "Technical", "importance": 5},
    {"skill_id": "S003", "skill_name": "SQL Database", "category": "Technical", "importance": 4},
    {"skill_id": "S004", "skill_name": "Machine Learning", "category": "Technical", "importance": 4},
    {"skill_id": "S005", "skill_name": "Web Development", "category": "Technical", "importance": 3},
    {"skill_id": "S006", "skill_name": "Cloud Computing", "category": "Technical", "importance": 4},
    {"skill_id": "S007", "skill_name": "DevOps", "category": "Technical", "importance": 3},
    {"skill_id": "S008", "skill_name": "Cybersecurity", "category": "Technical", "importance": 4},
    {"skill_id": "S009", "skill_name": "Network Administration", "category": "Technical", "importance": 3},
    {"skill_id": "S010", "skill_name": "System Design", "category": "Technical", "importance": 5},
    
    # Soft Skills
    {"skill_id": "S011", "skill_name": "Communication", "category": "Soft", "importance": 5},
    {"skill_id": "S012", "skill_name": "Teamwork", "category": "Soft", "importance": 5},
    {"skill_id": "S013", "skill_name": "Problem Solving", "category": "Soft", "importance": 5},
    {"skill_id": "S014", "skill_name": "Time Management", "category": "Soft", "importance": 4},
    {"skill_id": "S015", "skill_name": "Adaptability", "category": "Soft", "importance": 4},
    {"skill_id": "S016", "skill_name": "Critical Thinking", "category": "Soft", "importance": 5},
    {"skill_id": "S017", "skill_name": "Creativity", "category": "Soft", "importance": 3},
    {"skill_id": "S018", "skill_name": "Emotional Intelligence", "category": "Soft", "importance": 4},
    {"skill_id": "S019", "skill_name": "Conflict Resolution", "category": "Soft", "importance": 4},
    {"skill_id": "S020", "skill_name": "Negotiation", "category": "Soft", "importance": 3},
    
    # Leadership Skills
    {"skill_id": "S021", "skill_name": "Team Leadership", "category": "Leadership", "importance": 5},
    {"skill_id": "S022", "skill_name": "Strategic Thinking", "category": "Leadership", "importance": 5},
    {"skill_id": "S023", "skill_name": "Decision Making", "category": "Leadership", "importance": 5},
    {"skill_id": "S024", "skill_name": "Mentoring", "category": "Leadership", "importance": 4},
    {"skill_id": "S025", "skill_name": "Project Management", "category": "Leadership", "importance": 5},
    {"skill_id": "S026", "skill_name": "Change Management", "category": "Leadership", "importance": 4},
    {"skill_id": "S027", "skill_name": "Stakeholder Management", "category": "Leadership", "importance": 4},
    {"skill_id": "S028", "skill_name": "Vision Setting", "category": "Leadership", "importance": 4},
    {"skill_id": "S029", "skill_name": "Performance Management", "category": "Leadership", "importance": 4},
    {"skill_id": "S030", "skill_name": "Budget Management", "category": "Leadership", "importance": 3},
    
    # Domain Skills - HR
    {"skill_id": "S031", "skill_name": "Recruitment", "category": "Domain-HR", "importance": 5},
    {"skill_id": "S032", "skill_name": "Employee Relations", "category": "Domain-HR", "importance": 5},
    {"skill_id": "S033", "skill_name": "Performance Appraisal", "category": "Domain-HR", "importance": 4},
    {"skill_id": "S034", "skill_name": "Training & Development", "category": "Domain-HR", "importance": 4},
    {"skill_id": "S035", "skill_name": "Compensation & Benefits", "category": "Domain-HR", "importance": 4},
    
    # Domain Skills - Finance
    {"skill_id": "S036", "skill_name": "Financial Analysis", "category": "Domain-Finance", "importance": 5},
    {"skill_id": "S037", "skill_name": "Accounting", "category": "Domain-Finance", "importance": 5},
    {"skill_id": "S038", "skill_name": "Budgeting", "category": "Domain-Finance", "importance": 4},
    {"skill_id": "S039", "skill_name": "Financial Reporting", "category": "Domain-Finance", "importance": 5},
    {"skill_id": "S040", "skill_name": "Tax Management", "category": "Domain-Finance", "importance": 3},
    
    # Domain Skills - Operations
    {"skill_id": "S041", "skill_name": "Process Optimization", "category": "Domain-Operations", "importance": 5},
    {"skill_id": "S042", "skill_name": "Quality Control", "category": "Domain-Operations", "importance": 4},
    {"skill_id": "S043", "skill_name": "Supply Chain", "category": "Domain-Operations", "importance": 4},
    {"skill_id": "S044", "skill_name": "Logistics", "category": "Domain-Operations", "importance": 3},
    {"skill_id": "S045", "skill_name": "Inventory Management", "category": "Domain-Operations", "importance": 3},
]

df_skills = pd.DataFrame(skills)
df_skills.to_csv(kg_data_dir / "skills.csv", index=False)
print(f"   ✓ Created {len(skills)} skills")
print()

# ============================================================================
# 3. JOB-SKILL REQUIREMENTS
# ============================================================================

print("3. Creating Job-Skill Requirements...")

job_skill_requirements = []

# IT Jobs
it_skills = ["S001", "S002", "S003", "S004", "S005", "S006", "S007", "S008", "S009", "S010",
             "S011", "S012", "S013", "S014", "S015", "S016"]

for job_id in ["J001", "J002", "J003", "J004", "J005", "J006", "J007"]:
    job = df_jobs[df_jobs['job_id'] == job_id].iloc[0]
    
    # Select skills based on level
    if job['level'] == 'junior':
        selected_skills = np.random.choice(it_skills, size=8, replace=False)
        min_levels = [2, 2, 2, 2, 3, 3, 3, 3]
    elif job['level'] == 'mid':
        selected_skills = np.random.choice(it_skills, size=10, replace=False)
        min_levels = [3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
    elif job['level'] == 'senior':
        selected_skills = np.random.choice(it_skills, size=12, replace=False)
        min_levels = [4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5]
    elif job['level'] == 'supervisor':
        selected_skills = it_skills[:14]
        min_levels = [4] * 10 + [5] * 4
    else:  # manager
        selected_skills = it_skills
        min_levels = [5] * 16
    
    for skill_id, min_level in zip(selected_skills, min_levels):
        job_skill_requirements.append({
            "job_id": job_id,
            "skill_id": skill_id,
            "min_proficiency": min_level
        })

# HR Jobs
hr_skills = ["S011", "S012", "S013", "S018", "S019", "S020", "S021", "S024", "S031", "S032", "S033", "S034", "S035"]

for job_id in ["J008", "J009", "J010"]:
    job = df_jobs[df_jobs['job_id'] == job_id].iloc[0]
    
    if job['level'] == 'mid':
        selected_skills = np.random.choice(hr_skills, size=8, replace=False)
        min_levels = [3, 3, 3, 3, 4, 4, 4, 4]
    elif job['level'] == 'supervisor':
        selected_skills = np.random.choice(hr_skills, size=10, replace=False)
        min_levels = [4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    else:  # manager
        selected_skills = hr_skills
        min_levels = [5] * 13
    
    for skill_id, min_level in zip(selected_skills, min_levels):
        job_skill_requirements.append({
            "job_id": job_id,
            "skill_id": skill_id,
            "min_proficiency": min_level
        })

# Finance Jobs
finance_skills = ["S011", "S013", "S014", "S016", "S025", "S030", "S036", "S037", "S038", "S039", "S040"]

for job_id in ["J011", "J012", "J013"]:
    job = df_jobs[df_jobs['job_id'] == job_id].iloc[0]
    
    if job['level'] == 'mid':
        selected_skills = np.random.choice(finance_skills, size=7, replace=False)
        min_levels = [3, 3, 3, 4, 4, 4, 4]
    elif job['level'] == 'supervisor':
        selected_skills = np.random.choice(finance_skills, size=9, replace=False)
        min_levels = [4, 4, 4, 4, 5, 5, 5, 5, 5]
    else:  # manager
        selected_skills = finance_skills
        min_levels = [5] * 11
    
    for skill_id, min_level in zip(selected_skills, min_levels):
        job_skill_requirements.append({
            "job_id": job_id,
            "skill_id": skill_id,
            "min_proficiency": min_level
        })

# Operations Jobs
ops_skills = ["S011", "S012", "S013", "S014", "S015", "S021", "S025", "S041", "S042", "S043", "S044", "S045"]

for job_id in ["J014", "J015"]:
    job = df_jobs[df_jobs['job_id'] == job_id].iloc[0]
    
    if job['level'] == 'supervisor':
        selected_skills = np.random.choice(ops_skills, size=9, replace=False)
        min_levels = [4, 4, 4, 4, 5, 5, 5, 5, 5]
    else:  # manager
        selected_skills = ops_skills
        min_levels = [5] * 12
    
    for skill_id, min_level in zip(selected_skills, min_levels):
        job_skill_requirements.append({
            "job_id": job_id,
            "skill_id": skill_id,
            "min_proficiency": min_level
        })

df_job_skills = pd.DataFrame(job_skill_requirements)
df_job_skills.to_csv(kg_data_dir / "job_skill_requirements.csv", index=False)
print(f"   ✓ Created {len(job_skill_requirements)} job-skill requirements")
print()

# ============================================================================
# 4. EMPLOYEE-SKILL MAPPINGS (from existing employee data)
# ============================================================================

print("4. Creating Employee-Skill Mappings...")

# Load employee data
final_dir = repo_root / "data" / "final"
df_employees = pd.read_csv(final_dir / "integrated_full_dataset.csv")

employee_skills = []

# Assign skills to employees based on their scores and department
for _, emp in df_employees.iterrows():
    emp_id = emp['employee_id_hash']
    
    # Determine department (simplified - use company_id % 4)
    dept_num = emp['company_id'] % 4
    if dept_num == 0:
        dept = "IT"
        dept_skills = it_skills
    elif dept_num == 1:
        dept = "HR"
        dept_skills = hr_skills
    elif dept_num == 2:
        dept = "Finance"
        dept_skills = finance_skills
    else:
        dept = "Operations"
        dept_skills = ops_skills
    
    # Number of skills based on performance
    if emp['performance_score'] >= 85:
        num_skills = np.random.randint(10, 15)
    elif emp['performance_score'] >= 70:
        num_skills = np.random.randint(7, 12)
    else:
        num_skills = np.random.randint(5, 9)
    
    # Select random skills
    selected_skills = np.random.choice(dept_skills, size=min(num_skills, len(dept_skills)), replace=False)
    
    for skill_id in selected_skills:
        # Proficiency based on scores
        base_prof = (emp['performance_score'] + emp['behavior_avg'] + emp['psychological_score']) / 60
        proficiency = int(np.clip(base_prof + np.random.normal(0, 0.5), 1, 5))
        
        employee_skills.append({
            "employee_id": emp_id,
            "skill_id": skill_id,
            "proficiency": proficiency
        })

df_emp_skills = pd.DataFrame(employee_skills)
df_emp_skills.to_csv(kg_data_dir / "employee_skills.csv", index=False)
print(f"   ✓ Created {len(employee_skills)} employee-skill mappings")
print()

# ============================================================================
# 5. DEPARTMENTS
# ============================================================================

print("5. Creating Departments...")

departments = [
    {"dept_id": "D001", "dept_name": "IT", "total_positions": 7},
    {"dept_id": "D002", "dept_name": "HR", "total_positions": 3},
    {"dept_id": "D003", "dept_name": "Finance", "total_positions": 3},
    {"dept_id": "D004", "dept_name": "Operations", "total_positions": 2}
]

df_depts = pd.DataFrame(departments)
df_depts.to_csv(kg_data_dir / "departments.csv", index=False)
print(f"   ✓ Created {len(departments)} departments")
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("✅ SAMPLE DATA CREATION COMPLETE!")
print("=" * 80)
print()
print("Files created:")
print(f"  ✓ {kg_data_dir / 'jobs.csv'} ({len(jobs)} jobs)")
print(f"  ✓ {kg_data_dir / 'skills.csv'} ({len(skills)} skills)")
print(f"  ✓ {kg_data_dir / 'job_skill_requirements.csv'} ({len(job_skill_requirements)} requirements)")
print(f"  ✓ {kg_data_dir / 'employee_skills.csv'} ({len(employee_skills)} mappings)")
print(f"  ✓ {kg_data_dir / 'departments.csv'} ({len(departments)} departments)")
print()
print("Summary:")
print(f"  • Jobs: {len(jobs)} positions across 4 departments")
print(f"  • Skills: {len(skills)} skills (Technical, Soft, Leadership, Domain)")
print(f"  • Employees: {len(df_employees)} with skill mappings")
print(f"  • Total Relationships: ~{len(job_skill_requirements) + len(employee_skills)}")
print()
print("Next step: Run build_graph.py to create the Knowledge Graph!")
print()
