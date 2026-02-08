from fasthtml.common import *
from fasthtml.svg import *
from styles.components.navbar import Navbar
from styles.components.footer import AppFooter
from backend.analytics import GoogleAnalytics


def contact_page(success=False):
    return Html(
    Head(
        *GoogleAnalytics("G-6NGE48T3KE"),
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('Contact Us | Luxe Properties'),
        Meta(name='description', content='Contact Luxe Properties - Get in touch with our team of real estate experts'),
        Link(rel='preconnect', href='https://fonts.googleapis.com'),
        Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
        Link(href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap', rel='stylesheet'),
        Link(rel='stylesheet', href='styles/components/navbar.css'),
        Link(rel='stylesheet', href='styles/components/footer.css'),
        Link(rel='stylesheet', href='styles/static/contact.css')
    ),
    Body(
        Navbar(active="contact"),
        Section(
            Div(
                P('Get In Touch', cls='hero-subtitle'),
                H1('Contact Us Today', cls='hero-title'),
                P("We're here to help you find your perfect property", cls='hero-description'),
                cls='hero-content'
            ),
            cls='hero-small'
        ),
        Div(
            Div('Message sent successfully! We will get back to you soon.', cls='success-banner-text'),
            cls='success-banner'
        ) if success else '',
        Section(
            Div(
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
                            Div(
                                Div(
                                    Svg(
                                        Path(d='M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'),
                                        viewbox='0 0 24 24',
                                        xmlns='http://www.w3.org/2000/svg'
                                    ),
                                    cls='contact-icon'
                                ),
                                Div(
                                    H4('Office Hours'),
                                    P(
                                        'Mon-Fri: 9:00 AM - 6:00 PM',
                                        Br(),
                                        'Sat-Sun: 10:00 AM - 4:00 PM'
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
                                Textarea(id='message', name='message', rows='5', placeholder='Tell us about your requirements...', required=''),
                                cls='form-group'
                            ),
                            Button('Send Message', type='submit', cls='btn btn-primary'),
                            action='/contact', method='POST',
                            cls='contact-form'
                        ),
                        cls='contact-form-wrapper'
                    ),
                    cls='contact-grid'
                ),
                cls='container'
            ),
            cls='section'
        ),
        Section(
            Div(
                Div(
                    Svg(
                        Path(d='M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z'),
                        viewbox='0 0 24 24',
                        xmlns='http://www.w3.org/2000/svg'
                    ),
                    P(
                        '123 Luxury Lane, Suite 100',
                        Br(),
                        'Beverly Hills, CA 90210'
                    ),
                    cls='map-content'
                ),
                cls='map-placeholder'
            ),
            cls='map-section'
        ),
        AppFooter(),
        Script(src='styles/components/navbar.js', defer=True),
        Script(src='styles/static/contact.js', defer=True),
        Script(src='styles/static/cookie_banner.js', defer=True)
    ),
    lang='en'
)
