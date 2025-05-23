from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def supabase_insert_item(item: dict):
    response = supabase.table("inventory").insert(item).execute()
    if response.get("error"):
        raise Exception(response["error"]["message"])
    return response
