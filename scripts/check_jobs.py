import json
import requests
from datetime import datetime

MIN_WEEKS = 30
START_MIN = datetime(2026, 6, 1)
START_MAX = datetime(2026, 8, 31)
END_MIN = datetime(2027, 3, 20)
END_MAX = datetime(2027, 5, 10)

def valid(job):
    try:
        start = datetime.fromisoformat(job["start"])
        end = datetime.fromisoformat(job["end"])
        weeks = (end - start).days / 7
        r = requests.head(job["url"], timeout=10)
        return (
            job["category"] == "Business" and
            START_MIN <= start <= START_MAX and
            END_MIN <= end <= END_MAX and
            weeks >= MIN_WEEKS and
            r.status_code == 200
        )
    except:
        return False

with open("data/jobs.json") as f:
    jobs = json.load(f)

verified = [j for j in jobs if valid(j)]

with open("data/jobs.json", "w") as f:
    json.dump(verified, f, indent=2)
