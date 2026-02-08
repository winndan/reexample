from fasthtml.common import *
from fasthtml.svg import *
from styles.components.navbar import Navbar
from styles.components.footer import AppFooter
from backend.analytics import GoogleAnalytics
from backend.listings import get_paginated_listings
import math


PER_PAGE = 6


def forsalepage(page=1):
    listings, total = get_paginated_listings("for_sale", page=page, per_page=PER_PAGE)
    total_pages = max(1, math.ceil(total / PER_PAGE))
    return Html(
    Head(
        *GoogleAnalytics("G-6NGE48T3KE"),
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('Properties For Sale - Luxe Properties'),
        Meta(name='description', content='Browse luxury properties for sale. Find your dream home from our exclusive collection.'),
        Link(rel='preconnect', href='https://fonts.googleapis.com'),
        Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
        Link(href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap', rel='stylesheet'),
        Link(rel='stylesheet', href='styles/components/navbar.css'),
        Link(rel='stylesheet', href='styles/components/footer.css'),
        Link(rel='stylesheet', href='styles/static/forsale.css')
    ),
    Body(
        Navbar(active="forsale"),
        Section(
            Div(
                Div(
                    A('Home', href='/'),
                    Span('/'),
                    Span('For Sale'),
                    cls='breadcrumb'
                ),
                H1('Properties For Sale', cls='page-title'),
                P('Find your perfect home from our exclusive collection of properties for sale', cls='page-subtitle'),
                cls='container'
            ),
            cls='page-header'
        ),
        Main(
            Div(
                Aside(
                    Div(
                        H3('Filter Properties'),
                        Button(
                            Svg(
                                Line(x1='18', y1='6', x2='6', y2='18'),
                                Line(x1='6', y1='6', x2='18', y2='18'),
                                width='24', height='24', viewbox='0 0 24 24',
                                fill='none', stroke='currentColor', stroke_width='2'
                            ),
                            id='filtersClose', cls='filters-close'
                        ),
                        cls='filters-header'
                    ),
                    Form(
                        Div(
                            Label('Location', cls='filter-label'),
                            Input(type='text', placeholder='Enter city or area', id='locationInput', cls='filter-input'),
                            cls='filter-group'
                        ),
                        Div(
                            Label('Property Type', cls='filter-label'),
                            Select(
                                Option('All Types', value=''),
                                Option('House & Lot', value='house'),
                                Option('Condos', value='condo'),
                                Option('Townhouse', value='townhouse'),
                                Option('Lot', value='lot'),
                                Option('Commercial', value='commercial'),
                                id='propertyType', cls='filter-select'
                            ),
                            cls='filter-group'
                        ),
                        Div(
                            Label('Price Range', cls='filter-label'),
                            Div(
                                Input(type='number', placeholder='Min Price', id='minPrice', cls='filter-input'),
                                Span('-', cls='price-separator'),
                                Input(type='number', placeholder='Max Price', id='maxPrice', cls='filter-input'),
                                cls='price-inputs'
                            ),
                            cls='filter-group'
                        ),
                        Div(
                            Label('Bedrooms', cls='filter-label'),
                            Div(
                                *[Label(Input(type='checkbox', name='bedrooms', value=v), Span(v), cls='checkbox-item') for v in ['Studio','1','2','3','4','5+']],
                                cls='checkbox-group'
                            ),
                            cls='filter-group'
                        ),
                        Div(
                            Label('Bathrooms', cls='filter-label'),
                            Div(
                                *[Label(Input(type='checkbox', name='bathrooms', value=v), Span(v), cls='checkbox-item') for v in ['1','2','3','4+']],
                                cls='checkbox-group'
                            ),
                            cls='filter-group'
                        ),
                        Div(
                            Button('Reset', type='button', id='resetFilters', cls='btn btn-outline'),
                            Button('Apply Filters', type='submit', cls='btn btn-primary'),
                            cls='filter-actions'
                        ),
                        id='filtersForm', cls='filters-form'
                    ),
                    id='filtersSidebar', cls='filters-sidebar'
                ),
                Div(
                    Div(
                        Div(Span(str(total), id='listingsCount'), ' Properties Found', cls='listings-count'),
                        Div(
                            Button(
                                Svg(Polygon(points='22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3'),
                                    width='20', height='20', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
                                'Filters', id='filterToggleBtn', cls='filter-toggle-btn'
                            ),
                            Div(
                                Button(
                                    Svg(Rect(x='3',y='3',width='7',height='7'), Rect(x='14',y='3',width='7',height='7'),
                                        Rect(x='14',y='14',width='7',height='7'), Rect(x='3',y='14',width='7',height='7'),
                                        width='20', height='20', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
                                    data_view='grid', aria_label='Grid view', cls='view-btn active'
                                ),
                                Button(
                                    Svg(Line(x1='8',y1='6',x2='21',y2='6'), Line(x1='8',y1='12',x2='21',y2='12'), Line(x1='8',y1='18',x2='21',y2='18'),
                                        Line(x1='3',y1='6',x2='3.01',y2='6'), Line(x1='3',y1='12',x2='3.01',y2='12'), Line(x1='3',y1='18',x2='3.01',y2='18'),
                                        width='20', height='20', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
                                    data_view='list', aria_label='List view', cls='view-btn'
                                ),
                                cls='view-toggle'
                            ),
                            Select(
                                Option('Newest First', value='newest'),
                                Option('Price: Low to High', value='price-low'),
                                Option('Price: High to Low', value='price-high'),
                                Option('Size: Largest', value='size'),
                                id='sortSelect', cls='sort-select'
                            ),
                            cls='listings-controls'
                        ),
                        cls='listings-header'
                    ),
                    Div(
                        *[_sale_card(l) for l in listings],
                        id='propertyGrid', cls='property-grid'
                    ),
                    _pagination_nav(page, total_pages, '/for-sale'),
                    cls='listings-main'
                ),
                cls='listing-container'
            ),
            cls='main-content'
        ),
        AppFooter(),
        Script(src='styles/components/navbar.js', defer=True),
        Script(src='styles/static/forsale.js', defer=True),
        Script(src='styles/static/cookie_banner.js', defer=True)
    ),
    lang='en'
)


def _pagination_nav(current_page, total_pages, base_url):
    if total_pages <= 1:
        return Div()
    return Nav(
        A(
            Svg(Polyline(points='15 18 9 12 15 6'), width='20', height='20', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
            'Previous',
            href=f'{base_url}?page={current_page - 1}' if current_page > 1 else None,
            cls='pagination-btn prev' + (' disabled' if current_page <= 1 else '')
        ),
        Div(
            *[A(str(p), href=f'{base_url}?page={p}', cls='page-number' + (' active' if p == current_page else '')) for p in range(1, total_pages + 1)],
            cls='pagination-numbers'
        ),
        A(
            'Next',
            Svg(Polyline(points='9 18 15 12 9 6'), width='20', height='20', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
            href=f'{base_url}?page={current_page + 1}' if current_page < total_pages else None,
            cls='pagination-btn next' + (' disabled' if current_page >= total_pages else '')
        ),
        aria_label='Page navigation', cls='pagination'
    )


def _sale_card(l):
    data_id = str(l.get('id', ''))
    title = l.get('title', '')
    price = l.get('price', '')
    price_label = l.get('price_label', 'Gross Price')
    price_numeric = l.get('price_numeric', 0)
    description = l.get('description', '')
    location = l.get('location', '')
    beds = l.get('beds', '')
    baths = l.get('baths', '')
    area = l.get('area', '')
    img_url = l.get('img_url', '')
    featured = l.get('featured', False)

    badges = []
    if featured:
        badges.append(Span('Featured', cls='badge badge-featured'))
    badges.append(Span('For Sale', cls='badge badge-sale'))

    # Extract numeric bed count for filtering
    bed_num = beds.split()[0] if beds else '0'

    return Article(
        Div(
            Img(src=img_url, alt=title, loading='lazy', cls='property-image'),
            Div(*badges, cls='property-badges'),
            Div(
                Div(
                    Span(
                        Svg(Path(d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'), Circle(cx='12', cy='10', r='3'),
                            width='14', height='14', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
                        location, cls='meta-item'
                    ),
                    cls='property-meta'
                ),
                cls='property-overlay'
            ),
            Button(
                Svg(Path(d='M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z'),
                    width='20', height='20', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
                aria_label='Add to favorites', cls='favorite-btn'
            ),
            cls='property-image-wrapper'
        ),
        Div(
            H3(A(title, href='#'), cls='property-title'),
            P(price, Span(price_label, cls='price-label'), cls='property-price'),
            P(description, cls='property-description'),
            Div(
                _feature_span('M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z', beds),
                _feature_span('M9 6l6 6-6 6', baths),
                _feature_span_rect(area),
                cls='property-features'
            ),
            Div(
                Div(cls='agent-info'),
                Div(A('Details', href='#', cls='btn btn-small'), cls='property-actions'),
                cls='property-footer'
            ),
            cls='property-content'
        ),
        data_id=data_id,
        data_location=location.lower(),
        data_price=str(int(price_numeric or 0)),
        data_beds=bed_num,
        cls='property-card'
    )


def _feature_span(path_d, text):
    return Span(
        Svg(Path(d=path_d), width='16', height='16', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
        text, cls='feature'
    )


def _feature_span_rect(text):
    return Span(
        Svg(Rect(x='3', y='3', width='18', height='18', rx='2'), width='16', height='16', viewbox='0 0 24 24', fill='none', stroke='currentColor', stroke_width='2'),
        text, cls='feature'
    )
