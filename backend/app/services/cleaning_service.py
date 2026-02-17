"""
Cleaning Service
================

Purpose: Handle file-level cleaning operations for FastAPI.

Handles:
- Reading uploaded files (CSV, Excel)
- Running ML cleaning
- Generating reports
- Saving cleaned files
"""

import pandas as pd
from pathlib import Path
import logging
from typing import Dict, Any, Optional
from io import BytesIO

logger = logging.getLogger(__name__)


class CleaningService:
    """
    Service for file cleaning operations.
    """
    
    @staticmethod
    def read_file(file_content: bytes, filename: str) -> Optional[pd.DataFrame]:
        """
        Read uploaded file into pandas DataFrame.
        
        Args:
            file_content: File bytes
            filename: Original filename (to detect type)
            
        Returns:
            pandas DataFrame or None if error
        """
        try:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(BytesIO(file_content))
                
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(BytesIO(file_content))
                
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            logger.info(f"✅ File read successfully: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error reading file: {e}")
            return None
    
    @staticmethod
    def save_cleaned_file(df: pd.DataFrame, original_filename: str, output_format: str = 'csv') -> Optional[bytes]:
        """
        Save cleaned DataFrame to bytes.
        
        Args:
            df: Cleaned pandas DataFrame
            original_filename: Original filename (for naming)
            output_format: Output format ('csv' or 'excel')
            
        Returns:
            File bytes or None if error
        """
        try:
            buffer = BytesIO()
            
            if output_format == 'csv':
                df.to_csv(buffer, index=False)
                
            elif output_format == 'excel':
                df.to_excel(buffer, index=False, engine='openpyxl')
                
            else:
                raise ValueError(f"Unsupported format: {output_format}")
            
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Error saving file: {e}")
            return None
    
    @staticmethod
    def generate_report(analysis: Dict[str, Any], summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cleaning report for user.
        
        Args:
            analysis: Analysis results
            summary: Cleaning summary
            
        Returns:
            Formatted report dict
        """
        try:
            report = {
                'file_info': {
                    'original_rows': analysis['total_rows'],
                    'original_columns': analysis['total_columns'],
                    'cleaned_rows': summary.get('cleaned_shape', [0])[0] if 'cleaned_shape' in summary else 0,
                },
                'problems_found': len(analysis.get('problems_detected', [])),
                'problems_details': analysis.get('problems_detected', []),
                'operations_performed': summary.get('operations_performed', 0),
                'changes_log': summary.get('changes_log', []),
                'quality_improvement': {
                    'rows_removed': summary.get('rows_removed', 0),
                    'operations': summary.get('operations_performed', 0)
                }
            }
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Error generating report: {e}")
            return {'error': str(e)}


# Global instance
cleaning_service = CleaningService()