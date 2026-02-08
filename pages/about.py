from fasthtml.common import *
from fasthtml.svg import *
from styles.components.navbar import Navbar
from styles.components.footer import AppFooter
from backend.analytics import GoogleAnalytics


def about_page():
    return Html(
    Head(
        *GoogleAnalytics("G-6NGE48T3KE"),
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('About Us | Luxe Properties'),
        Meta(name='description', content='Learn about Luxe Properties - Your trusted partner in luxury real estate with 25+ years of experience'),
        Link(rel='preconnect', href='https://fonts.googleapis.com'),
        Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
        Link(href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap', rel='stylesheet'),
        Link(rel='stylesheet', href='styles/components/navbar.css'),
        Link(rel='stylesheet', href='styles/components/footer.css'),
        Link(rel='stylesheet', href='styles/static/about.css')
    ),
    Body(
        Navbar(active="about"),
        Section(
            Div(
                P('About Luxe Properties', cls='hero-subtitle'),
                H1('Your Trusted Partner in Real Estate Excellence', cls='hero-title'),
                P('Setting the standard for luxury real estate since 1999', cls='hero-description'),
                cls='hero-content'
            ),
            cls='hero-small'
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
                        P('Our Story', cls='section-subtitle'),
                        H2('Excellence in Luxury Real Estate', cls='section-title'),
                        P('Founded in 1999, Luxe Properties has been at the forefront of luxury real estate for over two decades. What started as a small boutique agency has grown into one of the most trusted names in high-end property sales and rentals.', cls='about-description'),
                        P("Our success is built on a foundation of integrity, expertise, and an unwavering commitment to our clients. We don't just sell properties; we help people find their dream homes and make sound investment decisions.", cls='about-description'),
                        cls='about-content'
                    ),
                    cls='about-grid'
                ),
                cls='container'
            ),
            cls='section'
        ),
        Section(
            Div(
                Div(
                    Div(
                        Div('0', data_target='2500', cls='stat-number'),
                        Div('Properties Listed', cls='stat-label'),
                        cls='stat-item'
                    ),
                    Div(
                        Div('0', data_target='1800', cls='stat-number'),
                        Div('Happy Clients', cls='stat-label'),
                        cls='stat-item'
                    ),
                    Div(
                        Div('0', data_target='150', cls='stat-number'),
                        Div('Expert Agents', cls='stat-label'),
                        cls='stat-item'
                    ),
                    Div(
                        Div('0', data_target='25', cls='stat-number'),
                        Div('Years Experience', cls='stat-label'),
                        cls='stat-item'
                    ),
                    cls='stats-grid'
                ),
                cls='container'
            ),
            cls='section stats-section'
        ),
        Section(
            Div(
                Div(
                    P('Why Choose Us', cls='section-subtitle'),
                    H2('What Sets Us Apart', cls='section-title'),
                    cls='section-header'
                ),
                Div(
                    Div(
                        Div(
                            Svg(
                                Path(d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'),
                                viewbox='0 0 24 24',
                                xmlns='http://www.w3.org/2000/svg'
                            ),
                            cls='feature-icon'
                        ),
                        H3('Verified Listings', cls='feature-title'),
                        P('Every property is thoroughly verified and inspected to ensure accuracy and quality standards.', cls='feature-description'),
                        cls='feature-card'
                    ),
                    Div(
                        Div(
                            Svg(
                                Path(d='M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z'),
                                viewbox='0 0 24 24',
                                xmlns='http://www.w3.org/2000/svg'
                            ),
                            cls='feature-icon'
                        ),
                        H3('Expert Agents', cls='feature-title'),
                        P('Our team of seasoned professionals brings decades of combined experience to serve you.', cls='feature-description'),
                        cls='feature-card'
                    ),
                    Div(
                        Div(
                            Svg(
                                Path(d='M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z'),
                                viewbox='0 0 24 24',
                                xmlns='http://www.w3.org/2000/svg'
                            ),
                            cls='feature-icon'
                        ),
                        H3('Secure Transactions', cls='feature-title'),
                        P('We prioritize your security with encrypted transactions and comprehensive legal support.', cls='feature-description'),
                        cls='feature-card'
                    ),
                    Div(
                        Div(
                            Svg(
                                Path(d='M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'),
                                viewbox='0 0 24 24',
                                xmlns='http://www.w3.org/2000/svg'
                            ),
                            cls='feature-icon'
                        ),
                        H3('24/7 Support', cls='feature-title'),
                        P('Our dedicated support team is available around the clock to assist with your needs.', cls='feature-description'),
                        cls='feature-card'
                    ),
                    Div(
                        Div(
                            Svg(
                                Path(d='M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z'),
                                viewbox='0 0 24 24',
                                xmlns='http://www.w3.org/2000/svg'
                            ),
                            cls='feature-icon'
                        ),
                        H3('Prime Locations', cls='feature-title'),
                        P('Access exclusive properties in the most desirable neighborhoods and locations.', cls='feature-description'),
                        cls='feature-card'
                    ),
                    Div(
                        Div(
                            Svg(
                                Path(d='M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z'),
                                viewbox='0 0 24 24',
                                xmlns='http://www.w3.org/2000/svg'
                            ),
                            cls='feature-icon'
                        ),
                        H3('Market Insights', cls='feature-title'),
                        P('Stay informed with our comprehensive market analysis and property valuations.', cls='feature-description'),
                        cls='feature-card'
                    ),
                    cls='features-grid'
                ),
                cls='container'
            ),
            cls='section features-section'
        ),
        Section(
            Div(
                Div(
                    P('Our Team', cls='section-subtitle'),
                    H2('Meet Our Expert Agents', cls='section-title'),
                    cls='section-header'
                ),
                Div(
                    Div(
                        Div(
                            Img(src='https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&q=80', alt='John Anderson'),
                            cls='team-image'
                        ),
                        Div(
                            H3('John Anderson', cls='team-name'),
                            P('Senior Real Estate Agent', cls='team-role'),
                            P('15+ years of experience in luxury real estate with over 500 successful transactions.', cls='team-description'),
                            cls='team-content'
                        ),
                        cls='team-card'
                    ),
                    Div(
                        Div(
                            Img(src='https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&q=80', alt='Sarah Martinez'),
                            cls='team-image'
                        ),
                        Div(
                            H3('Sarah Martinez', cls='team-name'),
                            P('Property Consultant', cls='team-role'),
                            P('Specializing in high-end residential properties and investment opportunities.', cls='team-description'),
                            cls='team-content'
                        ),
                        cls='team-card'
                    ),
                    Div(
                        Div(
                            Img(src='https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80', alt='David Chen'),
                            cls='team-image'
                        ),
                        Div(
                            H3('David Chen', cls='team-name'),
                            P('Commercial Specialist', cls='team-role'),
                            P('Expert in commercial real estate with a focus on luxury developments.', cls='team-description'),
                            cls='team-content'
                        ),
                        cls='team-card'
                    ),
                    cls='team-grid'
                ),
                cls='container'
            ),
            cls='section team-section'
        ),
        AppFooter(),
        Script(src='styles/components/navbar.js', defer=True),
        Script(src='styles/static/about.js', defer=True),
        Script(src='styles/static/cookie_banner.js', defer=True)
    ),
    lang='en'
)
