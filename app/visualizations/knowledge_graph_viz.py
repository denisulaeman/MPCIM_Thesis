"""
Knowledge Graph Visualization
==============================
Interactive graph visualization using Pyvis
"""

from pyvis.network import Network
import networkx as nx
from typing import Optional, List, Set
import tempfile
from pathlib import Path

def create_interactive_graph(
    graph: nx.DiGraph,
    job_filter: Optional[str] = None,
    department_filter: Optional[str] = None,
    show_employees: bool = True,
    show_jobs: bool = True,
    show_skills: bool = True,
    max_employees: int = 50,
    height: str = "700px",
    width: str = "100%"
) -> str:
    """
    Create interactive Knowledge Graph visualization
    
    Args:
        graph: NetworkX graph
        job_filter: Filter by specific job ID
        department_filter: Filter by department
        show_employees: Show employee nodes
        show_jobs: Show job nodes
        show_skills: Show skill nodes
        max_employees: Maximum number of employees to show
        height: Graph height
        width: Graph width
        
    Returns:
        HTML string of the interactive graph
    """
    
    # Create Pyvis network
    net = Network(
        height=height,
        width=width,
        bgcolor='#ffffff',
        font_color='#2d3748',
        directed=True
    )
    
    # Configure physics and appearance
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "forceAtlas2Based": {
                "gravitationalConstant": -80,
                "centralGravity": 0.015,
                "springLength": 250,
                "springConstant": 0.05,
                "damping": 0.4
            },
            "maxVelocity": 50,
            "solver": "forceAtlas2Based",
            "timestep": 0.35,
            "stabilization": {
                "iterations": 200,
                "updateInterval": 25
            }
        },
        "nodes": {
            "font": {
                "size": 16,
                "face": "Arial",
                "color": "#2d3748"
            },
            "borderWidth": 2,
            "borderWidthSelected": 3
        },
        "edges": {
            "font": {
                "size": 14,
                "align": "middle"
            },
            "smooth": {
                "type": "continuous",
                "roundness": 0.5
            },
            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                }
            }
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 100,
            "navigationButtons": true,
            "keyboard": {
                "enabled": true
            }
        }
    }
    """)
    
    # Collect nodes to display
    nodes_to_show: Set[str] = set()
    
    # Filter logic
    if job_filter:
        # Show specific job and its related nodes
        if job_filter in graph.nodes():
            nodes_to_show.add(job_filter)
            
            # Add employees qualified for this job
            emp_count = 0
            for emp_id in graph.predecessors(job_filter):
                if graph.nodes[emp_id].get('node_type') == 'employee':
                    edge_data = graph.get_edge_data(emp_id, job_filter)
                    if edge_data and edge_data.get('relationship') == 'QUALIFIED_FOR':
                        nodes_to_show.add(emp_id)
                        emp_count += 1
                        if emp_count >= max_employees:
                            break
            
            # Add required skills
            for skill_id in graph.neighbors(job_filter):
                if graph.nodes[skill_id].get('node_type') == 'skill':
                    nodes_to_show.add(skill_id)
    
    elif department_filter:
        # Show all jobs in department and sample employees
        for node_id in graph.nodes():
            node_data = graph.nodes[node_id]
            
            if node_data.get('node_type') == 'job':
                if node_data.get('department') == department_filter:
                    nodes_to_show.add(node_id)
                    
                    # Add some employees
                    emp_count = 0
                    for emp_id in graph.predecessors(node_id):
                        if graph.nodes[emp_id].get('node_type') == 'employee':
                            nodes_to_show.add(emp_id)
                            emp_count += 1
                            if emp_count >= 5:  # 5 employees per job
                                break
    
    else:
        # Show sample of all node types
        emp_count = 0
        job_count = 0
        skill_count = 0
        
        for node_id in graph.nodes():
            node_type = graph.nodes[node_id].get('node_type')
            
            if node_type == 'employee' and show_employees and emp_count < max_employees:
                nodes_to_show.add(node_id)
                emp_count += 1
            elif node_type == 'job' and show_jobs and job_count < 15:
                nodes_to_show.add(node_id)
                job_count += 1
            elif node_type == 'skill' and show_skills and skill_count < 30:
                nodes_to_show.add(node_id)
                skill_count += 1
    
    # Add nodes to visualization
    for node_id in nodes_to_show:
        node_data = graph.nodes[node_id]
        node_type = node_data.get('node_type', 'unknown')
        
        # Node styling based on type
        if node_type == 'employee':
            color = '#667eea'  # Purple
            shape = 'dot'
            size = 20
            # Simple text format without HTML tags
            name = node_data.get('name', 'Unknown')
            perf = node_data.get('performance_score', 0)
            beh = node_data.get('behavior_avg', 0)
            psych = node_data.get('psychological_score', 0)
            lead = node_data.get('leadership_potential', 0)
            tenure = node_data.get('tenure_years', 0)
            
            title = f"{name}\nPerformance: {perf:.1f}\nBehavior: {beh:.1f}\nPsychological: {psych:.1f}\nLeadership: {lead:.1f}\nTenure: {tenure:.0f} years"
            label = name[:20]
            
        elif node_type == 'job':
            color = '#43e97b'  # Green
            shape = 'box'
            size = 30
            # Simple text format without HTML tags
            job_title = node_data.get('job_title', 'Unknown')
            dept = node_data.get('department', 'Unknown')
            level = node_data.get('level', 'Unknown')
            min_perf = node_data.get('min_performance', 0)
            min_beh = node_data.get('min_behavior', 0)
            min_psych = node_data.get('min_psychological', 0)
            
            title = f"{job_title}\nDepartment: {dept}\nLevel: {level}\nMin Performance: {min_perf:.0f}\nMin Behavior: {min_beh:.0f}\nMin Psychological: {min_psych:.0f}"
            label = job_title
            
        elif node_type == 'skill':
            color = '#f093fb'  # Pink
            shape = 'triangle'
            size = 15
            # Simple text format without HTML tags
            skill_name = node_data.get('skill_name', 'Unknown')
            category = node_data.get('category', 'Unknown')
            importance = node_data.get('importance', 0)
            
            title = f"{skill_name}\nCategory: {category}\nImportance: {importance}/5"
            label = skill_name[:20]
            
        elif node_type == 'department':
            color = '#feca57'  # Yellow
            shape = 'star'
            size = 35
            # Simple text format without HTML tags
            dept_name = node_data.get('dept_name', 'Unknown')
            positions = node_data.get('total_positions', 0)
            
            title = f"{dept_name}\nPositions: {positions}"
            label = dept_name
            
        else:
            color = '#718096'  # Gray
            shape = 'dot'
            size = 10
            title = str(node_id)
            label = str(node_id)[:10]
        
        net.add_node(
            node_id,
            label=label,
            title=title,
            color=color,
            shape=shape,
            size=size
        )
    
    # Add edges
    for u, v in graph.edges():
        if u in nodes_to_show and v in nodes_to_show:
            edge_data = graph.get_edge_data(u, v)
            relationship = edge_data.get('relationship', 'unknown')
            
            # Edge styling based on relationship
            if relationship == 'QUALIFIED_FOR':
                match_score = edge_data.get('match_score', 0)
                color = f'rgba(102, 126, 234, {match_score/100})'  # Opacity by match score
                width = 1 + (match_score / 50)  # Width by match score
                title = f"Match: {match_score:.1f}%"
                
            elif relationship == 'HAS_SKILL':
                proficiency = edge_data.get('proficiency', 0)
                color = f'rgba(240, 147, 251, {proficiency/5})'
                width = proficiency / 2
                title = f"Proficiency: {proficiency}/5"
                
            elif relationship == 'REQUIRES_SKILL':
                min_prof = edge_data.get('min_proficiency', 0)
                color = 'rgba(67, 233, 123, 0.5)'
                width = 1
                title = f"Required: {min_prof}/5"
                
            elif relationship == 'BELONGS_TO':
                color = 'rgba(254, 202, 87, 0.7)'
                width = 2
                title = "Belongs To"
                
            else:
                color = 'rgba(113, 128, 150, 0.3)'
                width = 1
                title = relationship
            
            net.add_edge(
                u, v,
                title=title,
                color=color,
                width=width
            )
    
    # Generate HTML
    html = net.generate_html()
    
    return html


def save_graph_html(html: str, filename: str = "knowledge_graph.html") -> str:
    """
    Save graph HTML to temporary file
    
    Args:
        html: HTML string
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    temp_dir = Path(tempfile.gettempdir())
    output_path = temp_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(output_path)


