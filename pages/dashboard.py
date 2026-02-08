from fasthtml.common import *
from fasthtml.svg import *
from backend.listings import get_all_listings, get_all_messages
from backend.ga_data import get_ga_overview, get_top_pages, get_traffic_sources, get_device_types


def dashboard_login():
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('Admin Login | Luxe Properties'),
        Meta(name='robots', content='noindex, nofollow'),
        Link(rel='preconnect', href='https://fonts.googleapis.com'),
        Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
        Link(href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap', rel='stylesheet'),
        Link(rel='stylesheet', href='styles/components/footer.css'),
        Link(rel='stylesheet', href='styles/static/dashboard.css')
    ),
    Body(
        Div(
            Div(
                Div(
                    Svg(
                        Path(d='M12 3L4 9v12h5v-7h6v7h5V9l-8-6z'),
                        viewbox='0 0 24 24',
                        fill='currentColor',
                        width='32', height='32'
                    ),
                    cls='login-logo-icon'
                ),
                H1('Luxe ', Span('Admin'), cls='login-brand'),
                cls='login-logo'
            ),
            H2('Dashboard Access', cls='login-title'),
            P('Enter your admin password to continue', cls='login-subtitle'),
            Form(
                Div(
                    Label('Password', fr='password'),
                    Input(type='password', id='password', name='password', placeholder='Enter admin password', required='', autofocus=''),
                    cls='form-group'
                ),
                Button('Sign In', type='submit', cls='btn btn-primary login-btn'),
                Div(id='loginError', cls='login-error'),
                method='POST',
                action='/admin',
                cls='login-form'
            ),
            P(A('Back to Website', href='/'), cls='login-back'),
            cls='login-card'
        ),
        cls='login-page'
    ),
    lang='en'
)


def dashboard_page(active_tab="overview"):
    tabs = [
        ("overview", "Analytics"),
        ("for-sale", "For Sale"),
        ("pre-selling", "Pre-Selling"),
        ("for-lease", "For Lease"),
        ("messages", "Messages"),
    ]
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('Admin Dashboard | Luxe Properties'),
        Meta(name='robots', content='noindex, nofollow'),
        Link(rel='preconnect', href='https://fonts.googleapis.com'),
        Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
        Link(href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap', rel='stylesheet'),
        Link(rel='stylesheet', href='styles/components/footer.css'),
        Link(rel='stylesheet', href='styles/static/dashboard.css')
    ),
    Body(
        Header(
            Div(
                Div(
                    Div(
                        Svg(
                            Path(d='M12 3L4 9v12h5v-7h6v7h5V9l-8-6z'),
                            viewbox='0 0 24 24',
                            fill='currentColor',
                            width='24', height='24'
                        ),
                        cls='dash-logo-icon'
                    ),
                    Span('Luxe ', Span('Admin', cls='dash-brand-accent'), cls='dash-brand'),
                    cls='dash-logo'
                ),
                Nav(
                    *[A(label, href=f'/admin?tab={tid}', cls=f'dash-nav-link{" active" if active_tab == tid else ""}') for tid, label in tabs],
                    cls='dash-nav'
                ),
                Div(
                    A('View Site', href='/', cls='btn-site', target='_blank'),
                    A('Logout', href='/admin/logout', cls='btn-logout'),
                    cls='dash-actions'
                ),
                Button(
                    Span(cls='hamburger-line'),
                    Span(cls='hamburger-line'),
                    Span(cls='hamburger-line'),
                    cls='dash-hamburger', onclick='toggleDashNav()'
                ),
                cls='dash-container'
            ),
            cls='dash-header'
        ),
        Main(
            _render_analytics_section() if active_tab == "overview" else
            _render_listing_management("for_sale", "For Sale", active_tab) if active_tab == "for-sale" else
            _render_listing_management("pre_selling", "Pre-Selling", active_tab) if active_tab == "pre-selling" else
            _render_listing_management("for_lease", "For Lease", active_tab) if active_tab == "for-lease" else
            _render_messages_section() if active_tab == "messages" else
            _render_analytics_section(),
            cls='dash-main'
        ),
        Script(src='styles/static/dashboard.js', defer=True)
    ),
    lang='en'
)


# --- Analytics Section (existing) ---

