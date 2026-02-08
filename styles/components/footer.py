from fasthtml.common import *
from fasthtml.svg import *

def AppFooter():
    return Footer(
        Div(
            Div(
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
                    P(
                        "Your trusted partner in finding the perfect property. "
                        "We make buying, selling, and leasing properties simple, secure, and stress-free."
                    ),
                    Div(
                        social("facebook"),
                        social("twitter"),
                        social("instagram"),
                        social("linkedin"),
                        cls="footer-social",
                    ),
                    cls="footer-brand",
                ),

                footer_column(
                    "Quick Links",
                    [
                        ("Home", "/"),
                        ("Properties", "/properties"),
                        ("Categories", "/categories"),
                        ("About Us", "/about"),
                        ("Contact", "/contact"),
                    ],
                ),

                footer_column(
                    "Property Types",
                    [
                        ("Houses", "#"),
                        ("Apartments", "#"),
                        ("Condos", "#"),
                        ("Villas", "#"),
                        ("Commercial", "#"),
                    ],
                ),

                footer_column(
                    "Support",
                    [
                        ("Help Center", "#"),
                        ("FAQs", "#"),
                        ("Testimonials", "#"),
                        ("Careers", "#"),
                        ("Blog", "#"),
                    ],
                ),

                cls="footer-grid",
            ),

            Div(
                P("2026 Luxe Properties. All rights reserved."),
                Div(
                    A("Privacy Policy", href="#"),
                    A("Terms of Service", href="#"),
                    A("Cookie Policy", href="#"),
                    cls="footer-legal",
                ),
                cls="footer-bottom",
            ),

            cls="container",
        ),
        cls="footer",
    )


# ---------- helpers ----------

def footer_column(title, links):
    return Div(
        H4(title),
        Ul(
            *[Li(A(text, href=href)) for text, href in links],
            cls="footer-links",
        ),
        cls="footer-column",
    )


def social(kind):
    icons = {
        "facebook": Svg(
            Path(d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"),
            viewbox="0 0 24 24",
            xmlns="http://www.w3.org/2000/svg",
        ),

        "twitter": Svg(
            Path(d="M23 3a10.9 10.9 0 0 1-3.14 1.53"
                   "A4.48 4.48 0 0 0 12 8.5v1"
                   "A10.66 10.66 0 0 1 3 4"
                   "s-4 9 5 13a11.64 11.64 0 0 1-7 2"
                   "c9 5 20 0 20-11.5"
                   "a4.5 4.5 0 0 0-.08-.83"),
            viewbox="0 0 24 24",
            xmlns="http://www.w3.org/2000/svg",
        ),

        "instagram": Svg(
            Rect(x="2", y="2", width="20", height="20", rx="5", ry="5",
                 fill="none", stroke="currentColor", stroke_width="2"),
            Circle(cx="12", cy="12", r="4",
                   fill="none", stroke="currentColor", stroke_width="2"),
            Circle(cx="18", cy="6", r="1"),
            viewbox="0 0 24 24",
            xmlns="http://www.w3.org/2000/svg",
        ),

        "linkedin": Svg(
            Path(d="M16 8a6 6 0 0 1 6 6v7h-4v-7"
                   "a2 2 0 0 0-2-2"
                   "a2 2 0 0 0-2 2v7h-4v-7"
                   "a6 6 0 0 1 6-6z"),
            Rect(x="2", y="9", width="4", height="12"),
            Circle(cx="4", cy="4", r="2"),
            viewbox="0 0 24 24",
            xmlns="http://www.w3.org/2000/svg",
        ),
    }

    return A(
        icons[kind],
        href="#",
        aria_label=kind.capitalize(),
    )
