"""
Build Knowledge Graph for MPCIM
================================
Create NetworkX graph with Employee-Job-Skill relationships
"""

import pandas as pd
import numpy as np
import networkx as nx
import pickle
from pathlib import Path
from datetime import datetime

print("=" * 80)
print("BUILDING MPCIM KNOWLEDGE GRAPH")
print("=" * 80)
print()

# Setup paths
repo_root = Path(__file__).resolve().parents[2]
kg_data_dir = repo_root / "data" / "knowledge_graph"
final_dir = repo_root / "data" / "final"
output_dir = repo_root / "results" / "knowledge_graph"
output_dir.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("1. Loading data...")

# Load employee data
df_employees = pd.read_csv(final_dir / "integrated_full_dataset.csv")
print(f"   ✓ Employees: {len(df_employees)}")

# Load jobs
df_jobs = pd.read_csv(kg_data_dir / "jobs.csv")
print(f"   ✓ Jobs: {len(df_jobs)}")

# Load skills
df_skills = pd.read_csv(kg_data_dir / "skills.csv")
print(f"   ✓ Skills: {len(df_skills)}")

# Load job-skill requirements
df_job_skills = pd.read_csv(kg_data_dir / "job_skill_requirements.csv")
print(f"   ✓ Job-Skill Requirements: {len(df_job_skills)}")

# Load employee-skill mappings
df_emp_skills = pd.read_csv(kg_data_dir / "employee_skills.csv")
print(f"   ✓ Employee-Skill Mappings: {len(df_emp_skills)}")

# Load departments
df_depts = pd.read_csv(kg_data_dir / "departments.csv")
print(f"   ✓ Departments: {len(df_depts)}")

print()

# ============================================================================
# 2. CREATE GRAPH
# ============================================================================

print("2. Creating Knowledge Graph...")

# Initialize directed graph
G = nx.DiGraph()

print("   Creating nodes...")

# Add Employee nodes
for _, emp in df_employees.iterrows():
    G.add_node(
        emp['employee_id_hash'],
        node_type='employee',
        name=emp['name'],
        tenure_years=float(emp['tenure_years']),
        performance_score=float(emp['performance_score']),
        behavior_avg=float(emp['behavior_avg']),
        psychological_score=float(emp['psychological_score']),
        drive_score=float(emp['drive_score']),
        mental_strength_score=float(emp['mental_strength_score']),
        adaptability_score=float(emp['adaptability_score']),
        collaboration_score=float(emp['collaboration_score']),
        leadership_potential=float(emp['leadership_potential']),
        holistic_score=float(emp['holistic_score']),
        has_promotion=int(emp['has_promotion']),
        gender=emp['gender'],
        marital_status=emp['marital_status'],
        is_permanent=emp['is_permanent']
    )

print(f"      ✓ Added {len(df_employees)} employee nodes")

# Add Job nodes
for _, job in df_jobs.iterrows():
    G.add_node(
        job['job_id'],
        node_type='job',
        job_title=job['job_title'],
        department=job['department'],
        level=job['level'],
        min_performance=float(job['min_performance']),
        min_behavior=float(job['min_behavior']),
        min_psychological=float(job['min_psychological']),
        min_leadership=float(job['min_leadership']),
        min_tenure=float(job['min_tenure']),
        max_tenure=float(job['max_tenure'])
    )

print(f"      ✓ Added {len(df_jobs)} job nodes")

# Add Skill nodes
for _, skill in df_skills.iterrows():
    G.add_node(
        skill['skill_id'],
        node_type='skill',
        skill_name=skill['skill_name'],
        category=skill['category'],
        importance=int(skill['importance'])
    )

print(f"      ✓ Added {len(df_skills)} skill nodes")

# Add Department nodes
for _, dept in df_depts.iterrows():
    G.add_node(
        dept['dept_id'],
        node_type='department',
        dept_name=dept['dept_name'],
        total_positions=int(dept['total_positions'])
    )

