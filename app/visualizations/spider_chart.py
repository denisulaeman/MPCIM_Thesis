"""
Spider Chart (Radar Chart) Visualization
=========================================
8-dimensional employee profile visualization
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import numpy as np

def create_spider_chart(
    profile: Dict,
    job_requirements: Optional[Dict] = None,
    title: Optional[str] = None,
    show_job_overlay: bool = False
) -> go.Figure:
    """
    Create spider/radar chart for employee profile
    
    Args:
        profile: Employee profile with 'dimensions' dict
        job_requirements: Optional job requirements to overlay
        title: Chart title
        show_job_overlay: Whether to show job requirements overlay
        
    Returns:
        Plotly Figure object
    """
    
    # 8 dimensions
    dimensions = [
        'Performance<br>Excellence',
        'Behavioral<br>Competency',
        'Psychological<br>Readiness',
        'Drive &<br>Motivation',
        'Mental<br>Strength',
        'Adaptability',
        'Collaboration',
        'Leadership<br>Potential'
    ]
    
    # Get values from profile
    values = [
        profile['dimensions'].get('Performance Excellence', 0),
        profile['dimensions'].get('Behavioral Competency', 0),
        profile['dimensions'].get('Psychological Readiness', 0),
        profile['dimensions'].get('Drive & Motivation', 0),
        profile['dimensions'].get('Mental Strength', 0),
        profile['dimensions'].get('Adaptability', 0),
        profile['dimensions'].get('Collaboration', 0),
        profile['dimensions'].get('Leadership Potential', 0)
    ]
    
    # Create figure
    fig = go.Figure()
    
    # Add employee profile trace
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=dimensions,
        fill='toself',
        name=profile.get('name', 'Employee'),
        line=dict(color='#667eea', width=2),
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    # Add job requirements overlay if provided
    if show_job_overlay and job_requirements:
        job_values = [
            job_requirements.get('min_performance', 0),
            job_requirements.get('min_behavior', 0),
            job_requirements.get('min_psychological', 0),
            job_requirements.get('min_leadership', 0),  # Use for Drive
            job_requirements.get('min_leadership', 0),  # Use for Mental Strength
            job_requirements.get('min_psychological', 0),  # Use for Adaptability
            job_requirements.get('min_behavior', 0),  # Use for Collaboration
            job_requirements.get('min_leadership', 0)
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=job_values,
            theta=dimensions,
            fill='toself',
            name=job_requirements.get('job_title', 'Job Requirement'),
            line=dict(color='#f093fb', width=2, dash='dash'),
            fillcolor='rgba(240, 147, 251, 0.2)'
        ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(0,0,0,0.1)'
            )
        ),
        showlegend=True,
        title=dict(
            text=title or f"Profile: {profile.get('name', 'Employee')}",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#2d3748')
        ),
        font=dict(size=12),
        height=500,
        margin=dict(l=80, r=80, t=100, b=80),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig


def create_comparison_spider_chart(
    profiles: List[Dict],
    title: str = "Employee Comparison"
) -> go.Figure:
    """
    Create spider chart comparing multiple employees
    
    Args:
        profiles: List of employee profiles
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    
    dimensions = [
        'Performance<br>Excellence',
        'Behavioral<br>Competency',
        'Psychological<br>Readiness',
        'Drive &<br>Motivation',
        'Mental<br>Strength',
        'Adaptability',
        'Collaboration',
        'Leadership<br>Potential'
    ]
    
    # Color palette
    colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a']
    
    fig = go.Figure()
    
    for idx, profile in enumerate(profiles[:5]):  # Max 5 employees
        values = [
            profile['dimensions'].get('Performance Excellence', 0),
            profile['dimensions'].get('Behavioral Competency', 0),
            profile['dimensions'].get('Psychological Readiness', 0),
            profile['dimensions'].get('Drive & Motivation', 0),
            profile['dimensions'].get('Mental Strength', 0),
            profile['dimensions'].get('Adaptability', 0),
            profile['dimensions'].get('Collaboration', 0),
            profile['dimensions'].get('Leadership Potential', 0)
        ]
        
        color = colors[idx % len(colors)]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=dimensions,
            fill='toself',
            name=profile.get('name', f'Employee {idx+1}'),
            line=dict(color=color, width=2),
            fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2)'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20
            )
        ),
        showlegend=True,
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#2d3748')
        ),
        height=600,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig


