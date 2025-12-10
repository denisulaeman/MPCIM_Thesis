"""
AI Predictor Utilities for Streamlit App
Simplified version for easy integration
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple
import streamlit as st


def predict_with_confidence(model, scaler, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Predict with confidence scores
    
    Returns:
        predictions, probabilities, confidence_scores
    """
    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)[:, 1]
    
    # Confidence: distance from 0.5, scaled to 0-1
    confidence = np.abs(probabilities - 0.5) * 2
    
    return predictions, probabilities, confidence


def get_feature_contributions(model, X: pd.DataFrame, idx: int) -> pd.DataFrame:
    """Get top contributing features for a prediction"""
    feature_importance = model.feature_importances_
    feature_values = X.iloc[idx].values
    
    # Simple contribution: importance * normalized value
    contributions = feature_importance * np.abs(feature_values) / (np.abs(feature_values).sum() + 1e-10)
    
    contrib_df = pd.DataFrame({
        'feature': X.columns,
        'value': feature_values,
        'importance': feature_importance,
        'contribution': contributions
    }).sort_values('contribution', ascending=False)
    
    return contrib_df


def find_similar_candidates(scaler, X: pd.DataFrame, idx: int, 
                           df_full: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Find similar candidates using cosine similarity"""
    X_scaled = scaler.transform(X)
    
    target_features = X_scaled[idx].reshape(1, -1)
    similarities = cosine_similarity(target_features, X_scaled)[0]
    
    # Get top N similar (excluding self)
    similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
    
    similar_df = df_full.iloc[similar_indices].copy()
    similar_df['similarity_score'] = similarities[similar_indices]
    
    return similar_df


def generate_ai_recommendations(feature_contrib: pd.DataFrame, 
                               current_prob: float) -> List[Dict]:
    """Generate AI-powered recommendations"""
    recommendations = []
    
    # Recommendation templates
    rec_templates = {
        'tenure_years': {
            'icon': '⏱️',
            'low': 'Gain more experience in current role',
            'high': 'Leverage extensive experience to mentor others',
            'action': 'Continue building track record'
        },
        'performance_score': {
            'icon': '📊',
            'low': 'Focus on improving performance metrics',
            'high': 'Maintain excellent performance standards',
            'action': 'Set and achieve measurable goals'
        },
        'psychological_score': {
            'icon': '🧠',
            'low': 'Develop psychological readiness through training',
            'high': 'Leverage strong mental readiness',
            'action': 'Participate in leadership programs'
        },
        'drive_score': {
            'icon': '🔥',
            'low': 'Increase motivation and career ambition',
            'high': 'Channel high drive into strategic initiatives',
            'action': 'Set clear career development goals'
        },
        'leadership_potential': {
            'icon': '👑',
            'low': 'Develop leadership skills through workshops',
            'high': 'Demonstrate leadership in projects',
            'action': 'Seek leadership opportunities'
        },
        'adaptability_score': {
            'icon': '🔄',
            'low': 'Improve flexibility and change management',
            'high': 'Lead change initiatives',
            'action': 'Take on diverse assignments'
        },
        'mental_strength_score': {
            'icon': '💪',
            'low': 'Build resilience and stress management',
            'high': 'Handle high-pressure situations',
            'action': 'Practice stress management techniques'
        },
        'collaboration_score': {
            'icon': '🤝',
            'low': 'Enhance teamwork and interpersonal skills',
            'high': 'Foster collaborative environment',
            'action': 'Lead cross-functional teams'
        }
    }
    
    # Get top 5 features
    top_features = feature_contrib.head(5)
    
    for _, row in top_features.iterrows():
        feature = row['feature']
        value = row['value']
        contribution = row['contribution']
        
        if feature in rec_templates:
            template = rec_templates[feature]
            level = 'high' if value > 0 else 'low'
            
            recommendations.append({
                'icon': template['icon'],
                'feature': feature.replace('_', ' ').title(),
                'text': template[level],
                'action': template['action'],
                'priority': contribution,
                'impact': 'High' if contribution > 0.1 else 'Medium' if contribution > 0.05 else 'Low'
            })
    
    return recommendations


def calculate_readiness_scores(row: pd.Series) -> Dict:
    """Calculate comprehensive readiness scores"""
    
    # Get scores (normalized to 0-1)
    performance = row.get('performance_score', 70) / 100
    behavior = row.get('behavior_avg', 70) / 100
    psychological = row.get('psychological_score', 70) / 100
    leadership = row.get('leadership_potential', 70) / 100
    
    # Calculate weighted overall readiness
    overall = (
        performance * 0.30 +
        behavior * 0.25 +
        psychological * 0.25 +
        leadership * 0.20
    )
    
    # Get readiness level
    if overall >= 0.85:
        level = "🌟 Exceptional - Ready Now"
        color = "green"
    elif overall >= 0.75:
        level = "✅ High - Ready Soon"
        color = "blue"
    elif overall >= 0.65:
        level = "⚠️ Moderate - Needs Development"
        color = "orange"
    elif overall >= 0.50:
        level = "❌ Low - Significant Development Needed"
        color = "red"
    else:
        level = "🚫 Not Ready - Extensive Development Required"
        color = "darkred"
    
    return {
        'overall': overall,
        'performance': performance,
        'behavior': behavior,
        'psychological': psychological,
        'leadership': leadership,
        'level': level,
        'color': color
    }


def generate_natural_language_explanation(row: pd.Series, 
                                         probability: float,
                                         feature_contrib: pd.DataFrame) -> str:
    """Generate natural language explanation"""
    
    # Start with probability assessment
    if probability >= 0.8:
        intro = f"🌟 **Exceptional Candidate** ({probability:.1%} promotion probability)"
        assessment = "This candidate demonstrates outstanding readiness for promotion with excellent qualifications across all dimensions."
    elif probability >= 0.7:
        intro = f"✅ **Strong Candidate** ({probability:.1%} promotion probability)"
        assessment = "This candidate shows strong potential for promotion with solid performance in key areas."
    elif probability >= 0.6:
        intro = f"⚠️ **Good Candidate** ({probability:.1%} promotion probability)"
        assessment = "This candidate has good qualifications but may benefit from targeted development in specific areas."
    elif probability >= 0.5:
        intro = f"💡 **Developing Candidate** ({probability:.1%} promotion probability)"
        assessment = "This candidate shows potential but requires focused development before promotion readiness."
    else:
        intro = f"📋 **Early-Stage Candidate** ({probability:.1%} promotion probability)"
        assessment = "This candidate needs significant development across multiple dimensions before being promotion-ready."
    
    # Add top contributing factors
    top_3 = feature_contrib.head(3)
    factors = "\n\n**Key Contributing Factors:**\n"
    
    for idx, (_, feat_row) in enumerate(top_3.iterrows(), 1):
        feature_name = feat_row['feature'].replace('_', ' ').title()
        contribution = feat_row['contribution'] * 100
        factors += f"{idx}. {feature_name} ({contribution:.1f}% contribution)\n"
    
    return intro + "\n\n" + assessment + factors


def predict_what_if_scenario(model, scaler, X: pd.DataFrame, 
                             feature: str, new_value: float) -> Tuple[float, float, float]:
    """
    Predict what-if scenario
    
    Returns:
        original_prob, new_prob, change
    """
    # Original prediction
    X_scaled = scaler.transform(X)
    original_prob = model.predict_proba(X_scaled)[0, 1]
    
    # Modified prediction
    X_modified = X.copy()
    X_modified[feature] = new_value
    X_modified_scaled = scaler.transform(X_modified)
    new_prob = model.predict_proba(X_modified_scaled)[0, 1]
    
    change = new_prob - original_prob
    
    return original_prob, new_prob, change


def get_confidence_level(confidence: float) -> Tuple[str, str]:
    """Get confidence level label and color"""
    if confidence >= 0.9:
        return "Very High", "green"
    elif confidence >= 0.75:
        return "High", "blue"
    elif confidence >= 0.6:
        return "Moderate", "orange"
    else:
        return "Low", "red"


def format_feature_name(feature: str) -> str:
    """Format feature name for display"""
    name_map = {
        'tenure_years': '⏱️ Tenure (Years)',
        'performance_score': '📊 Performance Score',
        'behavior_avg': '🎯 Behavior Score',
        'psychological_score': '🧠 Psychological Score',
        'drive_score': '🔥 Drive & Motivation',
        'mental_strength_score': '💪 Mental Strength',
        'adaptability_score': '🔄 Adaptability',
        'collaboration_score': '🤝 Collaboration',
        'leadership_potential': '👑 Leadership Potential',
        'perf_beh_ratio': '⚖️ Performance/Behavior Ratio',
        'score_difference': '📏 Score Balance',
        'combined_score': '📈 Combined Score'
    }
    
    return name_map.get(feature, feature.replace('_', ' ').title())