def create_job_focused_graph(
    graph: nx.DiGraph,
    job_id: str,
    top_n: int = 10
) -> str:
    """
    Create graph focused on a specific job and its top candidates
    
    Args:
        graph: NetworkX graph
        job_id: Job identifier
        top_n: Number of top candidates to show
        
    Returns:
        HTML string
    """
    
    net = Network(height="600px", width="100%", bgcolor='#ffffff', font_color='#2d3748')
    
    # Configure better physics and font
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "forceAtlas2Based": {
                "gravitationalConstant": -80,
                "centralGravity": 0.02,
                "springLength": 150,
                "springConstant": 0.1
            },
            "solver": "forceAtlas2Based",
            "stabilization": {"iterations": 200}
        },
        "nodes": {
            "font": {"size": 16, "face": "Arial"}
        },
        "edges": {
            "font": {"size": 14},
            "smooth": {"type": "continuous"}
        }
    }
    """)
    
    # Add job node
    if job_id not in graph.nodes():
        return "<p>Job not found</p>"
    
    job_data = graph.nodes[job_id]
    job_title = job_data.get('job_title', 'Unknown')
    dept = job_data.get('department', 'Unknown')
    level = job_data.get('level', 'Unknown')
    
    net.add_node(
        job_id,
        label=job_title,
        color='#43e97b',
        shape='box',
        size=40,
        title=f"{job_title}\nDepartment: {dept}\nLevel: {level}"
    )
    
    # Get top candidates
    candidates = []
    for emp_id in graph.predecessors(job_id):
        if graph.nodes[emp_id].get('node_type') == 'employee':
            edge_data = graph.get_edge_data(emp_id, job_id)
            if edge_data and edge_data.get('relationship') == 'QUALIFIED_FOR':
                candidates.append({
                    'id': emp_id,
                    'match_score': edge_data.get('match_score', 0)
                })
    
    # Sort and take top N
    candidates.sort(key=lambda x: x['match_score'], reverse=True)
    top_candidates = candidates[:top_n]
    
    # Add candidate nodes
    for rank, cand in enumerate(top_candidates, 1):
        emp_id = cand['id']
        emp_data = graph.nodes[emp_id]
        match_score = cand['match_score']
        
        # Color gradient based on rank
        if rank == 1:
            color = '#FFD700'  # Gold
            size = 30
        elif rank == 2:
            color = '#C0C0C0'  # Silver
            size = 25
        elif rank == 3:
            color = '#CD7F32'  # Bronze
            size = 22
        else:
            color = '#667eea'
            size = 18
        
        # Simple text format without HTML tags
        name = emp_data.get('name', 'Unknown')
        perf = emp_data.get('performance_score', 0)
        beh = emp_data.get('behavior_avg', 0)
        psych = emp_data.get('psychological_score', 0)
        
        net.add_node(
            emp_id,
            label=f"#{rank} {name[:15]}",
            color=color,
            size=size,
            title=f"#{rank}: {name}\nMatch Score: {match_score:.1f}%\nPerformance: {perf:.1f}\nBehavior: {beh:.1f}\nPsychological: {psych:.1f}"
        )
        
        # Add edge
        net.add_edge(
            emp_id,
            job_id,
            title=f"Match: {match_score:.1f}%",
            color=f'rgba(102, 126, 234, {match_score/100})',
            width=2 + (match_score / 25)
        )
    
    return net.generate_html()
