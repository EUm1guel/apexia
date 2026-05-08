import os

SUPABASE_PROJECT_URL = os.getenv(
    "SUPABASE_PROJECT_URL",
    "https://vvmkuelnhcsrslzgjdrc.supabase.co"
)

API_KEY = os.getenv(
    "SUPABASE_KEY",
    "sb_publishable_ZG57PkRSowDo8BYW8UrQWg_60LnXpvL"
)

BASE_REST = f"{SUPABASE_PROJECT_URL}/rest/v1"
BASE_STORAGE = f"{SUPABASE_PROJECT_URL}/storage/v1"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

TIMEOUT = 10

BUCKET_CURSOS = "cursos"


def get_headers(extra=None):
    headers = HEADERS.copy()
    if extra:
        headers.update(extra)
    return headers


def table_url(table):
    return f"{BASE_REST}/{table}"


def storage_upload_url(file_name):
    return f"{BASE_STORAGE}/object/{BUCKET_CURSOS}/{file_name}"


def storage_public_url(file_name):
    return f"{BASE_STORAGE}/object/public/{BUCKET_CURSOS}/{file_name}"