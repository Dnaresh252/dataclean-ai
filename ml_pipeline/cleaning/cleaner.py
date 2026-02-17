"""
Data Cleaning Operations
========================

Purpose: Actually FIX data quality issues detected by ML models.

Each cleaning operation:
- Takes a pandas DataFrame
- Fixes specific problem type
- Returns cleaned DataFrame + change log
- Handles errors gracefully
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Cleans data quality issues in pandas DataFrames.
    
    Production-ready implementation with:
    - Error handling
    - Change tracking
    - Logging
    - Type hints
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize cleaner with a DataFrame.
        
        Args:
            df: pandas DataFrame to clean
        """
        self.original_df = df.copy()
        self.cleaned_df = df.copy()
        self.changes_log = []  # Track all changes made
        
        logger.info(f"DataCleaner initialized with {len(df)} rows, {len(df.columns)} columns")
    
    def remove_duplicates(self, keep: str = 'first') -> Dict[str, Any]:
        """
        Remove exact duplicate rows.
        
        Args:
            keep: Which duplicate to keep ('first', 'last', or False to remove all)
            
        Returns:
            Dict with results: {
                'rows_removed': int,
                'original_count': int,
                'cleaned_count': int
            }
        """
        try:
            original_count = len(self.cleaned_df)
            
            # Find duplicates
            duplicates = self.cleaned_df.duplicated(keep=keep)
            duplicate_count = duplicates.sum()
            
            if duplicate_count == 0:
                logger.info("No duplicates found")
                return {
                    'rows_removed': 0,
                    'original_count': original_count,
                    'cleaned_count': original_count
                }
            
            # Remove duplicates
            self.cleaned_df = self.cleaned_df[~duplicates].reset_index(drop=True)
            
            # Log changes
            change = {
                'operation': 'remove_duplicates',
                'timestamp': datetime.now().isoformat(),
                'rows_removed': int(duplicate_count),
                'original_count': original_count,
                'cleaned_count': len(self.cleaned_df)
            }
            self.changes_log.append(change)
            
            logger.info(f"Removed {duplicate_count} duplicate rows")
            
            return change
            
        except Exception as e:
            logger.error(f"Error removing duplicates: {e}")
            return {
                'error': str(e),
                'rows_removed': 0
            }
    
    def fill_missing_values(self, column: str, strategy: str = 'auto') -> Dict[str, Any]:
        """
        Fill missing values in a column.
        
        Args:
            column: Column name to fill
            strategy: How to fill ('auto', 'mean', 'median', 'mode', 'drop')
            
        Returns:
            Dict with results: {
                'values_filled': int,
                'strategy_used': str,
                'fill_value': Any
            }
        """
        try:
            if column not in self.cleaned_df.columns:
                raise ValueError(f"Column '{column}' not found")
            
            # Count missing values
            missing_count = self.cleaned_df[column].isna().sum()
            
            if missing_count == 0:
                logger.info(f"No missing values in column '{column}'")
                return {
                    'values_filled': 0,
                    'strategy_used': strategy,
                    'fill_value': None
                }
            
            # Determine fill strategy
            if strategy == 'auto':
                # Auto-detect best strategy based on data type
                if pd.api.types.is_numeric_dtype(self.cleaned_df[column]):
                    strategy = 'median'
                else:
                    strategy = 'mode'
            
            # Apply strategy
            if strategy == 'mean':
                fill_value = self.cleaned_df[column].mean()
                self.cleaned_df[column].fillna(fill_value, inplace=True)
                
            elif strategy == 'median':
                fill_value = self.cleaned_df[column].median()
                self.cleaned_df[column].fillna(fill_value, inplace=True)
                
            elif strategy == 'mode':
                fill_value = self.cleaned_df[column].mode()[0] if len(self.cleaned_df[column].mode()) > 0 else None
                if fill_value is not None:
                    self.cleaned_df[column].fillna(fill_value, inplace=True)
                    
            elif strategy == 'drop':
                self.cleaned_df = self.cleaned_df.dropna(subset=[column]).reset_index(drop=True)
                fill_value = 'dropped_rows'
            
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            # Log changes
            change = {
                'operation': 'fill_missing_values',
                'timestamp': datetime.now().isoformat(),
                'column': column,
                'values_filled': int(missing_count),
                'strategy_used': strategy,
                'fill_value': str(fill_value) if fill_value is not None else None
            }
            self.changes_log.append(change)
            
            logger.info(f"Filled {missing_count} missing values in '{column}' using {strategy}")
            
            return change
            
        except Exception as e:
            logger.error(f"Error filling missing values in '{column}': {e}")
            return {
                'error': str(e),
                'values_filled': 0
            }
    
    def remove_outliers(self, column: str, method: str = 'iqr', threshold: float = 1.5) -> Dict[str, Any]:
        """
        Remove or cap outliers in a numeric column.
        
        Args:
            column: Column name
            method: Detection method ('iqr' or 'zscore')
            threshold: Threshold for outlier detection
            
        Returns:
            Dict with results
        """
        try:
            if column not in self.cleaned_df.columns:
                raise ValueError(f"Column '{column}' not found")
            
            if not pd.api.types.is_numeric_dtype(self.cleaned_df[column]):
                raise ValueError(f"Column '{column}' is not numeric")
            
            original_count = len(self.cleaned_df)
            
            if method == 'iqr':
                # IQR method
                q1 = self.cleaned_df[column].quantile(0.25)
                q3 = self.cleaned_df[column].quantile(0.75)
                iqr = q3 - q1
                
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
                
                # Remove outliers
                mask = (self.cleaned_df[column] >= lower_bound) & (self.cleaned_df[column] <= upper_bound)
                self.cleaned_df = self.cleaned_df[mask].reset_index(drop=True)
                
            elif method == 'zscore':
                # Z-score method
                mean = self.cleaned_df[column].mean()
                std = self.cleaned_df[column].std()
                
                z_scores = np.abs((self.cleaned_df[column] - mean) / std)
                mask = z_scores < threshold
                
                self.cleaned_df = self.cleaned_df[mask].reset_index(drop=True)
            
            else:
                raise ValueError(f"Unknown method: {method}")
            
            outliers_removed = original_count - len(self.cleaned_df)
            
            # Log changes
            change = {
                'operation': 'remove_outliers',
                'timestamp': datetime.now().isoformat(),
                'column': column,
                'method': method,
                'outliers_removed': int(outliers_removed),
                'original_count': original_count,
                'cleaned_count': len(self.cleaned_df)
            }
            self.changes_log.append(change)
            
            logger.info(f"Removed {outliers_removed} outliers from '{column}' using {method}")
            
            return change
            
        except Exception as e:
            logger.error(f"Error removing outliers from '{column}': {e}")
            return {
                'error': str(e),
                'outliers_removed': 0
            }
    
    def standardize_format(self, column: str, target_format: str = 'auto') -> Dict[str, Any]:
        """
        Standardize format in a text column.
        
        Args:
            column: Column name
            target_format: Target format ('upper', 'lower', 'title', 'auto')
            
        Returns:
            Dict with results
        """
        try:
            if column not in self.cleaned_df.columns:
                raise ValueError(f"Column '{column}' not found")
            
            # Count values that will change
            original_values = self.cleaned_df[column].copy()
            
            # Apply formatting
            if target_format == 'upper':
                self.cleaned_df[column] = self.cleaned_df[column].str.upper()
            elif target_format == 'lower':
                self.cleaned_df[column] = self.cleaned_df[column].str.lower()
            elif target_format == 'title':
                self.cleaned_df[column] = self.cleaned_df[column].str.title()
            elif target_format == 'auto':
                # Auto-detect most common format
                # Use title case as default
                self.cleaned_df[column] = self.cleaned_df[column].str.title()
            
            # Also remove extra whitespace
            self.cleaned_df[column] = self.cleaned_df[column].str.strip()
            
            # Count changes
            changed_count = (original_values != self.cleaned_df[column]).sum()
            
            # Log changes
            change = {
                'operation': 'standardize_format',
                'timestamp': datetime.now().isoformat(),
                'column': column,
                'target_format': target_format,
                'values_changed': int(changed_count)
            }
            self.changes_log.append(change)
            
            logger.info(f"Standardized format in '{column}', {changed_count} values changed")
            
            return change
            
        except Exception as e:
            logger.error(f"Error standardizing format in '{column}': {e}")
            return {
                'error': str(e),
                'values_changed': 0
            }
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """
        Get the cleaned DataFrame.
        
        Returns:
            Cleaned pandas DataFrame
        """
        return self.cleaned_df.copy()
    
    def get_changes_log(self) -> List[Dict[str, Any]]:
        """
        Get log of all changes made.
        
        Returns:
            List of change dictionaries
        """
        return self.changes_log.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of cleaning operations.
        
        Returns:
            Summary dict with before/after stats
        """
        return {
            'original_shape': self.original_df.shape,
            'cleaned_shape': self.cleaned_df.shape,
            'rows_removed': len(self.original_df) - len(self.cleaned_df),
            'operations_performed': len(self.changes_log),
            'changes_log': self.changes_log
        }


# Example usage and testing
if __name__ == "__main__":
    # Create sample messy data
    messy_data = pd.DataFrame({
        'name': ['John Doe', 'JOHN DOE', 'Jane Smith', 'Jane Smith', 'Bob  '],
        'age': [25, 25, 30, 30, 150],  # 150 is outlier
        'salary': [50000, 50000, None, 60000, 55000],
        'email': ['john@email.com', 'john@email.com', 'jane@email.com', 'jane@email.com', 'bob@email.com']
    })
    
    print("Original Data:")
    print(messy_data)
    print("\n" + "="*60 + "\n")
    
    # Clean the data
    cleaner = DataCleaner(messy_data)
    
    # Remove duplicates
    result1 = cleaner.remove_duplicates()
    print(f"Duplicates removed: {result1}")
    
    # Fill missing values
    result2 = cleaner.fill_missing_values('salary', strategy='median')
    print(f"Missing values filled: {result2}")
    
    # Standardize format
    result3 = cleaner.standardize_format('name', target_format='title')
    print(f"Format standardized: {result3}")
    
    # Remove outliers
    result4 = cleaner.remove_outliers('age', method='iqr')
    print(f"Outliers removed: {result4}")
    
    print("\n" + "="*60 + "\n")
    print("Cleaned Data:")
    print(cleaner.get_cleaned_data())
    
    print("\n" + "="*60 + "\n")
    print("Summary:")
    import json
    print(json.dumps(cleaner.get_summary(), indent=2))