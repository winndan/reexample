from fasthtml.common import *
from fasthtml.svg import *


def PhoneIcon(cls=""):
    return Svg(
        Path(
            d="M22 16.92v3a2 2 0 0 1-2.18 2"
              "A19.86 19.86 0 0 1 3 5.18"
              "A2 2 0 0 1 5.11 3h3"
              "a2 2 0 0 1 2 1.72"
              "c.12.81.3 1.6.54 2.36"
              "a2 2 0 0 1-.45 2.11L9.03 10.97"
              "a16 16 0 0 0 6 6l1.78-1.78"
              "a2 2 0 0 1 2.11-.45"
              "c.76.24 1.55.42 2.36.54"
              "a2 2 0 0 1 1.72 2z"
        ),
        fill="none",
        stroke="currentColor",
        stroke_width="2",
        stroke_linecap="round",
        stroke_linejoin="round",
        viewbox="0 0 24 24",
        xmlns="http://www.w3.org/2000/svg",
        cls=cls,
    )


def Navbar(active: str = "home"):
    def link(label, href, key):
        cls = "nav-link active" if key == active else "nav-link"
        return Li(A(label, href=href, cls=cls))

    def mobile_link(label, href):
        return Li(A(label, href=href, cls="mobile-nav-link"))

    return (
        Header(
            Div(
                A(
                    Div(
                        Svg(
                            Path(d="M12 3L4 9v12h5v-7h6v7h5V9l-8-6z"),
                            viewbox="0 0 24 24",
                        ),
                        cls="logo-icon",
                    ),
                    "Luxe",
                    Span("Properties"),
                    href="/",
                    cls="logo",
                ),

                Nav(
                    Ul(
                        link("Home", "/", "home"),
                        link("For Sale", "/for-sale", "forsale"),
                        link("Pre-Selling", "/pre-selling", "preselling"),
                        link("For Lease", "/for-lease", "forlease"),
                        link("About", "/about", "about"),
                        link("Contact", "/contact", "contact"),
                        cls="nav-list",
                    ),
                    cls="nav",
                ),

                Div(
                    A(
                        PhoneIcon(),
                        "+1 (800) 555-1234",
                        href="tel:+18005551234",
                        cls="header-phone",
                    ),
                    A("Get Started", href="/contact", cls="btn btn-primary"),
                    cls="header-contact",
                ),

                Button(Span(), Span(), Span(), cls="mobile-toggle"),
                cls="container",
            ),
            cls="header",
        ),

        Div(cls="mobile-overlay"),

        Div(
            Button("✕", cls="mobile-menu-close"),
            Ul(
                mobile_link("Home", "/"),
                mobile_link("For Sale", "/for-sale"),
                mobile_link("Pre-Selling", "/pre-selling"),
                mobile_link("For Lease", "/for-lease"),
                mobile_link("About", "/about"),
                mobile_link("Contact", "/contact"),
                cls="mobile-nav-list",
            ),
            cls="mobile-menu",
        )
    )
