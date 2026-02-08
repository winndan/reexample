from fasthtml.common import *

def GoogleAnalytics(measurement_id: str):
    return [
        Script(
            src=f"https://www.googletagmanager.com/gtag/js?id={measurement_id}",
            async_=True
        ),
        Script(f"""
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{measurement_id}');
        """)
    ]
