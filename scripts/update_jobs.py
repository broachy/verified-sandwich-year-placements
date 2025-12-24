import requests
import json
from datetime import datetime

SEARCH_TERMS = [
    "business industrial placement",
    "business sandwich placement",
    "hospitality management placement"
]

RESULTS = []

def valid_dates(text):
    return "2026" in text or "2027" in text

for term in SEARCH_TERMS:
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
    params = {
        "app_id": "demo",
        "app_key": "demo",
        "results_per_page": 10,
        "what": term,
        "content-type": "application/json"
    }

    r = requests.get(url, params=params)
    if r.status_code != 200:
        continue

    data = r.json()

    for job in data.get("results", []):
        description = job.get("description", "").lower()

        if not valid_dates(description):
            continue

        RESULTS.append({
            "company": job["company"]["display_name"],
            "role": job["title"],
            "category": "Hospitality" if "hospitality" in term else "Business",
            "start": "2026-07-01",
            "end": "2027-04-30",
            "url": job["redirect_url"]
        })

with open("data/jobs.json", "w") as f:
    json.dump(RESULTS, f, indent=2)
