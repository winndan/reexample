
"MonsterUI Scrollspy Example application"

from fasthtml.common import *
from fasthtml.svg import *
import random
from styles.components.navbar import Navbar
from styles.components.footer import AppFooter
from styles.components.cookie_banner import CookieBanner
from backend.analytics import GoogleAnalytics
from backend.listings import get_latest_listings, get_listing_counts, get_homepage_settings

# Using the "slate" theme with Highlight.js enabled


# --- SVG icon helpers (reused across featured cards) ---

def _location_svg():
    return Svg(
        Path(d='M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z'),
        viewbox='0 0 24 24', xmlns='http://www.w3.org/2000/svg'
    )

def _bed_svg():
    return Svg(
        Path(d='M7 14c1.66 0 3-1.34 3-3S8.66 8 7 8s-3 1.34-3 3 1.34 3 3 3zm0-4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm12-3h-8v8H3V5H1v15h2v-3h18v3h2v-9c0-2.21-1.79-4-4-4zm2 8h-8V9h6c1.1 0 2 .9 2 2v4z'),
        viewbox='0 0 24 24', xmlns='http://www.w3.org/2000/svg'
    )

def _bath_svg():
    return Svg(
        Path(d='M21 10H7V7c0-1.1.9-2 2-2s2 .9 2 2h2c0-2.21-1.79-4-4-4S5 4.79 5 7v3H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2v-8c0-1.1-.9-2-2-2zm0 10H3v-8h18v8z'),
        viewbox='0 0 24 24', xmlns='http://www.w3.org/2000/svg'
    )

def _area_svg():
    return Svg(
        Path(d='M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z'),
        viewbox='0 0 24 24', xmlns='http://www.w3.org/2000/svg'
    )

def _heart_svg():
    return Svg(
        Path(d='M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z'),
        viewbox='0 0 24 24', xmlns='http://www.w3.org/2000/svg'
    )


def _badge_text(listing):
    t = listing.get("_type", "")
    if t == "for_sale":
        return "For Sale"
    elif t == "for_lease":
        return "For Rent"
    elif t == "pre_selling":
        return "Pre-Selling"
    return "For Sale"


def _featured_card(listing):
    price = listing.get("price", "")
    price_label = listing.get("price_label", "")
    is_lease = listing.get("_type") == "for_lease"

    price_content = (
        Div(price, Span(price_label), cls='property-price') if is_lease
        else Div(price, cls='property-price')
    )

    return Article(
        Div(
            Img(src=listing.get("img_url", ""), alt=listing.get("title", "")),
            Span(_badge_text(listing), cls='property-badge'),
            Button(_heart_svg(), aria_label='Add to favorites', cls='property-favorite'),
            cls='property-image'
        ),
        Div(
            price_content,
            H3(listing.get("title", ""), cls='property-title'),
            P(_location_svg(), listing.get("location", ""), cls='property-location'),
            Div(
                Span(_bed_svg(), listing.get("beds", ""), cls='property-feature'),
                Span(_bath_svg(), listing.get("baths", ""), cls='property-feature'),
                Span(_area_svg(), listing.get("area", ""), cls='property-feature'),
                cls='property-features'
            ),
            cls='property-content'
        ),
        cls='property-card'
    )