def create_skill_proficiency_chart(skills: List[Dict], title: str = "Skill Proficiency") -> go.Figure:
    """
    Create horizontal bar chart for skill proficiency
    
    Args:
        skills: List of skill dictionaries with 'skill_name' and 'proficiency'
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    
    if not skills:
        # Return empty figure
        fig = go.Figure()
        fig.add_annotation(
            text="No skills data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='gray')
        )
        return fig
    
    # Sort by proficiency
    skills_sorted = sorted(skills, key=lambda x: x.get('proficiency', 0), reverse=True)
    
    # Take top 15 skills
    top_skills = skills_sorted[:15]
    
    skill_names = [s.get('skill_name', 'Unknown') for s in top_skills]
    proficiencies = [s.get('proficiency', 0) for s in top_skills]
    categories = [s.get('category', 'Unknown') for s in top_skills]
    
    # Color by category
    category_colors = {
        'Technical': '#667eea',
        'Soft': '#4facfe',
        'Leadership': '#f093fb',
        'Domain-HR': '#43e97b',
        'Domain-Finance': '#fa709a',
        'Domain-Operations': '#feca57'
    }
    
    colors = [category_colors.get(cat, '#718096') for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=skill_names,
        x=proficiencies,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        text=[f"{p}/5" for p in proficiencies],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Proficiency: %{x}/5<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=16, color='#2d3748')
        ),
        xaxis=dict(
            title="Proficiency Level",
            range=[0, 5],
            tickmode='linear',
            tick0=0,
            dtick=1,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            title="",
            autorange='reversed'
        ),
        height=max(400, len(top_skills) * 30),
        margin=dict(l=150, r=50, t=80, b=50),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False
    )
    
    return fig


def get_strength_weakness_analysis(profile: Dict) -> Dict:
    """
    Analyze employee strengths and weaknesses based on profile
    
    Args:
        profile: Employee profile with dimensions
        
    Returns:
        Dictionary with strengths and weaknesses
    """
    
    dimensions_dict = profile.get('dimensions', {})
    
    # Sort dimensions by score
    sorted_dims = sorted(dimensions_dict.items(), key=lambda x: x[1], reverse=True)
    
    # Top 3 are strengths, bottom 3 are weaknesses
    strengths = [
        {'dimension': dim, 'score': score}
        for dim, score in sorted_dims[:3]
        if score >= 70
    ]
    
    weaknesses = [
        {'dimension': dim, 'score': score}
        for dim, score in sorted_dims[-3:]
        if score < 75
    ]
    
    # Overall assessment
    avg_score = np.mean(list(dimensions_dict.values()))
    
    if avg_score >= 85:
        overall = "Excellent - Well-rounded profile"
    elif avg_score >= 75:
        overall = "Good - Strong overall performance"
    elif avg_score >= 65:
        overall = "Fair - Room for improvement"
    else:
        overall = "Needs Development - Focus on key areas"
    
    # Balance check (low variance = balanced)
    variance = np.var(list(dimensions_dict.values()))
    
    if variance < 50:
        balance = "Well-balanced profile"
    elif variance < 150:
        balance = "Moderately balanced"
    else:
        balance = "Unbalanced - Significant gaps between dimensions"
    
    return {
        'strengths': strengths,
        'weaknesses': weaknesses,
        'overall_assessment': overall,
        'balance_assessment': balance,
        'average_score': round(avg_score, 1),
        'variance': round(variance, 1)
    }
