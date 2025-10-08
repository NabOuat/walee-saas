"""
Supabase client configuration for Walee
"""
import os
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://mqhmwffpbumevkhtdjnd.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xaG13ZmZwYnVtZXZraHRkam5kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk4Mzk5NjEsImV4cCI6MjA3NTQxNTk2MX0.Nka5IQNRWDMrFZKK31k3bHbxgR3F_HA2ZeWE58gzkew')

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase_client() -> Client:
    """
    Get Supabase client instance
    
    Usage:
        from walee.supabase_client import get_supabase_client
        
        supabase = get_supabase_client()
        data = supabase.table('users').select('*').execute()
    """
    return supabase
