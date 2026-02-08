# backend/admin.py

ADMIN_PASSWORD = "luxe2026"

def is_admin_logged_in(session) -> bool:
    return session.get("admin_auth", False)

def login_admin(session):
    session["admin_auth"] = True

def logout_admin(session):
    session.pop("admin_auth", None)

def check_password(password: str) -> bool:
    return password == ADMIN_PASSWORD
