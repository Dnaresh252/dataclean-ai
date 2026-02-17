"""
ML Service
==========

Purpose: Wrapper around ML models for use in FastAPI backend.

Handles:
- Loading ML models on startup
- Running predictions on uploaded files
- Error handling for production
"""

import pandas as pd
from pathlib import Path
import logging
import sys
from typing import Dict, Any

# Add ml_pipeline to path
ml_pipeline_path = Path(__file__).parent.parent.parent.parent / 'ml_pipeline'
sys.path.append(str(ml_pipeline_path))

from cleaning.ml_cleaner import MLDataCleaner

logger = logging.getLogger(__name__)


class MLService:
    """
    Service for ML-powered data analysis and cleaning.
    
    Singleton pattern - one instance shared across app.
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance exists (singleton)."""
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize ML models (only once)."""
        if self._initialized:
            return
        
        try:
            # Load ML models
            models_dir = Path(__file__).parent.parent.parent.parent / 'models'
            self.ml_cleaner = MLDataCleaner(models_dir=str(models_dir))
            
            self._initialized = True
            logger.info("✅ ML Service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ML Service: {e}")
            raise
    
    def analyze_file(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze uploaded DataFrame for data quality issues.
        
        Args:
            df: pandas DataFrame from uploaded file
            
        Returns:
            Analysis results with problems detected
        """
        try:
            logger.info(f"Analyzing file: {df.shape}")
            
            # Run ML analysis
            analysis = self.ml_cleaner.analyze_dataframe(df)
            
            logger.info(f"Analysis complete: {len(analysis['problems_detected'])} problems found")
            
            return {
                'success': True,
                'analysis': analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing file: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get cleaning recommendations based on analysis.
        
        Args:
            analysis: Analysis results from analyze_file()
            
        Returns:
            List of recommended cleaning operations
        """
        try:
            recommendations = self.ml_cleaner.recommend_cleaning_operations(analysis)
            
            return {
                'success': True,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def clean_file(self, df: pd.DataFrame, auto_apply: bool = True) -> Dict[str, Any]:
        """
        Complete cleaning workflow: analyze → recommend → clean.
        
        Args:
            df: pandas DataFrame to clean
            auto_apply: Whether to auto-apply recommendations
            
        Returns:
            Complete cleaning report with cleaned data
        """
        try:
            logger.info(f"Cleaning file: {df.shape}")
            
            # Run complete workflow
            result = self.ml_cleaner.clean_dataframe(df, auto_apply=auto_apply)
            
            logger.info(f"Cleaning complete: {result['original_shape']} → {result['cleaned_shape']}")
            
            return {
                'success': True,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Error cleaning file: {e}")
            return {
                'success': False,
                'error': str(e)
            }


# Global instance
ml_service = MLService()