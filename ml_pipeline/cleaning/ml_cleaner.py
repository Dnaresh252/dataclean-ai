"""
ML-Powered Data Cleaner
========================

Purpose: Use ML models to detect problems, then apply cleaning operations.

Flow:
1. Load ML models
2. Analyze DataFrame (detect problems)
3. Recommend cleaning operations
4. Apply cleaning operations
5. Return cleaned data + report
"""

import pandas as pd
import joblib
import json
from pathlib import Path
from typing import Dict, List, Any
import logging
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from data.feature_extractor import ColumnFeatureExtractor
from cleaning.cleaner import DataCleaner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLDataCleaner:
    """
    ML-powered data cleaning system.
    
    Uses trained models to detect problems, then applies appropriate fixes.
    """
    
    def __init__(self, models_dir: str = None):
        """
        Initialize with trained ML models.
        
        Args:
            models_dir: Path to directory containing trained models
        """
        if models_dir is None:
            # Default to models directory
            models_dir = Path(__file__).parent.parent.parent / 'models'
        
        self.models_dir = Path(models_dir)
        self.models = {}
        self.metadata = {}
        
        # Load models
        self._load_models()
        
        logger.info("MLDataCleaner initialized with trained models")
    
    def _load_models(self):
        """Load all trained ML models."""
        try:
            # Load metadata
            metadata_file = self.models_dir / 'classifier_metadata.json'
            with open(metadata_file, 'r') as f:
                self.metadata = json.load(f)
            
            # Load each model
            problem_types = ['has_duplicates', 'has_missing', 'has_outliers', 
                           'has_format_issue', 'has_type_issue']
            
            for ptype in problem_types:
                model_file = self.models_dir / f'{ptype}_classifier.joblib'
                if model_file.exists():
                    self.models[ptype] = joblib.load(model_file)
                    logger.info(f"Loaded model: {ptype}")
                else:
                    logger.warning(f"Model not found: {ptype}")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze DataFrame and detect problems using ML models.
        
        Args:
            df: pandas DataFrame to analyze
            
        Returns:
            Dict with analysis results per column
        """
        analysis = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': {},
            'problems_detected': []
        }
        
        for col in df.columns:
            try:
                # Extract features from column
                extractor = ColumnFeatureExtractor(df[col], col)
                features = extractor.extract_all_features()
                
                # Convert to DataFrame for model prediction
                feature_row = pd.DataFrame([features])
                feature_row = feature_row[self.metadata['feature_columns']]
                
                # Predict problems
                column_problems = {}
                for ptype, model in self.models.items():
                    try:
                        # Get probability
                        proba = model.predict_proba(feature_row)[0]
                        
                        if len(proba) == 2:
                            prob = float(proba[1])  # Probability of having problem
                        else:
                            prob = 0.0
                        
                        column_problems[ptype] = {
                            'probability': prob,
                            'has_problem': prob > 0.5
                        }
                        
                        # Add to overall problems list if detected
                        if prob > 0.5:
                            analysis['problems_detected'].append({
                                'column': col,
                                'problem_type': ptype,
                                'probability': prob
                            })
                            
                    except Exception as e:
                        logger.warning(f"Error predicting {ptype} for {col}: {e}")
                        column_problems[ptype] = {
                            'probability': 0.0,
                            'has_problem': False
                        }
                
                # Store column analysis
                analysis['columns'][col] = {
                    'problems': column_problems,
                    'missing_percentage': float(features.get('missing_percentage', 0)),
                    'duplicate_percentage': float(features.get('duplicate_percentage', 0)),
                    'outlier_percentage': float(features.get('outlier_percentage', 0)),
                    'format_consistency_score': float(features.get('format_consistency_score', 100))
                }
                
            except Exception as e:
                logger.error(f"Error analyzing column {col}: {e}")
                analysis['columns'][col] = {
                    'error': str(e)
                }
        
        return analysis
    
    def recommend_cleaning_operations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recommended cleaning operations based on analysis.
        
        Args:
            analysis: Analysis results from analyze_dataframe()
            
        Returns:
            List of recommended operations
        """
        recommendations = []
        
        # Check for file-level duplicates
        for prob_info in analysis['problems_detected']:
            if prob_info['problem_type'] == 'has_duplicates' and prob_info['probability'] > 0.7:
                recommendations.append({
                    'operation': 'remove_duplicates',
                    'priority': 'high',
                    'reason': 'Multiple columns show high duplicate percentage',
                    'params': {'keep': 'first'}
                })
                break  # Only recommend once for file-level operation
        
        # Check column-specific problems
        for col, col_info in analysis['columns'].items():
            if 'error' in col_info:
                continue
            
            problems = col_info['problems']
            
            # Missing values
            if problems.get('has_missing', {}).get('has_problem', False):
                recommendations.append({
                    'operation': 'fill_missing_values',
                    'column': col,
                    'priority': 'medium',
                    'reason': f"Column has {col_info['missing_percentage']:.1f}% missing values",
                    'params': {'strategy': 'auto'}
                })
            
            # Outliers
            if problems.get('has_outliers', {}).get('has_problem', False):
                recommendations.append({
                    'operation': 'remove_outliers',
                    'column': col,
                    'priority': 'low',
                    'reason': f"Column has {col_info['outlier_percentage']:.1f}% outliers",
                    'params': {'method': 'iqr', 'threshold': 1.5}
                })
            
            # Format issues
            if problems.get('has_format_issue', {}).get('has_problem', False):
                recommendations.append({
                    'operation': 'standardize_format',
                    'column': col,
                    'priority': 'low',
                    'reason': f"Format consistency only {col_info['format_consistency_score']:.1f}%",
                    'params': {'target_format': 'auto'}
                })
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(key=lambda x: priority_order[x['priority']])
        
        return recommendations
    
    def clean_dataframe(self, df: pd.DataFrame, auto_apply: bool = True) -> Dict[str, Any]:
        """
        Complete cleaning workflow: analyze → recommend → clean.
        
        Args:
            df: pandas DataFrame to clean
            auto_apply: Whether to automatically apply recommended operations
            
        Returns:
            Dict with cleaned data and report
        """
        logger.info(f"Starting cleaning workflow for DataFrame: {df.shape}")
        
        # Step 1: Analyze
        analysis = self.analyze_dataframe(df)
        logger.info(f"Analysis complete: {len(analysis['problems_detected'])} problems detected")
        
        # Step 2: Get recommendations
        recommendations = self.recommend_cleaning_operations(analysis)
        logger.info(f"Generated {len(recommendations)} recommendations")
        
        # Step 3: Apply cleaning if auto_apply
        if auto_apply:
            cleaner = DataCleaner(df)
            
            for rec in recommendations:
                operation = rec['operation']
                
                try:
                    if operation == 'remove_duplicates':
                        cleaner.remove_duplicates(**rec['params'])
                        
                    elif operation == 'fill_missing_values':
                        cleaner.fill_missing_values(rec['column'], **rec['params'])
                        
                    elif operation == 'remove_outliers':
                        cleaner.remove_outliers(rec['column'], **rec['params'])
                        
                    elif operation == 'standardize_format':
                        cleaner.standardize_format(rec['column'], **rec['params'])
                        
                except Exception as e:
                    logger.error(f"Error applying {operation}: {e}")
            
            cleaned_df = cleaner.get_cleaned_data()
            summary = cleaner.get_summary()
            
        else:
            cleaned_df = df.copy()
            summary = {'note': 'auto_apply was False, no cleaning performed'}
        
        # Return complete report
        return {
            'original_shape': df.shape,
            'cleaned_shape': cleaned_df.shape,
            'analysis': analysis,
            'recommendations': recommendations,
            'summary': summary,
            'cleaned_data': cleaned_df
        }


