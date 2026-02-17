"""
Cleaning API Routes
===================

Endpoints:
- POST /api/v1/analyze - Analyze uploaded file
- POST /api/v1/clean - Clean uploaded file
- GET /api/v1/health - Health check
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import logging
from io import BytesIO

from app.services.ml_service import ml_service
from app.services.cleaning_service import cleaning_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status message
    """
    return {
        "status": "healthy",
        "service": "DataClean.AI API",
        "version": "0.1.0"
    }


@router.post("/analyze")
async def analyze_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analyze uploaded file for data quality issues.
    
    Args:
        file: Uploaded CSV or Excel file
        
    Returns:
        Analysis results with problems detected
    """
    try:
        logger.info(f"📤 Received file: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload CSV or Excel files."
            )
        
        # Read file
        file_content = await file.read()
        df = cleaning_service.read_file(file_content, file.filename)
        
        if df is None:
            raise HTTPException(
                status_code=400,
                detail="Failed to read file. Please ensure it's a valid CSV or Excel file."
            )
        
        # Run ML analysis
        result = ml_service.analyze_file(df)
        
        if not result['success']:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {result.get('error', 'Unknown error')}"
            )
        
        # Get recommendations
        recommendations_result = ml_service.get_recommendations(result['analysis'])
        
        # Format response
        response = {
            "filename": file.filename,
            "file_info": {
                "rows": result['analysis']['total_rows'],
                "columns": result['analysis']['total_columns']
            },
            "problems_detected": result['analysis']['problems_detected'],
            "recommendations": recommendations_result.get('recommendations', []),
            "summary": {
                "total_problems": len(result['analysis']['problems_detected']),
                "recommended_operations": len(recommendations_result.get('recommendations', []))
            }
        }
        
        logger.info(f"✅ Analysis complete: {response['summary']['total_problems']} problems found")
        
        return response
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/clean")
async def clean_file(file: UploadFile = File(...)):
    """
    Clean uploaded file using ML-powered cleaning.
    
    Args:
        file: Uploaded CSV or Excel file
        
    Returns:
        Cleaned file for download + cleaning report
    """
    try:
        logger.info(f"📤 Received file for cleaning: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload CSV or Excel files."
            )
        
        # Read file
        file_content = await file.read()
        df = cleaning_service.read_file(file_content, file.filename)
        
        if df is None:
            raise HTTPException(
                status_code=400,
                detail="Failed to read file. Please ensure it's a valid CSV or Excel file."
            )
        
        # Run ML cleaning
        result = ml_service.clean_file(df, auto_apply=True)
        
        if not result['success']:
            raise HTTPException(
                status_code=500,
                detail=f"Cleaning failed: {result.get('error', 'Unknown error')}"
            )
        
        # Get cleaned DataFrame
        cleaned_df = result['result']['cleaned_data']
        
        # Save cleaned file to bytes
        output_format = 'csv' if file.filename.endswith('.csv') else 'excel'
        cleaned_bytes = cleaning_service.save_cleaned_file(
            cleaned_df, 
            file.filename, 
            output_format
        )
        
        if cleaned_bytes is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate cleaned file"
            )
        
        # Generate cleaned filename
        file_stem = file.filename.rsplit('.', 1)[0]
        file_ext = 'csv' if output_format == 'csv' else 'xlsx'
        cleaned_filename = f"{file_stem}_cleaned.{file_ext}"
        
        logger.info(f"✅ Cleaning complete: {result['result']['original_shape']} → {result['result']['cleaned_shape']}")
        
        # Return file as download
        return StreamingResponse(
            BytesIO(cleaned_bytes),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={cleaned_filename}",
                "X-Original-Rows": str(result['result']['original_shape'][0]),
                "X-Cleaned-Rows": str(result['result']['cleaned_shape'][0]),
                "X-Problems-Fixed": str(len(result['result']['recommendations']))
            }
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )