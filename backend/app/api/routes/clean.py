"""
Cleaning API Routes
===================

Endpoints:
- POST /api/v1/analyze - Analyze uploaded file
- POST /api/v1/clean - Clean uploaded file
- GET /api/v1/health - Health check
"""

from fastapi import APIRouter, UploadFile, File, HTTPException,Header
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional

import logging
from io import BytesIO
from app.core.database import get_supabase
from app.core.auth import decode_access_token
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
async def analyze_file(
    file: UploadFile = File(...),
    authorization: Optional[str] = Header(None)
):
    """
    Analyze uploaded file for data quality issues.
    Saves file record to database if user is authenticated.
    """
    try:
        logger.info(f"📤 Received file: {file.filename}")
        
        # Check authentication (optional for free users)
        user_id = None
        user_verified = True 
        if authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
            payload = decode_access_token(token)
            if payload:
                user_id = payload.get("sub")
                if user_id:
                    supabase = get_supabase()
                    user_result = supabase.table("users").select("email_verified").eq("id", user_id).execute()
                    if user_result.data:
                        user_verified = user_result.data[0].get("email_verified", False)
                
                        if not user_verified:
                             raise HTTPException(
                        status_code=403,
                        detail="Please verify your email before uploading files. Check your inbox."
                    )
        
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
        
        # Save to database if user is authenticated
        if user_id:
            try:
                supabase = get_supabase()
                
                # Check usage limits
                usage_result = supabase.rpc("get_current_usage", {"user_uuid": user_id}).execute()
                
                if usage_result.data:
                    usage = usage_result.data[0]
                    limits = {"free": 2, "pro": 50}
                    user_limit = limits.get(usage["plan"], 2)
                    
                    if usage["files_analyzed"] >= user_limit:
                        raise HTTPException(
                            status_code=403,
                            detail=f"Monthly limit reached. You've used {usage['files_analyzed']}/{user_limit} files this month."
                        )
                
                # Save file record
                file_record = supabase.table("files").insert({
                    "user_id": user_id,
                    "original_filename": file.filename,
                    "file_size": len(file_content),
                    "rows_count": result['analysis']['total_rows'],
                    "columns_count": result['analysis']['total_columns'],
                    "problems_detected": len(result['analysis']['problems_detected']),
                    "status": "analyzed"
                }).execute()
                
                if file_record.data:
                    file_id = file_record.data[0]["id"]
                    
                    # Save analysis results
                    supabase.table("analysis_results").insert({
                        "file_id": file_id,
                        "problems_detected": result['analysis']['problems_detected'],
                        "recommendations": recommendations_result.get('recommendations', []),
                        "summary": result['analysis']
                    }).execute()
                    
                    # Update usage
                    supabase.rpc("increment_usage", {
                        "user_uuid": user_id,
                        "files_count": 1,
                        "rows_count": result['analysis']['total_rows']
                    }).execute()
                    
                    logger.info(f"✅ Saved file record for user {user_id}")
            
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Database save error: {e}")
                # Don't fail the request if DB save fails
        
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
@router.get("/files")
async def get_user_files(authorization: Optional[str] = Header(None)):
    """
    Get user's file history.
    
    Returns:
        List of user's uploaded files with analysis results
    """
    try:
        # Get user from token
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.replace("Bearer ", "")
        payload = decode_access_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload.get("sub")
        
        # Fetch user's files
        supabase = get_supabase()
        result = supabase.table("files").select("*").eq("user_id", user_id).order("uploaded_at", desc=True).limit(20).execute()
        
        return {
            "files": result.data,
            "total": len(result.data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching files: {e}")
        raise HTTPException(status_code=500, detail=str(e))