print(f"      ✓ Added {len(df_depts)} department nodes")

print()
print("   Creating relationships...")

# Add Employee-Skill relationships (HAS_SKILL)
for _, row in df_emp_skills.iterrows():
    if G.has_node(row['employee_id']) and G.has_node(row['skill_id']):
        G.add_edge(
            row['employee_id'],
            row['skill_id'],
            relationship='HAS_SKILL',
            proficiency=int(row['proficiency'])
        )

print(f"      ✓ Added {len(df_emp_skills)} HAS_SKILL relationships")

# Add Job-Skill relationships (REQUIRES_SKILL)
for _, row in df_job_skills.iterrows():
    if G.has_node(row['job_id']) and G.has_node(row['skill_id']):
        G.add_edge(
            row['job_id'],
            row['skill_id'],
            relationship='REQUIRES_SKILL',
            min_proficiency=int(row['min_proficiency'])
        )

print(f"      ✓ Added {len(df_job_skills)} REQUIRES_SKILL relationships")

# Add Job-Department relationships (BELONGS_TO)
for _, job in df_jobs.iterrows():
    dept_id = f"D{str(df_depts[df_depts['dept_name'] == job['department']].index[0] + 1).zfill(3)}"
    if G.has_node(job['job_id']) and G.has_node(dept_id):
        G.add_edge(
            job['job_id'],
            dept_id,
            relationship='BELONGS_TO'
        )

print(f"      ✓ Added {len(df_jobs)} BELONGS_TO relationships")

print()

# ============================================================================
# 3. CALCULATE EMPLOYEE-JOB MATCHES (QUALIFIED_FOR)
# ============================================================================

print("3. Calculating Employee-Job match scores...")

def calculate_skill_match(emp_id, job_id):
    """Calculate skill match between employee and job"""
    # Get employee skills
    emp_skills = {}
    for neighbor in G.neighbors(emp_id):
        if G.nodes[neighbor].get('node_type') == 'skill':
            edge_data = G.get_edge_data(emp_id, neighbor)
            if edge_data and edge_data.get('relationship') == 'HAS_SKILL':
                emp_skills[neighbor] = edge_data.get('proficiency', 0)
    
    # Get job required skills
    job_skills = {}
    for neighbor in G.neighbors(job_id):
        if G.nodes[neighbor].get('node_type') == 'skill':
            edge_data = G.get_edge_data(job_id, neighbor)
            if edge_data and edge_data.get('relationship') == 'REQUIRES_SKILL':
                job_skills[neighbor] = edge_data.get('min_proficiency', 0)
    
    if not job_skills:
        return 0.0
    
    # Calculate match
    total_match = 0
    for skill_id, min_prof in job_skills.items():
        emp_prof = emp_skills.get(skill_id, 0)
        if emp_prof >= min_prof:
            total_match += 1
    
    return total_match / len(job_skills)

match_count = 0
qualified_relationships = []

for emp_id in [n for n in G.nodes() if G.nodes[n].get('node_type') == 'employee']:
    emp_data = G.nodes[emp_id]
    
    for job_id in [n for n in G.nodes() if G.nodes[n].get('node_type') == 'job']:
        job_data = G.nodes[job_id]
        
        # Calculate match score components
        # 1. Performance match (30%)
        perf_match = min(emp_data['performance_score'] / job_data['min_performance'], 1.0)
        
        # 2. Behavioral match (25%)
        beh_match = min(emp_data['behavior_avg'] / job_data['min_behavior'], 1.0)
        
        # 3. Psychological match (25%)
        psych_match = min(emp_data['psychological_score'] / job_data['min_psychological'], 1.0)
        
        # 4. Skill match (20%)
        skill_match = calculate_skill_match(emp_id, job_id)
        
        # Total weighted score
        match_score = (
            perf_match * 0.30 +
            beh_match * 0.25 +
            psych_match * 0.25 +
            skill_match * 0.20
        ) * 100
        
        # Only add if match score >= 70% (qualified threshold)
        if match_score >= 70:
            G.add_edge(
                emp_id,
                job_id,
                relationship='QUALIFIED_FOR',
                match_score=round(match_score, 2),
                perf_match=round(perf_match * 100, 2),
                beh_match=round(beh_match * 100, 2),
                psych_match=round(psych_match * 100, 2),
                skill_match=round(skill_match * 100, 2)
            )
            match_count += 1
            
            qualified_relationships.append({
                'employee_id': emp_id,
                'employee_name': emp_data['name'],
                'job_id': job_id,
                'job_title': job_data['job_title'],
                'match_score': round(match_score, 2),
                'perf_match': round(perf_match * 100, 2),
                'beh_match': round(beh_match * 100, 2),
                'psych_match': round(psych_match * 100, 2),
                'skill_match': round(skill_match * 100, 2)
            })

print(f"   ✓ Added {match_count} QUALIFIED_FOR relationships")
print()

# Save qualified relationships to CSV for analysis
df_qualified = pd.DataFrame(qualified_relationships)
df_qualified.to_csv(output_dir / "employee_job_matches.csv", index=False)
print(f"   ✓ Saved matches to: {output_dir / 'employee_job_matches.csv'}")
print()

# ============================================================================
# 4. GRAPH STATISTICS
# ============================================================================

print("4. Graph Statistics:")
print()

total_nodes = G.number_of_nodes()
total_edges = G.number_of_edges()

node_types = {}
for node in G.nodes():
    ntype = G.nodes[node].get('node_type', 'unknown')
    node_types[ntype] = node_types.get(ntype, 0) + 1

edge_types = {}
for u, v in G.edges():
    etype = G.get_edge_data(u, v).get('relationship', 'unknown')
    edge_types[etype] = edge_types.get(etype, 0) + 1

print(f"   Total Nodes: {total_nodes:,}")
print(f"   Total Edges: {total_edges:,}")
print()

print("   Nodes by Type:")
for ntype, count in sorted(node_types.items()):
    print(f"      • {ntype}: {count:,}")
print()

print("   Edges by Type:")
for etype, count in sorted(edge_types.items()):
    print(f"      • {etype}: {count:,}")
print()

# Average degree
avg_degree = sum(dict(G.degree()).values()) / total_nodes
print(f"   Average Degree: {avg_degree:.2f}")
print()

# ============================================================================
# 5. SAVE GRAPH
# ============================================================================

print("5. Saving Knowledge Graph...")

# Save as pickle
graph_file = output_dir / "mpcim_knowledge_graph.pkl"
with open(graph_file, 'wb') as f:
    pickle.dump(G, f)
print(f"   ✓ Saved graph to: {graph_file}")

# Save as GraphML (for Neo4j or other tools)
graphml_file = output_dir / "mpcim_knowledge_graph.graphml"
nx.write_graphml(G, graphml_file)
print(f"   ✓ Saved GraphML to: {graphml_file}")

# Save metadata
metadata = {
    'created_at': datetime.now().isoformat(),
    'total_nodes': total_nodes,
    'total_edges': total_edges,
    'node_types': node_types,
    'edge_types': edge_types,
    'avg_degree': avg_degree
}

metadata_file = output_dir / "graph_metadata.txt"
with open(metadata_file, 'w') as f:
    f.write("MPCIM Knowledge Graph Metadata\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Created: {metadata['created_at']}\n\n")
    f.write(f"Total Nodes: {metadata['total_nodes']:,}\n")
    f.write(f"Total Edges: {metadata['total_edges']:,}\n")
    f.write(f"Average Degree: {metadata['avg_degree']:.2f}\n\n")
    f.write("Nodes by Type:\n")
    for ntype, count in sorted(metadata['node_types'].items()):
        f.write(f"  • {ntype}: {count:,}\n")
    f.write("\nEdges by Type:\n")
    for etype, count in sorted(metadata['edge_types'].items()):
        f.write(f"  • {etype}: {count:,}\n")

