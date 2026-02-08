import uuid
from backend.supabase_client import supabase, supabase_admin

TABLE_MAP = {
    "for_sale": "listings_for_sale",
    "pre_selling": "listings_pre_selling",
    "for_lease": "listings_for_lease",
}


def get_all_listings(listing_type: str) -> list[dict]:
    table = TABLE_MAP.get(listing_type)
    if not table or not supabase:
        return []
    try:
        result = supabase.table(table).select("*").order("created_at", desc=True).execute()
        return result.data or []
    except Exception:
        return []


def get_paginated_listings(listing_type: str, page: int = 1, per_page: int = 6) -> tuple[list[dict], int]:
    table = TABLE_MAP.get(listing_type)
    if not table or not supabase:
        return [], 0
    try:
        count_result = supabase.table(table).select("id", count="exact").execute()
        total = count_result.count if count_result.count is not None else 0
        start = (page - 1) * per_page
        end = start + per_page - 1
        result = supabase.table(table).select("*").order("created_at", desc=True).range(start, end).execute()
        return result.data or [], total
    except Exception:
        return [], 0


def get_listing_by_id(listing_type: str, listing_id: str) -> dict | None:
    table = TABLE_MAP.get(listing_type)
    if not table or not supabase:
        return None
    try:
        result = supabase.table(table).select("*").eq("id", listing_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


def create_listing(listing_type: str, data: dict) -> dict | None:
    table = TABLE_MAP.get(listing_type)
    if not table or not supabase_admin:
        return None
    try:
        result = supabase_admin.table(table).insert(data).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


def update_listing(listing_type: str, listing_id: str, data: dict) -> dict | None:
    table = TABLE_MAP.get(listing_type)
    if not table or not supabase_admin:
        return None
    clean = {k: v for k, v in data.items() if v is not None}
    if not clean:
        return None
    try:
        result = supabase_admin.table(table).update(clean).eq("id", listing_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


def delete_listing(listing_type: str, listing_id: str) -> bool:
    table = TABLE_MAP.get(listing_type)
    if not table or not supabase_admin:
        return False
    try:
        supabase_admin.table(table).delete().eq("id", listing_id).execute()
        return True
    except Exception:
        return False


# --- Contact Messages ---

def submit_contact_message(data: dict) -> dict | None:
    print(f"[contact] Attempting to insert message: {data}")
    if not supabase_admin:
        print("[contact] ERROR: supabase_admin client is not configured — check SUPABASE_URL and SUPABASE_SERVICE_KEY in .env")
        return None
    try:
        result = supabase_admin.table("contact_messages").insert(data).execute()
        print(f"[contact] Insert result: {result.data}")
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"[contact] Failed to insert message: {e}")
        return None


def get_all_messages() -> list[dict]:
    if not supabase_admin:
        return []
    try:
        result = supabase_admin.table("contact_messages").select("*").order("created_at", desc=True).execute()
        return result.data or []
    except Exception:
        return []


def mark_message_read(message_id: str) -> bool:
    if not supabase_admin:
        return False
    try:
        supabase_admin.table("contact_messages").update({"is_read": True}).eq("id", message_id).execute()
        return True
    except Exception:
        return False


def delete_message(message_id: str) -> bool:
    if not supabase_admin:
        return False
    try:
        supabase_admin.table("contact_messages").delete().eq("id", message_id).execute()
        return True
    except Exception:
        return False


# --- Homepage Data ---

def get_latest_listings(limit=6):
    if not supabase:
        return []
    try:
        per_table = max(limit // 3, 1)
        results = []
        for ltype, table in TABLE_MAP.items():
            rows = supabase.table(table).select("*").order("created_at", desc=True).limit(per_table).execute()
            for row in (rows.data or []):
                row["_type"] = ltype
                results.append(row)
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return results[:limit]
    except Exception:
        return []


def get_listing_counts():
    if not supabase:
        return {}
    try:
        counts = {}
        for ltype, table in TABLE_MAP.items():
            result = supabase.table(table).select("id", count="exact").execute()
            counts[ltype] = result.count if result.count is not None else 0
        return counts
    except Exception:
        return {}


def get_homepage_settings():
    if not supabase:
        return []
    try:
        result = supabase.table("homepage_settings").select("*").order("setting_key").execute()
        return result.data or []
    except Exception:
        return []


def update_homepage_setting(key, value, label):
    if not supabase_admin:
        return False
    try:
        supabase_admin.table("homepage_settings").update(
            {"setting_value": value, "setting_label": label}
        ).eq("setting_key", key).execute()
        return True
    except Exception:
        return False


# --- Image Upload ---

def upload_image(file_bytes: bytes, filename: str) -> str | None:
    if not supabase_admin:
        return None
    try:
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
        path = f"listings/{uuid.uuid4().hex}.{ext}"
        supabase_admin.storage.from_("property-images").upload(path, file_bytes, {"content-type": f"image/{ext}"})
        public_url = supabase_admin.storage.from_("property-images").get_public_url(path)
        return public_url
    except Exception:
        return None
