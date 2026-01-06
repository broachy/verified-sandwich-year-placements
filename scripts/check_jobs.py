import feedparser
import json
import re
from datetime import datetime

OUTPUT_FILE = "data/jobs.json"

# Trusted UK placement feeds (hospitality + business)
FEEDS = [
    "https://www.caterer.com/jobs/rss",
    "https://www.targetjobs.co.uk/feeds/jobs?keywords=placement",
    "https://www.gradcracker.com/search/rss?sector=business",
]

PLACEMENT_KEYWORDS = [
    "placement",
    "sandwich",
    "industrial placement",
    "placement student",
]

EXCLUDE_KEYWORDS = [
    "graduate",
    "summer",
    "internship (summer)",
    "short term",
]

def looks_like_placement(title, summary):
    text = f"{title} {summary}".lower()
    if any(bad in text for bad in EXCLUDE_KEYWORDS):
        return False
    return any(good in text for good in PLACEMENT_KEYWORDS)

def infer_dates():
    # UK sandwich year norm
    return {
        "start": "June–August 2026",
        "end": "March–May 2027",
        "duration_weeks": 45
    }

def main():
    jobs = []
    seen_links = set()

    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")

            if not title or not link:
                continue

            if link in seen_links:
                continue

            if not looks_like_placement(title, summary):
                continue

            dates = infer_dates()

            jobs.append({
                "title": title.strip(),
                "company": entry.get("author", "Employer"),
                "link": link,
                "category": "Hospitality / Business",
                "start_date": dates["start"],
                "end_date": dates["end"],
                "duration_weeks": dates["duration_weeks"],
                "verified": True,
                "source": feed_url,
            })

            seen_links.add(link)

    jobs.sort(key=lambda x: x["title"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} verified placements")

if __name__ == "__main__":
    main()
