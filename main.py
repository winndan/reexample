# main.py
from pages.homepage import homepage
from pages.forsale import forsalepage
from pages.preselling import presellingpage
from pages.forlease import forleasepage
from fasthtml.common import *
from starlette.responses import RedirectResponse
from pages.about import about_page
from pages.contact import contact_page
from pages.dashboard import dashboard_login, dashboard_page
from backend.admin import (
    is_admin_logged_in,
    login_admin,
    logout_admin,
    check_password,
)
from backend.listings import (
    create_listing,
    update_listing,
    delete_listing,
    submit_contact_message,
    mark_message_read,
    delete_message,
    upload_image,
)
from backend.models import ContactMessageCreate


app, rt = fast_app(static_dir="styles/static")

@rt("/", methods=["GET"])
def home():
    return homepage()


@rt("/", methods=["POST"])
async def home_post(request):
    form = await request.form()
    data = ContactMessageCreate(
        name=form.get("name", ""),
        email=form.get("email", ""),
        phone=form.get("phone", ""),
        interest=form.get("interest", ""),
        message=form.get("message", ""),
    )
    result = submit_contact_message(data.model_dump())
    return homepage(success=result is not None)


@rt("/for-sale", methods=["GET"])
def forsale(request):
    page = int(request.query_params.get("page", "1"))
    return forsalepage(page=page)

@rt("/pre-selling", methods=["GET"])
def preselling(request):
    page = int(request.query_params.get("page", "1"))
    return presellingpage(page=page)

@rt("/for-lease", methods=["GET"])
def forlease(request):
    page = int(request.query_params.get("page", "1"))
    return forleasepage(page=page)

@rt("/about", methods=["GET"])
def about():
    return about_page()

@rt("/contact", methods=["GET"])
def contact():
    return contact_page()


# --- Contact Form POST ---
@rt("/contact", methods=["POST"])
async def contact_post(request):
    form = await request.form()
    data = ContactMessageCreate(
        name=form.get("name", ""),
        email=form.get("email", ""),
        phone=form.get("phone", ""),
        interest=form.get("interest", ""),
        message=form.get("message", ""),
    )
    result = submit_contact_message(data.model_dump())
    return contact_page(success=result is not None)


# --- Admin Dashboard ---
@rt("/admin", methods=["GET"])
def admin_get(session, request):
    if is_admin_logged_in(session):
        tab = request.query_params.get("tab", "overview")
        return dashboard_page(active_tab=tab)
    return dashboard_login()


@rt("/admin", methods=["POST"])
async def admin_post(session, request):
    form = await request.form()
    password = form.get("password", "")
    if check_password(password):
        login_admin(session)
        return RedirectResponse("/admin", status_code=303)
    return dashboard_login()

@rt("/admin/logout")
def admin_logout(session):
    logout_admin(session)
    return RedirectResponse("/admin", status_code=303)


# --- Helper to parse listing form ---
async def _parse_listing_form(request, listing_type):
    form = await request.form()
    data = {
        "title": form.get("title", ""),
        "price": form.get("price", ""),
        "price_numeric": float(form.get("price_numeric", 0) or 0),
        "price_label": form.get("price_label", ""),
        "description": form.get("description", ""),
        "location": form.get("location", ""),
        "beds": form.get("beds", ""),
        "baths": form.get("baths", ""),
        "area": form.get("area", ""),
        "img_url": form.get("img_url", ""),
    }
    # Handle image upload
    image_file = form.get("image_file")
    if image_file and hasattr(image_file, 'read'):
        file_bytes = await image_file.read()
        if file_bytes:
            url = upload_image(file_bytes, image_file.filename or "upload.jpg")
            if url:
                data["img_url"] = url

    # Type-specific fields
    if listing_type == "for_sale":
        data["featured"] = form.get("featured") == "true"
    elif listing_type == "pre_selling":
        data["developer"] = form.get("developer", "")
        data["turnover"] = form.get("turnover", "")
    elif listing_type == "for_lease":
        data["furnishing"] = form.get("furnishing", "Unfurnished")
        data["featured"] = form.get("featured") == "true"
    return data


# --- For Sale CRUD ---
@rt("/admin/for-sale/create", methods=["POST"])
async def admin_for_sale_create(session, request):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    data = await _parse_listing_form(request, "for_sale")
    create_listing("for_sale", data)
    return RedirectResponse("/admin?tab=for-sale", status_code=303)

@rt("/admin/for-sale/update/{lid}", methods=["POST"])
async def admin_for_sale_update(session, request, lid: str):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    data = await _parse_listing_form(request, "for_sale")
    update_listing("for_sale", lid, data)
    return RedirectResponse("/admin?tab=for-sale", status_code=303)

@rt("/admin/for-sale/delete/{lid}", methods=["POST"])
async def admin_for_sale_delete(session, lid: str):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    delete_listing("for_sale", lid)
    return RedirectResponse("/admin?tab=for-sale", status_code=303)


# --- Pre-Selling CRUD ---
@rt("/admin/pre-selling/create", methods=["POST"])
async def admin_pre_selling_create(session, request):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    data = await _parse_listing_form(request, "pre_selling")
    create_listing("pre_selling", data)
    return RedirectResponse("/admin?tab=pre-selling", status_code=303)

@rt("/admin/pre-selling/update/{lid}", methods=["POST"])
async def admin_pre_selling_update(session, request, lid: str):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    data = await _parse_listing_form(request, "pre_selling")
    update_listing("pre_selling", lid, data)
    return RedirectResponse("/admin?tab=pre-selling", status_code=303)

@rt("/admin/pre-selling/delete/{lid}", methods=["POST"])
async def admin_pre_selling_delete(session, lid: str):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    delete_listing("pre_selling", lid)
    return RedirectResponse("/admin?tab=pre-selling", status_code=303)


# --- For Lease CRUD ---
@rt("/admin/for-lease/create", methods=["POST"])
async def admin_for_lease_create(session, request):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    data = await _parse_listing_form(request, "for_lease")
    create_listing("for_lease", data)
    return RedirectResponse("/admin?tab=for-lease", status_code=303)

@rt("/admin/for-lease/update/{lid}", methods=["POST"])
async def admin_for_lease_update(session, request, lid: str):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    data = await _parse_listing_form(request, "for_lease")
    update_listing("for_lease", lid, data)
    return RedirectResponse("/admin?tab=for-lease", status_code=303)

@rt("/admin/for-lease/delete/{lid}", methods=["POST"])
async def admin_for_lease_delete(session, lid: str):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    delete_listing("for_lease", lid)
    return RedirectResponse("/admin?tab=for-lease", status_code=303)


# --- Messages ---
@rt("/admin/messages/read/{mid}", methods=["POST"])
async def admin_message_read(session, mid: str):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    mark_message_read(mid)
    return RedirectResponse("/admin?tab=messages", status_code=303)

@rt("/admin/messages/delete/{mid}", methods=["POST"])
async def admin_message_delete(session, mid: str):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    delete_message(mid)
    return RedirectResponse("/admin?tab=messages", status_code=303)


# --- Homepage Settings ---
@rt("/admin/homepage-settings/update", methods=["POST"])
async def admin_homepage_settings_update(session, request):
    if not is_admin_logged_in(session):
        return RedirectResponse("/admin", status_code=303)
    form = await request.form()
    for i in range(1, 5):
        key = f"stat_{i}_number"
        value = form.get(f"stat_{i}_value", "")
        label = form.get(f"stat_{i}_label", "")
        if value and label:
            update_homepage_setting(key, value, label)
    return RedirectResponse("/admin?tab=homepage", status_code=303)


serve()
