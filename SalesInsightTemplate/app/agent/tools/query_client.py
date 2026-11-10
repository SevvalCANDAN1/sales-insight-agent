import json
import os
import urllib.error
import urllib.request


def fetch_sales_data(
    start_date: str,
    end_date: str,
    product_name: str = "",
    region_name: str = "",
    group_by: str = "month",
) -> list:
    """Fetch aggregated sales rows from the local query service."""
    base_url = os.getenv("SALES_QUERY_URL", "").rstrip("/")
    if not base_url:
        raise RuntimeError("SALES_QUERY_URL is not configured.")

    body = json.dumps(
        {
            "start_date": start_date,
            "end_date": end_date,
            "product_name": product_name,
            "region_name": region_name,
            "group_by": group_by,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/sales",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise RuntimeError(f"Sales query service is unreachable: {error}") from error

    if "results" not in payload:
        raise RuntimeError(payload.get("error", "Sales query service returned no results."))
    return payload["results"]
