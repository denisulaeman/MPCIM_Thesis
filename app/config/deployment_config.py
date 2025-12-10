"""
Deployment Configuration for MPCIM App
Generated: December 8, 2025
"""

# Model Configuration
DEFAULT_MODEL = "xgboost"  # Best performing model (100% accuracy)
AVAILABLE_MODELS = ['xgboost', 'random_forest', 'neural_network']

# Data Configuration
DATA_SOURCE = "integrated_full_dataset.csv"
FEATURE_COUNT = 23  # With psychological features

# Feature Configuration
PSYCHOLOGICAL_FEATURES_ENABLED = True

# Model Performance (from training)
MODEL_PERFORMANCE = {
    "xgboost": {
        "accuracy": 1.00,
        "precision": 1.00,
        "recall": 1.00,
        "f1_score": 1.00
    },
    "random_forest": {
        "accuracy": 1.00,
        "precision": 1.00,
        "recall": 1.00,
        "f1_score": 1.00
    },
    "neural_network": {
        "accuracy": 1.00,
        "precision": 1.00,
        "recall": 1.00,
        "f1_score": 1.00
    }
}

# UI Configuration
SHOW_PSYCHOLOGICAL_SCORES = True
SHOW_LEADERSHIP_POTENTIAL = True
SHOW_HOLISTIC_ASSESSMENT = True

# Feature Importance (from XGBoost)
TOP_FEATURES = [
    "tenure_category_encoded",
    "tenure_years",
    "holistic_score",
    "is_permanent_encoded",
    "behavior_avg",
    "performance_score",
    "psychological_score",
    "combined_score",
    "perf_beh_ratio",
    "behavioral_level_encoded"
]

# Psychological Feature Contribution
QA_CONTRIBUTION = {
    "xgboost": 0.1728,  # 17.28%
    "random_forest": 0.2996  # 29.96%
}