def _fetch_analytics():
    try:
        overview = get_ga_overview()
        pages = get_top_pages()
        sources = get_traffic_sources()
        devices = get_device_types()
        return overview, pages, sources, devices, None
    except Exception as e:
        return None, [], [], [], str(e)


def _format_number(n):
    if n >= 1000:
        return f"{n:,}"
    return str(n)


def _format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    if mins > 0:
        return f"{mins}m {secs}s"
    return f"{secs}s"


def _render_analytics_section():
    overview, pages, sources, devices, error = _fetch_analytics()

    users = _format_number(overview["users"]) if overview else "—"
    sessions = _format_number(overview["sessions"]) if overview else "—"
    pageviews = _format_number(overview["pageviews"]) if overview else "—"
    top_source = sources[0]["source"] if sources else "—"

    sections = [
        Section(
            H2('Overview', cls='section-heading'),
            P('Analytics from Google Analytics 4 — Last 7 days', cls='section-desc'),
            Div(
                _stat_card('Active Users', users, 'Last 7 days',
                           'M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z'),
                _stat_card('Sessions', sessions, 'Last 7 days',
                           'M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'),
                _stat_card('Page Views', pageviews, 'Last 7 days',
                           'M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z'),
                _stat_card('Top Source', top_source, 'Last 30 days',
                           'M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z'),
                cls='stats-grid', id='statsGrid'
            ),
            id='overview', cls='dash-section'
        ),
        Section(
            H2('Top Pages', cls='section-heading'),
            P('Most visited pages in the last 30 days', cls='section-desc'),
            Div(
                Div(
                    Div(
                        Span('Page', cls='table-head'),
                        Span('Views', cls='table-head'),
                        Span('Avg. Time', cls='table-head'),
                        cls='table-row table-header'
                    ),
                    Div(
                        *[_page_row(p["path"], p["title"], _format_number(p["views"]), _format_time(p["avg_time_sec"])) for p in pages]
                        if pages else [Div(P('No page data available.', cls='empty-text'), cls='table-row')],
                        id='pagesTable', cls='table-body'
                    ),
                    cls='dash-table'
                ),
                cls='table-wrapper'
            ),
            id='pages', cls='dash-section'
        ),
        Section(
            H2('Traffic Sources', cls='section-heading'),
            P('Where your visitors come from — Last 30 days', cls='section-desc'),
            Div(
                Div(
                    Div(
                        Span('Source / Medium', cls='table-head'),
                        Span('Sessions', cls='table-head'),
                        cls='table-row table-header source-header'
                    ),
                    Div(
                        *[_source_row(s["source"], _format_number(s["sessions"])) for s in sources]
                        if sources else [Div(P('No traffic data available.', cls='empty-text'), cls='table-row')],
                        id='sourcesTable', cls='table-body'
                    ),
                    cls='dash-table'
                ),
                cls='table-wrapper'
            ),
            id='sources', cls='dash-section'
        ),
        Section(
            H2('Devices', cls='section-heading'),
            P('Device breakdown — Last 30 days', cls='section-desc'),
            Div(
                *[_device_card(d["device"], d["sessions"], sum(dd["sessions"] for dd in devices)) for d in devices]
                if devices else [P('No device data available.', cls='empty-text')],
                cls='devices-grid'
            ),
            id='devices', cls='dash-section'
        ),
    ]

    if error:
        sections.append(
            Section(
                Div(
                    Div(
                        Svg(
                            Path(d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z'),
                            viewbox='0 0 24 24', fill='currentColor', width='24', height='24'
                        ),
                        cls='setup-icon'
                    ),
                    Div(
                        H3('Analytics Connection Issue'),
                        P(f'Could not load analytics data: {error}'),
                        P('Make sure your GA4 service account credentials are in ', Code('documents/cred.json'),
                          ' and the service account has access to your GA4 property.'),
                        cls='setup-text'
                    ),
                    cls='setup-card'
                ),
                cls='dash-section'
            )
        )

    return Div(*sections)


# --- Listing Management ---

def _render_listing_management(listing_type, label, active_tab):
    listings = get_all_listings(listing_type)
    url_slug = active_tab  # e.g. "for-sale"
    return Div(
        Section(
            Div(
                Div(
                    H2(f'{label} Listings', cls='section-heading'),
                    P(f'Manage your {label.lower()} property listings', cls='section-desc'),
                ),
                Button('+ Add Listing', onclick='openModal("addModal")', cls='btn-add'),
                cls='management-header'
            ),
            Div(
                Div(
                    Span('Image', cls='table-head'),
                    Span('Title', cls='table-head'),
                    Span('Price', cls='table-head'),
                    Span('Location', cls='table-head'),
                    Span('Actions', cls='table-head'),
                    cls='table-row table-header listing-table-header'
                ),
                Div(
                    *[_listing_row(l, url_slug) for l in listings],
                    Div(P('No listings found.', cls='empty-text'), cls='table-row') if not listings else '',
                    cls='table-body'
                ),
                cls='dash-table'
            ),
            cls='dash-section'
        ),
        _add_modal(listing_type, url_slug),
        *[_edit_modal(l, listing_type, url_slug) for l in listings],
    )


def _listing_row(listing, url_slug):
    lid = listing.get('id', '')
    return Div(
        Span(
            Img(src=listing.get('img_url', ''), alt=listing.get('title', ''), cls='listing-thumb'),
            cls='listing-img-cell'
        ),
        Span(listing.get('title', ''), cls='cell-value listing-title-cell'),
        Span(listing.get('price', ''), cls='cell-value'),
        Span(listing.get('location', ''), cls='cell-value'),
        Span(
            Button('Edit', onclick=f'openModal("editModal-{lid}")', cls='btn-action btn-edit'),
            Form(
                Button('Delete', type='submit', cls='btn-action btn-delete',
                       onclick="return confirm('Delete this listing?')"),
                action=f'/admin/{url_slug}/delete/{lid}', method='POST',
                cls='inline-form'
            ),
            cls='actions-cell'
        ),
        cls='table-row listing-table-row'
    )


def _add_modal(listing_type, url_slug):
    fields = _common_fields()
    if listing_type == "for_sale":
        fields.extend([
            _form_field('Featured', 'featured', 'checkbox'),
        ])
    elif listing_type == "pre_selling":
        fields.extend([
            _form_field('Developer', 'developer', 'text', required=True),
            _form_field('Turnover Year', 'turnover', 'text', required=True),
        ])
    elif listing_type == "for_lease":
        fields.extend([
            _form_field('Furnishing', 'furnishing', 'select', options=['Fully Furnished', 'Semi-Furnished', 'Unfurnished', 'Bare']),
            _form_field('Featured', 'featured', 'checkbox'),
        ])

    return Div(
        Div(
            Div(
                H3('Add New Listing'),
                Button('×', onclick='closeModal("addModal")', cls='modal-close'),
                cls='modal-header'
            ),
            Form(
                *fields,
                Div(
                    Label('Image File', cls='field-label'),
                    Input(type='file', name='image_file', accept='image/*', cls='field-input'),
                    P('Or provide an image URL below', cls='field-hint'),
                    cls='field-group'
                ),
                Div(
                    Button('Create Listing', type='submit', cls='btn-add'),
                    cls='modal-actions'
                ),
                action=f'/admin/{url_slug}/create', method='POST', enctype='multipart/form-data',
                cls='modal-form'
            ),
            cls='modal-content'
        ),
        id='addModal', cls='modal-overlay', style='display:none'
    )


def _edit_modal(listing, listing_type, url_slug):
    lid = listing.get('id', '')
    fields = _common_fields(listing)
    if listing_type == "for_sale":
        fields.extend([
            _form_field('Featured', 'featured', 'checkbox', value=listing.get('featured', False)),
        ])
    elif listing_type == "pre_selling":
        fields.extend([
            _form_field('Developer', 'developer', 'text', value=listing.get('developer', ''), required=True),
            _form_field('Turnover Year', 'turnover', 'text', value=listing.get('turnover', ''), required=True),
        ])
    elif listing_type == "for_lease":
        fields.extend([
            _form_field('Furnishing', 'furnishing', 'select', value=listing.get('furnishing', ''),
                       options=['Fully Furnished', 'Semi-Furnished', 'Unfurnished', 'Bare']),
            _form_field('Featured', 'featured', 'checkbox', value=listing.get('featured', False)),
        ])

    return Div(
        Div(
            Div(
                H3('Edit Listing'),
                Button('×', onclick=f'closeModal("editModal-{lid}")', cls='modal-close'),
                cls='modal-header'
            ),
            Form(
                *fields,
                Div(
                    Label('Image File', cls='field-label'),
                    Input(type='file', name='image_file', accept='image/*', cls='field-input'),
                    P('Leave empty to keep current image', cls='field-hint'),
                    cls='field-group'
                ),
                Div(
                    Button('Update Listing', type='submit', cls='btn-add'),
                    cls='modal-actions'
                ),
                action=f'/admin/{url_slug}/update/{lid}', method='POST', enctype='multipart/form-data',
                cls='modal-form'
            ),
            cls='modal-content'
        ),
        id=f'editModal-{lid}', cls='modal-overlay', style='display:none'
    )


def _common_fields(listing=None):
    v = listing or {}
    return [
        _form_field('Title', 'title', 'text', value=v.get('title', ''), required=True),
        Div(
            _form_field('Price', 'price', 'text', value=v.get('price', ''), required=True),
            _form_field('Price (Numeric)', 'price_numeric', 'number', value=str(v.get('price_numeric', '0'))),
            cls='form-row-2'
        ),
        _form_field('Price Label', 'price_label', 'text', value=v.get('price_label', '')),
        _form_field('Description', 'description', 'textarea', value=v.get('description', ''), required=True),
        Div(
            _form_field('Location', 'location', 'text', value=v.get('location', ''), required=True),
            _form_field('Area', 'area', 'text', value=v.get('area', '')),
            cls='form-row-2'
        ),
        Div(
            _form_field('Beds', 'beds', 'text', value=v.get('beds', '')),
            _form_field('Baths', 'baths', 'text', value=v.get('baths', '')),
            cls='form-row-2'
        ),
        _form_field('Image URL', 'img_url', 'text', value=v.get('img_url', '')),
    ]


def _form_field(label, name, field_type='text', value='', required=False, options=None):
    if field_type == 'checkbox':
        checked = bool(value) if value != '' else False
        return Div(
            Label(
                Input(type='checkbox', name=name, value='true', checked=checked),
                f' {label}',
                cls='field-checkbox-label'
            ),
            cls='field-group'
        )
    if field_type == 'select':
        return Div(
            Label(label, cls='field-label'),
            Select(
                *[Option(opt, value=opt, selected=(opt == value)) for opt in (options or [])],
                name=name, cls='field-input'
            ),
            cls='field-group'
        )
    if field_type == 'textarea':
        return Div(
            Label(label, cls='field-label'),
            Textarea(value or '', name=name, rows='3', cls='field-input', required=required),
            cls='field-group'
        )
    return Div(
        Label(label, cls='field-label'),
        Input(type=field_type, name=name, value=str(value), cls='field-input', required=required),
        cls='field-group'
    )


# --- Messages Section ---

def _render_messages_section():
    messages = get_all_messages()
    return Div(
        Section(
            H2('Contact Messages', cls='section-heading'),
            P('Messages submitted through the contact form', cls='section-desc'),
            Div(
                Div(
                    Span('From', cls='table-head'),
                    Span('Interest', cls='table-head'),
                    Span('Date', cls='table-head'),
                    Span('Status', cls='table-head'),
                    Span('Actions', cls='table-head'),
                    cls='table-row table-header msg-table-header'
                ),
                Div(
                    *[_message_row(m) for m in messages],
                    Div(P('No messages yet.', cls='empty-text'), cls='table-row') if not messages else '',
                    cls='table-body'
                ),
                cls='dash-table'
            ),
            cls='dash-section'
        ),
        *[_message_view_modal(m) for m in messages],
    )


def _message_row(msg):
    mid = msg.get('id', '')
    is_read = msg.get('is_read', False)
    created = msg.get('created_at', '')
    if created and isinstance(created, str):
        created = created[:10]
    return Div(
        Span(
            Span(msg.get('name', ''), cls='msg-name'),
            Span(msg.get('email', ''), cls='msg-email'),
            cls='msg-from-cell'
        ),
        Span(msg.get('interest', '—') or '—', cls='cell-value'),
        Span(str(created), cls='cell-value'),
        Span(
            Span('Read', cls='status-badge status-read') if is_read else Span('New', cls='status-badge status-new'),
            cls='cell-value'
        ),
        Span(
            Button('View', onclick=f'openModal("msgModal-{mid}")', cls='btn-action btn-view'),
            Form(
                Button('Mark Read', type='submit', cls='btn-action btn-read'),
                action=f'/admin/messages/read/{mid}', method='POST', cls='inline-form'
            ) if not is_read else '',
            Form(
                Button('Delete', type='submit', cls='btn-action btn-delete',
                       onclick="return confirm('Delete this message?')"),
                action=f'/admin/messages/delete/{mid}', method='POST', cls='inline-form'
            ),
            cls='actions-cell'
        ),
        cls='table-row msg-table-row'
    )


def _message_view_modal(msg):
    mid = msg.get('id', '')
    return Div(
        Div(
            Div(
                H3('Message Details'),
                Button('×', onclick=f'closeModal("msgModal-{mid}")', cls='modal-close'),
                cls='modal-header'
            ),
            Div(
                Div(Strong('From: '), msg.get('name', ''), cls='msg-detail'),
                Div(Strong('Email: '), msg.get('email', ''), cls='msg-detail'),
                Div(Strong('Phone: '), msg.get('phone', ''), cls='msg-detail'),
                Div(Strong('Interest: '), msg.get('interest', '—') or '—', cls='msg-detail'),
                Div(Strong('Date: '), str(msg.get('created_at', ''))[:10], cls='msg-detail'),
                Hr(),
                P(msg.get('message', ''), cls='msg-body'),
                cls='modal-body'
            ),
            cls='modal-content modal-content-sm'
        ),
        id=f'msgModal-{mid}', cls='modal-overlay', style='display:none'
    )


# --- Helpers for analytics ---

def _stat_card(title, value, subtitle, icon_path):
    return Div(
        Div(
            Div(
                Svg(Path(d=icon_path), viewbox='0 0 24 24', fill='currentColor', width='22', height='22'),
                cls='stat-icon'
            ),
            Div(
                P(title, cls='stat-title'),
                H3(value, cls='stat-value'),
                P(subtitle, cls='stat-subtitle'),
                cls='stat-info'
            ),
            cls='stat-inner'
        ),
        cls='stat-card'
    )


def _page_row(path, name, views, avg_time):
    return Div(
        Span(Span(name, cls='page-name'), Span(path, cls='page-path'), cls='page-cell'),
        Span(views, cls='cell-value'),
        Span(avg_time, cls='cell-value'),
        cls='table-row'
    )


def _source_row(source, sessions):
    return Div(
        Span(source, cls='cell-value source-name'),
        Span(sessions, cls='cell-value'),
        cls='table-row source-row'
    )


def _device_card(device, sessions, total):
    pct = round(sessions / total * 100) if total > 0 else 0
    icon_paths = {
        "desktop": "M21 2H3c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h7l-2 3v1h8v-1l-2-3h7c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H3V4h18v12z",
        "mobile": "M15.5 1h-8C6.12 1 5 2.12 5 3.5v17C5 21.88 6.12 23 7.5 23h8c1.38 0 2.5-1.12 2.5-2.5v-17C18 2.12 16.88 1 15.5 1zm-4 21c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4.5-4H7V4h9v14z",
        "tablet": "M18.5 0h-14C3.12 0 2 1.12 2 2.5v19C2 22.88 3.12 24 4.5 24h14c1.38 0 2.5-1.12 2.5-2.5v-19C21 1.12 19.88 0 18.5 0zm-7 23c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm7.5-4H4V3h15v16z",
    }
    icon = icon_paths.get(device.lower(), icon_paths["desktop"])
    return Div(
        Div(
            Div(
                Svg(Path(d=icon), viewbox='0 0 24 24', fill='currentColor', width='22', height='22'),
                cls='stat-icon'
            ),
            Div(
                P(device.capitalize(), cls='stat-title'),
                H3(f'{pct}%', cls='stat-value'),
                P(f'{sessions:,} sessions', cls='stat-subtitle'),
                cls='stat-info'
            ),
            cls='stat-inner'
        ),
        cls='stat-card'
    )
