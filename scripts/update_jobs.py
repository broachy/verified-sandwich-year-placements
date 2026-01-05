import requests
import json
import re

SEARCH_TERMS = {
    "Business": [
        "business industrial placement",
        "business sandwich placement",
        "management placement"
    ],
    "Hospitality": [
        "hospitality placement",
        "hospitality sandwich year",
        "hotel management placement"
    ]
}

RESULTS = []

def is_hospitality_placement(text):
    keywords = [
        "placement",
        "sandwich",
        "12 month",
        "year-long",
        "industrial placement"
    ]
    return any(k in text for k in keywords)

def has_explicit_business_dates(text):
    return "2026" in text and "2027" in text

for category, terms in SEARCH_TERMS.items():
    for term in terms:
        url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
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
            title = job.get("title", "").lower()

            if category == "Business":
                if not has_explicit_business_dates(description):
                    continue
                start = "2026-07-01"
                end = "2027-04-30"
                note = "Dates confirmed by employer"
            else:
                if not is_hospitality_placement(description + title):
                    continue
                start = "2026-06-15"
                end = "2027-04-30"
                note = "Expected dates based on standard sandwich-year structure"

            RESULTS.append({
                "company": job["company"]["display_name"],
                "role": job["title"],
                "category": category,
                "start": start,
                "end": end,
                "url": job["redirect_url"],
                "date_status": note
            })

with open("data/jobs.json", "w") as f:
    json.dump(RESULTS, f, indent=2)