# Example usage and testing
if __name__ == "__main__":
    # Create sample messy data
    messy_data = pd.DataFrame({
        'name': ['John Doe', 'JOHN DOE', 'Jane Smith', 'Jane Smith', 'Bob Wilson'],
        'age': [25, 25, 30, 30, 150],  # 150 is outlier
        'salary': [50000, 50000, None, 60000, 55000],
        'email': ['john@email.com', 'john@email.com', None, 'jane@email.com', 'bob@email.com']
    })
    
    print("Original Data:")
    print(messy_data)
    print("\n" + "="*60 + "\n")
    
    # Clean using ML
    ml_cleaner = MLDataCleaner()
    result = ml_cleaner.clean_dataframe(messy_data, auto_apply=True)
    
    print("Analysis Summary:")
    print(f"Problems detected: {len(result['analysis']['problems_detected'])}")
    for problem in result['analysis']['problems_detected']:
        print(f"  - {problem['column']}: {problem['problem_type']} ({problem['probability']:.1%})")
    
    print("\nRecommendations:")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"{i}. [{rec['priority'].upper()}] {rec['operation']}")
        print(f"   Reason: {rec['reason']}")
    
    print("\n" + "="*60 + "\n")
    print("Cleaned Data:")
    print(result['cleaned_data'])
    
    print("\n" + "="*60 + "\n")
    print("Summary:")
    print(json.dumps(result['summary'], indent=2, default=str))