print(f"   ✓ Saved metadata to: {metadata_file}")
print()

# ============================================================================
# 6. GENERATE SAMPLE QUERIES
# ============================================================================

print("6. Testing sample queries...")

# Query 1: Top candidates for a specific job
job_id = "L012"  # Manager IT position
if job_id in G.nodes():
    job_title = G.nodes[job_id]['job_title']
else:
    # Fallback to first job
    job_nodes = [n for n in G.nodes() if G.nodes[n].get('node_type') == 'job']
    job_id = job_nodes[0] if job_nodes else None
    job_title = G.nodes[job_id]['job_title'] if job_id else "Unknown"

candidates = []
for emp_id in G.predecessors(job_id):
    if G.nodes[emp_id].get('node_type') == 'employee':
        edge_data = G.get_edge_data(emp_id, job_id)
        if edge_data and edge_data.get('relationship') == 'QUALIFIED_FOR':
            candidates.append({
                'employee_id': emp_id,
                'name': G.nodes[emp_id]['name'],
                'match_score': edge_data['match_score']
            })

candidates.sort(key=lambda x: x['match_score'], reverse=True)
top_5 = candidates[:5]

print(f"\n   Query: Top 5 candidates for '{job_title}':")
for i, cand in enumerate(top_5, 1):
    print(f"      {i}. {cand['name']} - Match: {cand['match_score']:.1f}%")

# Query 2: Jobs qualified for a specific employee
if len(df_employees) > 0:
    sample_emp = df_employees.iloc[0]
    emp_id = sample_emp['employee_id_hash']
    emp_name = sample_emp['name']
    
    qualified_jobs = []
    for job_id in G.successors(emp_id):
        if G.nodes[job_id].get('node_type') == 'job':
            edge_data = G.get_edge_data(emp_id, job_id)
            if edge_data and edge_data.get('relationship') == 'QUALIFIED_FOR':
                qualified_jobs.append({
                    'job_id': job_id,
                    'job_title': G.nodes[job_id]['job_title'],
                    'match_score': edge_data['match_score']
                })
    
    qualified_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    print(f"\n   Query: Jobs qualified for '{emp_name}':")
    for i, job in enumerate(qualified_jobs[:5], 1):
        print(f"      {i}. {job['job_title']} - Match: {job['match_score']:.1f}%")

print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("✅ KNOWLEDGE GRAPH BUILD COMPLETE!")
print("=" * 80)
print()
print("Graph Summary:")
print(f"  • Total Nodes: {total_nodes:,}")
print(f"  • Total Edges: {total_edges:,}")
print(f"  • Employee Nodes: {node_types.get('employee', 0):,}")
print(f"  • Job Nodes: {node_types.get('job', 0):,}")
print(f"  • Skill Nodes: {node_types.get('skill', 0):,}")
print(f"  • Department Nodes: {node_types.get('department', 0):,}")
print()
print("Relationships:")
print(f"  • HAS_SKILL: {edge_types.get('HAS_SKILL', 0):,}")
print(f"  • REQUIRES_SKILL: {edge_types.get('REQUIRES_SKILL', 0):,}")
print(f"  • QUALIFIED_FOR: {edge_types.get('QUALIFIED_FOR', 0):,}")
print(f"  • BELONGS_TO: {edge_types.get('BELONGS_TO', 0):,}")
print()
print("Files Created:")
print(f"  ✓ {graph_file}")
print(f"  ✓ {graphml_file}")
print(f"  ✓ {metadata_file}")
print(f"  ✓ {output_dir / 'employee_job_matches.csv'}")
print()
print("Next: Run graph_queries.py to explore the graph!")
print()
