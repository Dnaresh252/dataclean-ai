"""
Test Supabase connection
"""

from app.core.database import get_supabase

try:
    supabase = get_supabase()
    
    # Test connection by fetching users (should be empty)
    result = supabase.table("users").select("*").execute()
    
    print("✅ Supabase connection successful!")
    print(f"Users in database: {len(result.data)}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")