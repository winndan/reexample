from fasthtml.common import *


def CookieBanner():
    return Div(
        Div(
            Div(
                Div(
                    Svg(
                        Path(d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z'),
                        viewbox='0 0 24 24',
                        xmlns='http://www.w3.org/2000/svg',
                        width='24', height='24',
                        fill='currentColor'
                    ),
                    cls='cookie-icon'
                ),
                Div(
                    H4('We Value Your Privacy'),
                    P(
                        'We use cookies and similar technologies to analyze site traffic and improve your experience. '
                        'By clicking "Accept All", you consent to our use of analytics cookies. ',
                        A('Learn more', href='/privacy', cls='cookie-link'),
                    ),
                    cls='cookie-text'
                ),
                cls='cookie-content'
            ),
            Div(
                Button('Decline', id='cookieDecline', cls='cookie-btn cookie-btn-decline'),
                Button('Accept All', id='cookieAccept', cls='cookie-btn cookie-btn-accept'),
                cls='cookie-actions'
            ),
            cls='cookie-inner'
        ),
        id='cookieBanner',
        cls='cookie-banner'
    )
