"""
Job Matching Service for MPCIM Knowledge Graph
===============================================
Service for querying Knowledge Graph and matching employees to jobs
"""

import pickle
import pandas as pd
import networkx as nx
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class JobMatchingService:
    """Service for job matching using Knowledge Graph"""
    
    def __init__(self):
        """Initialize the service and load Knowledge Graph"""
        self.repo_root = Path(__file__).resolve().parents[2]
        self.graph_file = self.repo_root / "results" / "knowledge_graph" / "mpcim_knowledge_graph.pkl"
        self.graph = None
        self.load_graph()
    
    def load_graph(self) -> bool:
        """Load Knowledge Graph from pickle file"""
        try:
            with open(self.graph_file, 'rb') as f:
                self.graph = pickle.load(f)
            return True
        except Exception as e:
            print(f"Error loading graph: {e}")
            return False
    
    def get_top_candidates(self, job_id: str, top_n: int = 5) -> List[Dict]:
        """
        Get top N candidates for a job position
        
        Args:
            job_id: Job identifier (e.g., 'J006')
            top_n: Number of top candidates to return
            
        Returns:
            List of candidate dictionaries with match details
        """
        if not self.graph or job_id not in self.graph.nodes():
            return []
        
        candidates = []
        
        # Get all employees qualified for this job
        for emp_id in self.graph.predecessors(job_id):
            if self.graph.nodes[emp_id].get('node_type') == 'employee':
                edge_data = self.graph.get_edge_data(emp_id, job_id)
                
                if edge_data and edge_data.get('relationship') == 'QUALIFIED_FOR':
                    emp_data = self.graph.nodes[emp_id]
                    
                    candidates.append({
                        'employee_id': emp_id,
                        'name': emp_data.get('name', 'Unknown'),
                        'match_score': edge_data.get('match_score', 0),
                        'perf_match': edge_data.get('perf_match', 0),
                        'beh_match': edge_data.get('beh_match', 0),
                        'psych_match': edge_data.get('psych_match', 0),
                        'skill_match': edge_data.get('skill_match', 0),
                        'performance_score': emp_data.get('performance_score', 0),
                        'behavior_avg': emp_data.get('behavior_avg', 0),
                        'psychological_score': emp_data.get('psychological_score', 0),
                        'leadership_potential': emp_data.get('leadership_potential', 0),
                        'tenure_years': emp_data.get('tenure_years', 0),
                        'holistic_score': emp_data.get('holistic_score', 0)
                    })
        
        # Sort by match score descending
        candidates.sort(key=lambda x: x['match_score'], reverse=True)
        
        return candidates[:top_n]
    
    def get_qualified_jobs(self, employee_id: str) -> List[Dict]:
        """
        Get all jobs an employee is qualified for
        
        Args:
            employee_id: Employee identifier (hash)
            
        Returns:
            List of job dictionaries with match details
        """
        if not self.graph or employee_id not in self.graph.nodes():
            return []
        
        qualified_jobs = []
        
        # Get all jobs this employee is qualified for
        for job_id in self.graph.successors(employee_id):
            if self.graph.nodes[job_id].get('node_type') == 'job':
                edge_data = self.graph.get_edge_data(employee_id, job_id)
                
                if edge_data and edge_data.get('relationship') == 'QUALIFIED_FOR':
                    job_data = self.graph.nodes[job_id]
                    
                    qualified_jobs.append({
                        'job_id': job_id,
                        'job_title': job_data.get('job_title', 'Unknown'),
                        'department': job_data.get('department', 'Unknown'),
                        'level': job_data.get('level', 'Unknown'),
                        'match_score': edge_data.get('match_score', 0),
                        'perf_match': edge_data.get('perf_match', 0),
                        'beh_match': edge_data.get('beh_match', 0),
                        'psych_match': edge_data.get('psych_match', 0),
                        'skill_match': edge_data.get('skill_match', 0),
                        'min_performance': job_data.get('min_performance', 0),
                        'min_behavior': job_data.get('min_behavior', 0),
                        'min_psychological': job_data.get('min_psychological', 0),
                        'min_leadership': job_data.get('min_leadership', 0)
                    })
        
        # Sort by match score descending
        qualified_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        return qualified_jobs
    
    def get_match_details(self, employee_id: str, job_id: str) -> Optional[Dict]:
        """
        Get detailed match information between employee and job
        
        Args:
            employee_id: Employee identifier
            job_id: Job identifier
            
        Returns:
            Dictionary with detailed match breakdown
        """
        if not self.graph:
            return None
        
        if employee_id not in self.graph.nodes() or job_id not in self.graph.nodes():
            return None
        
        edge_data = self.graph.get_edge_data(employee_id, job_id)
        
        if not edge_data or edge_data.get('relationship') != 'QUALIFIED_FOR':
            return None
        
        emp_data = self.graph.nodes[employee_id]
        job_data = self.graph.nodes[job_id]
        
        # Get employee skills
        emp_skills = []
        for neighbor in self.graph.neighbors(employee_id):
            if self.graph.nodes[neighbor].get('node_type') == 'skill':
                skill_edge = self.graph.get_edge_data(employee_id, neighbor)
                if skill_edge and skill_edge.get('relationship') == 'HAS_SKILL':
                    emp_skills.append({
                        'skill_id': neighbor,
                        'skill_name': self.graph.nodes[neighbor].get('skill_name', 'Unknown'),
                        'proficiency': skill_edge.get('proficiency', 0)
                    })
        
        # Get job required skills
        job_skills = []
        for neighbor in self.graph.neighbors(job_id):
            if self.graph.nodes[neighbor].get('node_type') == 'skill':
                skill_edge = self.graph.get_edge_data(job_id, neighbor)
                if skill_edge and skill_edge.get('relationship') == 'REQUIRES_SKILL':
                    job_skills.append({
                        'skill_id': neighbor,
                        'skill_name': self.graph.nodes[neighbor].get('skill_name', 'Unknown'),
                        'min_proficiency': skill_edge.get('min_proficiency', 0)
                    })
        
        return {
            'employee': {
                'id': employee_id,
                'name': emp_data.get('name', 'Unknown'),
                'performance_score': emp_data.get('performance_score', 0),
                'behavior_avg': emp_data.get('behavior_avg', 0),
                'psychological_score': emp_data.get('psychological_score', 0),
                'leadership_potential': emp_data.get('leadership_potential', 0),
                'tenure_years': emp_data.get('tenure_years', 0),
                'skills': emp_skills
            },
            'job': {
                'id': job_id,
                'title': job_data.get('job_title', 'Unknown'),
                'department': job_data.get('department', 'Unknown'),
                'level': job_data.get('level', 'Unknown'),
                'min_performance': job_data.get('min_performance', 0),
                'min_behavior': job_data.get('min_behavior', 0),
                'min_psychological': job_data.get('min_psychological', 0),
                'min_leadership': job_data.get('min_leadership', 0),
                'required_skills': job_skills
            },
            'match': {
                'overall_score': edge_data.get('match_score', 0),
                'perf_match': edge_data.get('perf_match', 0),
                'beh_match': edge_data.get('beh_match', 0),
                'psych_match': edge_data.get('psych_match', 0),
                'skill_match': edge_data.get('skill_match', 0)
            }
        }
    
    def get_career_path(self, employee_id: str, max_steps: int = 3) -> List[Dict]:
        """
        Get recommended career path for employee
        
        Args:
            employee_id: Employee identifier
            max_steps: Maximum number of career steps to show
            
        Returns:
            List of recommended positions in order
        """
        qualified_jobs = self.get_qualified_jobs(employee_id)
        
        if not qualified_jobs:
            return []
        
        # Sort by level progression (junior -> mid -> senior -> supervisor -> manager)
        level_order = {'junior': 1, 'mid': 2, 'senior': 3, 'supervisor': 4, 'manager': 5}
        
        # Filter and sort by level and match score
        career_path = []
        for job in qualified_jobs:
            job['level_rank'] = level_order.get(job['level'], 0)
            career_path.append(job)
        
        # Sort by level rank, then by match score
        career_path.sort(key=lambda x: (x['level_rank'], -x['match_score']))
        
        return career_path[:max_steps]
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all job positions in the graph"""
        if not self.graph:
            return []
        
        jobs = []
        for node_id in self.graph.nodes():
            if self.graph.nodes[node_id].get('node_type') == 'job':
                job_data = self.graph.nodes[node_id]
                
                # Count qualified candidates
                qualified_count = sum(
                    1 for pred in self.graph.predecessors(node_id)
                    if self.graph.nodes[pred].get('node_type') == 'employee'
                    and self.graph.get_edge_data(pred, node_id, {}).get('relationship') == 'QUALIFIED_FOR'
                )
                
                jobs.append({
                    'job_id': node_id,
                    'job_title': job_data.get('job_title', 'Unknown'),
                    'department': job_data.get('department', 'Unknown'),
                    'level': job_data.get('level', 'Unknown'),
                    'min_performance': job_data.get('min_performance', 0),
                    'min_behavior': job_data.get('min_behavior', 0),
                    'min_psychological': job_data.get('min_psychological', 0),
                    'min_leadership': job_data.get('min_leadership', 0),
                    'qualified_candidates': qualified_count
                })
        
        return jobs
    
    def get_employee_profile(self, employee_id: str) -> Optional[Dict]:
        """
        Get complete employee profile with 8-dimensional scores
        
        Args:
            employee_id: Employee identifier
            
        Returns:
            Dictionary with complete profile
        """
        if not self.graph or employee_id not in self.graph.nodes():
            return None
        
        emp_data = self.graph.nodes[employee_id]
        
        if emp_data.get('node_type') != 'employee':
            return None
        
        # Get employee skills
        skills = []
        for neighbor in self.graph.neighbors(employee_id):
            if self.graph.nodes[neighbor].get('node_type') == 'skill':
                skill_edge = self.graph.get_edge_data(employee_id, neighbor)
                if skill_edge and skill_edge.get('relationship') == 'HAS_SKILL':
                    skills.append({
                        'skill_name': self.graph.nodes[neighbor].get('skill_name', 'Unknown'),
                        'category': self.graph.nodes[neighbor].get('category', 'Unknown'),
                        'proficiency': skill_edge.get('proficiency', 0)
                    })
        
        # 8-dimensional profile for spider chart
        profile = {
            'employee_id': employee_id,
            'name': emp_data.get('name', 'Unknown'),
            'tenure_years': emp_data.get('tenure_years', 0),
            'dimensions': {
                'Performance Excellence': emp_data.get('performance_score', 0),
                'Behavioral Competency': emp_data.get('behavior_avg', 0),
                'Psychological Readiness': emp_data.get('psychological_score', 0),
                'Drive & Motivation': emp_data.get('drive_score', 0),
                'Mental Strength': emp_data.get('mental_strength_score', 0),
                'Adaptability': emp_data.get('adaptability_score', 0),
                'Collaboration': emp_data.get('collaboration_score', 0),
                'Leadership Potential': emp_data.get('leadership_potential', 0)
            },
            'holistic_score': emp_data.get('holistic_score', 0),
            'has_promotion': emp_data.get('has_promotion', 0),
            'skills': skills,
            'qualified_jobs_count': len(self.get_qualified_jobs(employee_id))
        }
        
        return profile
    
    def search_employees(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search employees by name
        
        Args:
            query: Search query (name)
            limit: Maximum results to return
            
        Returns:
            List of matching employees
        """
        if not self.graph:
            return []
        
        results = []
        query_lower = query.lower()
        
        for node_id in self.graph.nodes():
            if self.graph.nodes[node_id].get('node_type') == 'employee':
                name = self.graph.nodes[node_id].get('name', '')
                if query_lower in name.lower():
                    emp_data = self.graph.nodes[node_id]
                    results.append({
                        'employee_id': node_id,
                        'name': name,
                        'performance_score': emp_data.get('performance_score', 0),
                        'behavior_avg': emp_data.get('behavior_avg', 0),
                        'psychological_score': emp_data.get('psychological_score', 0),
                        'holistic_score': emp_data.get('holistic_score', 0),
                        'tenure_years': emp_data.get('tenure_years', 0)
                    })
                    
                    if len(results) >= limit:
                        break
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get Knowledge Graph statistics"""
        if not self.graph:
            return {}
        
        stats = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'employees': sum(1 for n in self.graph.nodes() if self.graph.nodes[n].get('node_type') == 'employee'),
            'jobs': sum(1 for n in self.graph.nodes() if self.graph.nodes[n].get('node_type') == 'job'),
            'skills': sum(1 for n in self.graph.nodes() if self.graph.nodes[n].get('node_type') == 'skill'),
            'departments': sum(1 for n in self.graph.nodes() if self.graph.nodes[n].get('node_type') == 'department'),
            'qualified_matches': sum(
                1 for u, v in self.graph.edges()
                if self.graph.get_edge_data(u, v).get('relationship') == 'QUALIFIED_FOR'
            )
        }
        
        return stats


# Singleton instance
_job_matching_service = None

def get_job_matching_service() -> JobMatchingService:
    """Get or create JobMatchingService singleton"""
    global _job_matching_service
    if _job_matching_service is None:
        _job_matching_service = JobMatchingService()
    return _job_matching_service