# --- Hardcoded fallback featured listings ---
FALLBACK_FEATURED = [
    {"title": "Modern Luxury Villa", "price": "$1,250,000", "price_label": "Gross Price", "location": "Beverly Hills, CA", "beds": "4 Beds", "baths": "3 Baths", "area": "3,500 sqft", "img_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=600&q=80", "_type": "for_sale"},
    {"title": "Contemporary Home", "price": "$890,000", "price_label": "Gross Price", "location": "Malibu, CA", "beds": "3 Beds", "baths": "2 Baths", "area": "2,800 sqft", "img_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&q=80", "_type": "for_sale"},
    {"title": "Penthouse Suite", "price": "$4,500", "price_label": "/month", "location": "Manhattan, NY", "beds": "2 Beds", "baths": "2 Baths", "area": "1,800 sqft", "img_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=600&q=80", "_type": "for_lease"},
    {"title": "Estate Mansion", "price": "$2,750,000", "price_label": "Gross Price", "location": "Hamptons, NY", "beds": "6 Beds", "baths": "5 Baths", "area": "7,200 sqft", "img_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&q=80", "_type": "for_sale"},
    {"title": "Waterfront Condo", "price": "$3,200", "price_label": "/month", "location": "Miami Beach, FL", "beds": "2 Beds", "baths": "2 Baths", "area": "1,400 sqft", "img_url": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=600&q=80", "_type": "for_lease"},
    {"title": "Modern Townhouse", "price": "$675,000", "price_label": "Gross Price", "location": "Austin, TX", "beds": "3 Beds", "baths": "2.5 Baths", "area": "2,100 sqft", "img_url": "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=600&q=80", "_type": "for_sale"},
]

# --- Hardcoded fallback stats ---
FALLBACK_STATS = [
    {"setting_key": "stat_1_number", "setting_value": "2500", "setting_label": "Properties Listed"},
    {"setting_key": "stat_2_number", "setting_value": "1800", "setting_label": "Happy Clients"},
    {"setting_key": "stat_3_number", "setting_value": "150", "setting_label": "Expert Agents"},
    {"setting_key": "stat_4_number", "setting_value": "25", "setting_label": "Years Experience"},
]


def homepage(success=False):
    # Fetch dynamic data
    featured = get_latest_listings(6) or FALLBACK_FEATURED
    counts = get_listing_counts()
    settings = get_homepage_settings() or FALLBACK_STATS

    # Build stats items from settings
    stats_items = []
    for s in settings:
        val = s.get("setting_value", "0")
        label = s.get("setting_label", "")
        stats_items.append(
            Div(
                Div('0', data_target=val, cls='stat-number'),
                Div(label, cls='stat-label'),
                cls='stat-item'
            )
        )

    # Category counts
    sale_count = counts.get("for_sale", 0)
    lease_count = counts.get("for_lease", 0)
    presell_count = counts.get("pre_selling", 0)
    total_count = sale_count + lease_count + presell_count

    # Success banner for contact form
    success_banner = Div(
        Div(
            P('Your message has been sent successfully! We will get back to you shortly.'),
            Button('x', onclick='this.parentElement.parentElement.remove()', cls='banner-close'),
            cls='container banner-inner'
        ),
        cls='success-banner'
    ) if success else ''

    return Html(
    Head(
        *GoogleAnalytics("G-6NGE48T3KE"),
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Meta(name='description', content='Luxe Properties - Discover luxury properties for sale and lease. Find your dream home with our trusted real estate services.'),
        Meta(name='keywords', content='real estate, properties, homes for sale, luxury homes, condos, apartments'),
        Meta(name='theme-color', content='#ffffff'),
        Title('Luxe Properties | Find Your Dream Home'),
        Link(rel='preconnect', href='https://fonts.googleapis.com'),
        Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
        Link(href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap', rel='stylesheet'),
        Link(rel='stylesheet', href='styles/components/navbar.css'),
        Link(rel='stylesheet', href='styles/components/footer.css'),
        Link(rel='stylesheet', href='styles/static/homepage.css'),
        Link(rel='stylesheet', href='styles/components/cookie_banner.css')
    ),
    Body(
        Navbar(active="home"),
        success_banner,
        Section(
            Div(
                P('Welcome to Luxe Properties', cls='hero-subtitle'),
                H1('Find Your Perfect Place to Call Home', cls='hero-title'),
                P('Discover luxury properties for sale and lease. We make buying, selling, and leasing properties simple, secure, and stress-free.', cls='hero-description'),
                Div(
                    Div(
                        Button('Buy', cls='search-tab active'),
                        Button('Rent', cls='search-tab'),
                        Button('Sell', cls='search-tab'),
                        cls='search-tabs'
                    ),
                    Form(
                        Div(
                            Label('Location', fr='location'),
                            Input(type='text', id='location', name='location', placeholder='Enter city or area'),
                            cls='search-field'
                        ),
                        Div(
                            Label('Property Type', fr='property-type'),
                            Select(
                                Option('All Types', value=''),
                                Option('House & Lot', value='house'),
                                Option('Condo', value='condo'),
                                Option('Townhouse', value='townhouse'),
                                Option('Commercial', value='commercial'),
                                id='property-type',
                                name='property-type'
                            ),
                            cls='search-field'
                        ),
                        Div(
                            Label('Price Range', fr='price-range'),
                            Select(
                                Option('Any Price', value=''),
                                Option('Under $15M', value='0-15000000'),
                                Option('$15M - $25M', value='15000000-25000000'),
                                Option('$25M - $50M', value='25000000-50000000'),
                                Option('$50M+', value='50000000'),
                                id='price-range',
                                name='price-range'
                            ),
                            cls='search-field'
                        ),
                        Div(
                            Label('Bedrooms', fr='bedrooms'),
                            Select(
                                Option('Any', value=''),
                                Option('Studio', value='studio'),
                                Option('1+', value='1'),
                                Option('2+', value='2'),
                                Option('3+', value='3'),
                                Option('4+', value='4'),
                                id='bedrooms',
                                name='bedrooms'
                            ),
                            cls='search-field'
                        ),
                        Button('Search', type='submit', cls='btn btn-primary search-btn'),
                        cls='search-form'
                    ),
                    cls='search-box'
                ),
                cls='hero-content'
            ),
            id='home',
            cls='hero'
        ),
        Section(
            Div(
                Div(
                    *stats_items,
                    cls='stats-grid'
                ),
                cls='container'
            ),
            cls='stats'
        ),
        Section(
            Div(
                Div(
                    P('Featured Listings', cls='section-subtitle'),
                    H2('Explore Our Premium Properties', cls='section-title'),
                    cls='section-header'
                ),
                Div(
                    *[_featured_card(l) for l in featured],
                    cls='properties-grid'
                ),
                Div(
                    A('View All Properties', href='/for-sale', cls='btn btn-outline'),
                    cls='properties-footer'
                ),
                cls='container'
            ),
            id='properties',
            cls='section'
        ),
        Section(
            Div(
                Div(
                    P('Property Types', cls='section-subtitle'),
                    H2('Browse by Category', cls='section-title'),
                    cls='section-header'
                ),
                Div(
                    Article(
                        Img(src='https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600&q=80', alt='For Sale'),
                        Div(
                            H3('For Sale', cls='category-title'),
                            P(f'{sale_count} Properties', cls='category-count'),
                            cls='category-overlay'
                        ),
                        A(href='/for-sale', cls='category-link'),
                        cls='category-card'
                    ),
                    Article(
                        Img(src='https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600&q=80', alt='Pre-Selling'),
                        Div(
                            H3('Pre-Selling', cls='category-title'),
                            P(f'{presell_count} Properties', cls='category-count'),
                            cls='category-overlay'
                        ),
                        A(href='/pre-selling', cls='category-link'),
                        cls='category-card'
                    ),
                    Article(
                        Img(src='https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&q=80', alt='For Lease'),
                        Div(
                            H3('For Lease', cls='category-title'),
                            P(f'{lease_count} Properties', cls='category-count'),
                            cls='category-overlay'
                        ),
                        A(href='/for-lease', cls='category-link'),
                        cls='category-card'
                    ),
                    Article(
                        Img(src='https://images.unsplash.com/photo-1613977257363-707ba9348227?w=600&q=80', alt='All Properties'),
                        Div(
                            H3('All Properties', cls='category-title'),
                            P(f'{total_count} Properties', cls='category-count'),
                            cls='category-overlay'
                        ),
                        A(href='/for-sale', cls='category-link'),
                        cls='category-card'
                    ),
                    cls='categories-grid'
                ),
                cls='container'
            ),
            id='categories',
            cls='section categories'
        ),
        Section(
            Div(
                Div(
                    Div(
                        Img(src='https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600&q=80', alt='Real estate team'),
                        Div(
                            Div('25+', cls='about-badge-number'),
                            Div('Years Experience', cls='about-badge-text'),
                            cls='about-badge'
                        ),
                        cls='about-image'
                    ),
                    Div(
                        P('About Us', cls='section-subtitle'),
                        H2('Your Trusted Partner in Real Estate Excellence', style='text-align: left;', cls='section-title'),
                        P('At Luxe Properties, we believe finding your dream home should be an exciting journey, not a stressful one. With over 25 years of experience in the luxury real estate market, our team of expert agents is dedicated to providing personalized service and unmatched expertise.', cls='about-description'),
                        Div(
                            Div(
                                Div(
                                    Svg(
                                        Path(d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'),
                                        viewbox='0 0 24 24',
                                        xmlns='http://www.w3.org/2000/svg'
                                    ),
                                    cls='about-feature-icon'
                                ),
                                Span('Verified Listings', cls='about-feature-text'),
                                cls='about-feature'
                            ),
                            Div(
                                Div(
                                    Svg(
                                        Path(d='M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z'),
                                        viewbox='0 0 24 24',
                                        xmlns='http://www.w3.org/2000/svg'
                                    ),
                                    cls='about-feature-icon'
                                ),
                                Span('Expert Agents', cls='about-feature-text'),
                                cls='about-feature'
                            ),
                            Div(
                                Div(
                                    Svg(
                                        Path(d='M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z'),
                                        viewbox='0 0 24 24',
                                        xmlns='http://www.w3.org/2000/svg'
                                    ),
                                    cls='about-feature-icon'
                                ),
                                Span('Secure Transactions', cls='about-feature-text'),
                                cls='about-feature'
                            ),
                            Div(
                                Div(
                                    Svg(
                                        Path(d='M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'),
                                        viewbox='0 0 24 24',
                                        xmlns='http://www.w3.org/2000/svg'
                                    ),
                                    cls='about-feature-icon'
                                ),
                                Span('24/7 Support', cls='about-feature-text'),
                                cls='about-feature'
                            ),
                            cls='about-features'
                        ),
                        A('Learn More', href='#contact', cls='btn btn-primary'),
                        cls='about-content'
                    ),
                    cls='about-grid'
                ),
                cls='container'
            ),
            id='about',
            cls='section'
        ),
        Section(
            Div(
                Div(
                    P('Testimonials', cls='section-subtitle'),
                    H2('What Our Clients Say', cls='section-title'),
                    cls='section-header'
                ),
                Div(
                    Div(
                        Div(
                            P('"Luxe Properties made our home buying experience absolutely seamless. Their team went above and beyond to find us the perfect property within our budget. Highly recommended!"', cls='testimonial-quote'),
                            Div(
                                Img(src='https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80', alt='Sarah Johnson', cls='testimonial-avatar'),
                                Div(
                                    Div('Sarah Johnson', cls='testimonial-name'),
                                    Div('Home Buyer', cls='testimonial-role'),
                                    cls='testimonial-info'
                                ),
                                cls='testimonial-author'
                            ),
                            cls='testimonial-card'
                        ),
                        Div(
                            P('"As a first-time seller, I was nervous about the process. The team at Luxe Properties guided me every step of the way and sold my property above asking price!"', cls='testimonial-quote'),
                            Div(
                                Img(src='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&q=80', alt='Michael Chen', cls='testimonial-avatar'),
                                Div(
                                    Div('Michael Chen', cls='testimonial-name'),
                                    Div('Property Seller', cls='testimonial-role'),
                                    cls='testimonial-info'
                                ),
                                cls='testimonial-author'
                            ),
                            cls='testimonial-card'
                        ),
                        Div(
                            P('"Professional, responsive, and truly dedicated to their clients. Luxe Properties found us the perfect investment property that exceeded all our expectations."', cls='testimonial-quote'),
                            Div(
                                Img(src='https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80', alt='Emily Rodriguez', cls='testimonial-avatar'),
                                Div(
                                    Div('Emily Rodriguez', cls='testimonial-name'),
                                    Div('Real Estate Investor', cls='testimonial-role'),
                                    cls='testimonial-info'
                                ),
                                cls='testimonial-author'
                            ),
                            cls='testimonial-card'
                        ),
                        cls='testimonials-track'
                    ),
                    Div(
                        Button(aria_label='Testimonial 1', cls='testimonial-dot active'),
                        Button(aria_label='Testimonial 2', cls='testimonial-dot'),
                        Button(aria_label='Testimonial 3', cls='testimonial-dot'),
                        cls='testimonials-dots'
                    ),
                    cls='testimonials-slider'
                ),
                cls='container'
            ),
            cls='section testimonials'
        ),
        Section(
            Div(
                Div(
                    P('Get In Touch', cls='section-subtitle'),
                    H2('Contact Us Today', cls='section-title'),
                    cls='section-header'
                ),
                Div(
                    Div(
                        H3("Let's Start a Conversation"),
                        P("Whether you're looking to buy, sell, or rent, our team is here to help you every step of the way. Reach out to us today and let's find your perfect property."),
                        Div(
                            Div(
                                Div(
                                    Svg(
                                        Path(d='M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z'),
                                        viewbox='0 0 24 24',
                                        xmlns='http://www.w3.org/2000/svg'
                                    ),
                                    cls='contact-icon'
                                ),
                                Div(
                                    H4('Visit Us'),
                                    P(
                                        '123 Luxury Lane, Suite 100',
                                        Br(),
                                        'Beverly Hills, CA 90210'
                                    ),
                                    cls='contact-text'
                                ),
                                cls='contact-item'
                            ),
                            Div(
                                Div(
                                    Svg(
                                        Path(d='M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z'),
                                        viewbox='0 0 24 24',
                                        xmlns='http://www.w3.org/2000/svg'
                                    ),
                                    cls='contact-icon'
                                ),
                                Div(
                                    H4('Call Us'),
                                    P(
                                        '+1 (800) 555-1234',
                                        Br(),
                                        'Mon-Fri, 9am-6pm PST'
                                    ),
                                    cls='contact-text'
                                ),
                                cls='contact-item'
                            ),
                            Div(
                                Div(
                                    Svg(
                                        Path(d='M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z'),
                                        viewbox='0 0 24 24',
                                        xmlns='http://www.w3.org/2000/svg'
                                    ),
                                    cls='contact-icon'
                                ),
                                Div(
                                    H4('Email Us'),
                                    P(
                                        'info@luxeproperties.com',
                                        Br(),
                                        'support@luxeproperties.com'
                                    ),
                                    cls='contact-text'
                                ),
                                cls='contact-item'
                            ),
                            cls='contact-details'
                        ),
                        cls='contact-info'
                    ),
                    Div(
                        H3('Send Us a Message'),
                        Form(
                            Div(
                                Div(
                                    Label('Full Name', fr='name'),
                                    Input(type='text', id='name', name='name', placeholder='John Doe', required=''),
                                    cls='form-group'
                                ),
                                Div(
                                    Label('Email Address', fr='email'),
                                    Input(type='email', id='email', name='email', placeholder='john@example.com', required=''),
                                    cls='form-group'
                                ),
                                cls='form-row'
                            ),
                            Div(
                                Div(
                                    Label('Phone Number', fr='phone'),
                                    Input(type='tel', id='phone', name='phone', placeholder='+1 (555) 000-0000', required=''),
                                    cls='form-group'
                                ),
                                Div(
                                    Label("I'm Interested In", fr='interest'),
                                    Select(
                                        Option('Select an option', value=''),
                                        Option('Buying Property', value='buying'),
                                        Option('Selling Property', value='selling'),
                                        Option('Renting Property', value='renting'),
                                        Option('Investment Opportunities', value='investing'),
                                        id='interest',
                                        name='interest'
                                    ),
                                    cls='form-group'
                                ),
                                cls='form-row'
                            ),
                            Div(
                                Label('Message', fr='message'),
                                Textarea(id='message', name='message', rows='4', placeholder='Tell us about your requirements...', required=''),
                                cls='form-group'
                            ),
                            Button('Send Message', type='submit', style='width: 100%;', cls='btn btn-primary'),
                            action='/', method='POST',
                            cls='contact-form'
                        ),
                        cls='contact-form-wrapper'
                    ),
                    cls='contact-grid'
                ),
                cls='container'
            ),
            id='contact',
            cls='section'
        ),
        CookieBanner(),
        AppFooter(),
        Script(src='styles/components/navbar.js', defer=True),
        Script(src='styles/static/homepage.js', defer=True),
        Script(src='styles/static/cookie_banner.js', defer=True)
    ),
    lang='en'
)
