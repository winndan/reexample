from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
)
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Config
# -----------------------------
PROPERTY_ID = os.getenv("GA_PROPERTY_ID", "523567550")

# -----------------------------
# Client init (lazy)
# -----------------------------
_client = None

def get_client():
    global _client
    if _client is None:
        private_key = os.getenv("GA_PRIVATE_KEY", "")
        client_email = os.getenv("GA_CLIENT_EMAIL", "")
        if not private_key or not client_email:
            raise ValueError("GA_PRIVATE_KEY and GA_CLIENT_EMAIL must be set in .env")
        creds_info = {
            "type": "service_account",
            "project_id": os.getenv("GA_PROJECT_ID", ""),
            "private_key_id": os.getenv("GA_PRIVATE_KEY_ID", ""),
            "private_key": private_key.replace("\\n", "\n"),
            "client_email": client_email,
            "client_id": os.getenv("GA_CLIENT_ID", ""),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "universe_domain": "googleapis.com",
        }
        credentials = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/analytics.readonly"],
        )
        _client = BetaAnalyticsDataClient(credentials=credentials)
    return _client

# -----------------------------
# Overview metrics
# -----------------------------
def get_ga_overview():
    client = get_client()
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
        ],
    )

    response = client.run_report(request)

    if not response.rows:
        return {"users": 0, "sessions": 0, "pageviews": 0}

    metrics = response.rows[0].metric_values

    return {
        "users": int(metrics[0].value),
        "sessions": int(metrics[1].value),
        "pageviews": int(metrics[2].value),
    }

# -----------------------------
# Top pages + time spent
# -----------------------------
def get_top_pages(limit=5):
    client = get_client()
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimensions=[
            Dimension(name="pagePath"),
            Dimension(name="pageTitle"),
        ],
        metrics=[
            Metric(name="screenPageViews"),
            Metric(name="userEngagementDuration"),
        ],
        order_bys=[{
            "metric": {"metric_name": "screenPageViews"},
            "desc": True
        }],
        limit=limit,
    )

    response = client.run_report(request)

    pages = []
    for row in response.rows:
        views = int(row.metric_values[0].value)
        engagement = float(row.metric_values[1].value)
        avg_time = round(engagement / views, 1) if views > 0 else 0

        pages.append({
            "path": row.dimension_values[0].value,
            "title": row.dimension_values[1].value,
            "views": views,
            "avg_time_sec": avg_time,
        })

    return pages

# -----------------------------
# Traffic sources
# -----------------------------
def get_traffic_sources(limit=5):
    client = get_client()
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimensions=[
            Dimension(name="sessionSourceMedium"),
        ],
        metrics=[
            Metric(name="sessions"),
        ],
        order_bys=[{
            "metric": {"metric_name": "sessions"},
            "desc": True
        }],
        limit=limit,
    )

    response = client.run_report(request)

    sources = []
    for row in response.rows:
        sources.append({
            "source": row.dimension_values[0].value or "(direct)",
            "sessions": int(row.metric_values[0].value),
        })

    return sources

# -----------------------------
# Device types
# -----------------------------
def get_device_types():
    client = get_client()
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimensions=[
            Dimension(name="deviceCategory"),
        ],
        metrics=[
            Metric(name="sessions"),
        ],
        order_bys=[{
            "metric": {"metric_name": "sessions"},
            "desc": True
        }],
    )

    response = client.run_report(request)

    devices = []
    for row in response.rows:
        devices.append({
            "device": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
        })

    return devices
