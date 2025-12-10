"""
Advanced AI Candidate Predictor
Enhanced with confidence scores, similarity analysis, and recommendations
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
from typing import Dict, List, Tuple

class AICandidatePredictor:
    """Advanced AI-powered candidate prediction system"""
    
    def __init__(self, model_path: str = None, scaler_path: str = None):
        """Initialize AI predictor"""
        self.model = None
        self.scaler = None
        self.feature_names = None
        
        if model_path and scaler_path:
            self.load_model(model_path, scaler_path)
    
    def load_model(self, model_path: str, scaler_path: str):
        """Load trained model and scaler"""
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        
        # Get feature names from model
        if hasattr(self.model, 'feature_names_in_'):
            self.feature_names = self.model.feature_names_in_
    
    def predict_with_confidence(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Predict promotion probability with confidence scores
        
        Returns:
            predictions: Binary predictions (0/1)
            probabilities: Promotion probabilities (0-1)
            confidence: Confidence scores (0-1)
        """
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get predictions
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)[:, 1]
        
        # Calculate confidence based on probability distance from 0.5
        # High confidence when probability is close to 0 or 1
        confidence = np.abs(probabilities - 0.5) * 2
        
        return predictions, probabilities, confidence
    
    def get_feature_contributions(self, X: pd.DataFrame, idx: int) -> pd.DataFrame:
        """
        Get feature contributions for a specific prediction
        Uses SHAP-like approach with tree feature importances
        """
        X_scaled = self.scaler.transform(X)
        
        # Get feature importances from model
        feature_importance = self.model.feature_importances_
        
        # Get feature values for this instance
        feature_values = X_scaled[idx]
        
        # Calculate contributions (simplified SHAP-like)
        contributions = feature_importance * feature_values
        
        # Normalize to sum to 1
        contributions = np.abs(contributions) / np.sum(np.abs(contributions))
        
        # Create DataFrame
        contrib_df = pd.DataFrame({
            'feature': X.columns,
            'value': X.iloc[idx].values,
            'contribution': contributions
        }).sort_values('contribution', ascending=False)
        
        return contrib_df
    
    def find_similar_candidates(self, X: pd.DataFrame, idx: int, top_n: int = 5) -> pd.DataFrame:
        """
        Find similar candidates using cosine similarity
        
        Args:
            X: Feature DataFrame
            idx: Index of target candidate
            top_n: Number of similar candidates to return
        
        Returns:
            DataFrame with similar candidates and similarity scores
        """
        X_scaled = self.scaler.transform(X)
        
        # Calculate cosine similarity
        target_features = X_scaled[idx].reshape(1, -1)
        similarities = cosine_similarity(target_features, X_scaled)[0]
        
        # Get top N similar (excluding self)
        similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
        
        similar_df = pd.DataFrame({
            'index': similar_indices,
            'similarity': similarities[similar_indices]
        })
        
        return similar_df
    
    def generate_recommendations(self, X: pd.DataFrame, y_pred: float, 
                                 feature_contrib: pd.DataFrame) -> List[Dict]:
        """
        Generate AI-powered recommendations for improvement
        
        Args:
            X: Feature DataFrame (single row)
            y_pred: Predicted promotion probability
            feature_contrib: Feature contributions DataFrame
        
        Returns:
            List of recommendations with priority and impact
        """
        recommendations = []
        
        # Get top negative contributors (areas for improvement)
        top_features = feature_contrib.head(10)
        
        for _, row in top_features.iterrows():
            feature = row['feature']
            value = row['value']
            contribution = row['contribution']
            
            # Generate recommendation based on feature
            rec = self._generate_feature_recommendation(feature, value, contribution)
            if rec:
                recommendations.append(rec)
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return recommendations
    
    def _generate_feature_recommendation(self, feature: str, value: float, 
                                        contribution: float) -> Dict:
        """Generate specific recommendation for a feature"""
        
        # Define recommendation templates
        recommendations_map = {
            'tenure_years': {
                'low': {
                    'text': 'Gain more experience in current role',
                    'action': 'Continue building expertise and track record',
                    'timeline': '6-12 months',
                    'priority': 0.8
                },
                'high': {
                    'text': 'Leverage extensive experience',
                    'action': 'Mentor junior staff and share knowledge',
                    'timeline': 'Ongoing',
                    'priority': 0.6
                }
            },
            'performance_score': {
                'low': {
                    'text': 'Improve performance metrics',
                    'action': 'Set clear goals and track progress weekly',
                    'timeline': '3-6 months',
                    'priority': 0.9
                },
                'high': {
                    'text': 'Maintain excellent performance',
                    'action': 'Continue current practices and set stretch goals',
                    'timeline': 'Ongoing',
                    'priority': 0.5
                }
            },
            'psychological_score': {
                'low': {
                    'text': 'Develop psychological readiness',
                    'action': 'Participate in leadership development programs',
                    'timeline': '3-6 months',
                    'priority': 0.85
                },
                'high': {
                    'text': 'Leverage strong psychological profile',
                    'action': 'Take on challenging projects',
                    'timeline': 'Immediate',
                    'priority': 0.7
                }
            },
            'drive_score': {
                'low': {
                    'text': 'Increase motivation and ambition',
                    'action': 'Identify career goals and create action plan',
                    'timeline': '1-3 months',
                    'priority': 0.8
                },
                'high': {
                    'text': 'Channel high drive effectively',
                    'action': 'Lead strategic initiatives',
                    'timeline': 'Immediate',
                    'priority': 0.6
                }
            },
            'leadership_potential': {
                'low': {
                    'text': 'Develop leadership skills',
                    'action': 'Attend leadership workshops and seek mentorship',
                    'timeline': '6-12 months',
                    'priority': 0.9
                },
                'high': {
                    'text': 'Demonstrate leadership capabilities',
                    'action': 'Lead cross-functional projects',
                    'timeline': 'Immediate',
                    'priority': 0.7
                }
            },
            'adaptability_score': {
                'low': {
                    'text': 'Improve adaptability',
                    'action': 'Take on diverse assignments outside comfort zone',
                    'timeline': '3-6 months',
                    'priority': 0.75
                },
                'high': {
                    'text': 'Leverage adaptability',
                    'action': 'Lead change management initiatives',
                    'timeline': 'Immediate',
                    'priority': 0.6
                }
            }
        }
        
        # Determine if value is low or high (simplified)
        level = 'low' if value < 0 else 'high'
        
        # Get recommendation template
        if feature in recommendations_map:
            template = recommendations_map[feature][level]
            
            return {
                'feature': feature,
                'text': template['text'],
                'action': template['action'],
                'timeline': template['timeline'],
                'priority': template['priority'] * contribution,  # Weight by contribution
                'impact': 'High' if contribution > 0.1 else 'Medium' if contribution > 0.05 else 'Low'
            }
        
        return None
    
    def predict_what_if(self, X: pd.DataFrame, feature: str, 
                       new_value: float) -> Tuple[float, float]:
        """
        Predict what-if scenario: what if feature changes to new_value?
        
        Args:
            X: Feature DataFrame (single row)
            feature: Feature to change
            new_value: New value for feature
        
        Returns:
            original_prob: Original promotion probability
            new_prob: New promotion probability after change
        """
        # Original prediction
        X_scaled = self.scaler.transform(X)
        original_prob = self.model.predict_proba(X_scaled)[0, 1]
        
        # Modified prediction
        X_modified = X.copy()
        X_modified[feature] = new_value
        X_modified_scaled = self.scaler.transform(X_modified)
        new_prob = self.model.predict_proba(X_modified_scaled)[0, 1]
        
        return original_prob, new_prob
    
    def generate_natural_language_explanation(self, X: pd.DataFrame, 
                                             y_pred: float,
                                             feature_contrib: pd.DataFrame) -> str:
        """
        Generate natural language explanation of prediction
        
        Args:
            X: Feature DataFrame (single row)
            y_pred: Predicted promotion probability
            feature_contrib: Feature contributions DataFrame
        
        Returns:
            Natural language explanation string
        """
        # Get top 3 contributing features
        top_features = feature_contrib.head(3)
        
        # Start explanation
        if y_pred >= 0.7:
            explanation = f"This candidate has a **high promotion probability ({y_pred:.1%})**. "
        elif y_pred >= 0.5:
            explanation = f"This candidate has a **moderate promotion probability ({y_pred:.1%})**. "
        else:
            explanation = f"This candidate has a **low promotion probability ({y_pred:.1%})**. "
        
        # Add key factors
        explanation += "Key factors contributing to this assessment:\n\n"
        
        for idx, (_, row) in enumerate(top_features.iterrows(), 1):
            feature = row['feature']
            value = row['value']
            contribution = row['contribution']
            
            # Format feature name
            feature_name = feature.replace('_', ' ').title()
            
            explanation += f"{idx}. **{feature_name}** (contributes {contribution*100:.1f}%)\n"
        
        # Add overall assessment
        explanation += f"\n**Overall Assessment**: "
        
        if y_pred >= 0.8:
            explanation += "Strong candidate with excellent readiness for promotion. "
        elif y_pred >= 0.6:
            explanation += "Good candidate with solid qualifications. "
        elif y_pred >= 0.4:
            explanation += "Developing candidate with potential for growth. "
        else:
            explanation += "Candidate needs significant development before promotion readiness. "
        
        return explanation
    
    def calculate_promotion_readiness_score(self, X: pd.DataFrame) -> Dict:
        """
        Calculate comprehensive promotion readiness score
        
        Returns:
            Dictionary with readiness scores across dimensions
        """
        # Get predictions
        _, probabilities, confidence = self.predict_with_confidence(X)
        
        # Calculate dimension scores
        performance_score = X['performance_score'].values[0] / 100
        behavior_score = X['behavior_avg'].values[0] / 100
        
        if 'psychological_score' in X.columns:
            psychological_score = X['psychological_score'].values[0] / 100
        else:
            psychological_score = 0.7  # Default
        
        if 'leadership_potential' in X.columns:
            leadership_score = X['leadership_potential'].values[0] / 100
        else:
            leadership_score = 0.7  # Default
        
        # Calculate overall readiness
        overall_readiness = (
            performance_score * 0.3 +
            behavior_score * 0.25 +
            psychological_score * 0.25 +
            leadership_score * 0.2
        )
        
        return {
            'overall_readiness': overall_readiness,
            'promotion_probability': probabilities[0],
            'confidence': confidence[0],
            'performance_readiness': performance_score,
            'behavioral_readiness': behavior_score,
            'psychological_readiness': psychological_score,
            'leadership_readiness': leadership_score,
            'readiness_level': self._get_readiness_level(overall_readiness)
        }
    
    def _get_readiness_level(self, score: float) -> str:
        """Get readiness level label"""
        if score >= 0.85:
            return "Exceptional - Ready Now"
        elif score >= 0.75:
            return "High - Ready Soon"
        elif score >= 0.65:
            return "Moderate - Needs Development"
        elif score >= 0.50:
            return "Low - Significant Development Needed"
        else:
            return "Not Ready - Extensive Development Required"


# Example usage
if __name__ == "__main__":
    print("AI Candidate Predictor - Advanced Features")
    print("=" * 80)
    print()
    print("Features:")
    print("1. ✅ Prediction with confidence scores")
    print("2. ✅ Feature contribution analysis")
    print("3. ✅ Similar candidate finding")
    print("4. ✅ AI-powered recommendations")
    print("5. ✅ What-if scenario analysis")
    print("6. ✅ Natural language explanations")
    print("7. ✅ Comprehensive readiness scoring")
    print()
    print("Ready for integration into Streamlit app!")
