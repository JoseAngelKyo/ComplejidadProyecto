from supabase import create_client

SUPABASE_URL = "https://vgdnokrkatntmaybimzp.supabase.co"
SUPABASE_KEY = "sb_secret_DSKX2aeMfRgbk51yWV450g_8_2BnN2u"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("SUPABASE CLIENT OK")
