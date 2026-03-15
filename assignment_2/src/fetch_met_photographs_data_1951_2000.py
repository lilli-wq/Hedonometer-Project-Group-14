import json
import time
from pathlib import Path

import requests


# ============================================================
# Configuration
# ============================================================

# Notes:
# Base URL for the Metropolitan Museum of Art Collection API.
API = "https://collectionapi.metmuseum.org/public/collection/v1"

# Notes:
# departmentId = 19 corresponds to the Photographs department.
DEPARTMENT_ID = 19

# Notes:
# We keep works whose date range overlaps with 1951–2000, inclusive.
DATE_BEGIN = 1951
DATE_END = 2000

# Notes:
# Stop once we collect 1000 unique records.
TARGET_COUNT = 1000

# Notes:
# A slower request interval reduces the chance of temporary blocking.
SLEEP_BETWEEN_REQUESTS = 1.0

# Notes:
# Timeout for each request.
TIMEOUT = 30

# Notes:
# Retry failed requests several times.
MAX_RETRIES = 5

# Notes:
# If too many requests fail in a row, stop early.
MAX_CONSECUTIVE_FAILURES = 8

# Notes:
# Save progress every N collected records.
SAVE_EVERY = 20

HEADERS = {
    "User-Agent": "course-project/1.0 (academic use; local fetch script)"
}


# ============================================================
# Paths
# ============================================================

# Notes:
# BASE_DIR points to the assignment_2 folder.
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CACHE_DIR = BASE_DIR / "data" / "cache"

RAW_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = RAW_DIR / "met_photographs_american_1951_2000_raw.json"
IDS_FILE = CACHE_DIR / "met_photographs_department_ids_1951_2000.json"


# ============================================================
# Helper functions
# ============================================================

def text(value):
    """
    Notes:
    Convert None to an empty string and strip whitespace.
    """
    if value is None:
        return ""
    return str(value).strip()


def nationality_ok(obj):
    """
    Notes:
    Keep only works whose artistNationality contains 'American'.
    """
    return "american" in text(obj.get("artistNationality")).lower()


def date_ok(obj):
    """
    Notes:
    Keep works whose date range overlaps with 1951–2000, inclusive.

    Overlap logic:
    objectEndDate >= 1951 AND objectBeginDate <= 2000
    """
    begin = obj.get("objectBeginDate")
    end = obj.get("objectEndDate")

    if begin is None or end is None:
        return False

    return end >= DATE_BEGIN and begin <= DATE_END


def build_record(obj):
    """
    Notes:
    Keep only fields needed for later analysis.
    """
    return {
        "objectID": obj.get("objectID"),
        "title": text(obj.get("title")),
        "artistDisplayName": text(obj.get("artistDisplayName")),
        "artistNationality": text(obj.get("artistNationality")),
        "objectDate": text(obj.get("objectDate")),
        "objectBeginDate": obj.get("objectBeginDate"),
        "objectEndDate": obj.get("objectEndDate"),
        "department": text(obj.get("department")),
        "classification": text(obj.get("classification")),
        "medium": text(obj.get("medium")),
        "repository": text(obj.get("repository")),
        "objectURL": text(obj.get("objectURL")),
    }


def save_json(obj, path):
    """
    Notes:
    Save Python data as pretty JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def get_json_with_retry(session, url, params=None):
    """
    Notes:
    Request JSON data with retry and long backoff.

    This handles temporary failures such as:
    - 403 Forbidden
    - 429 Too Many Requests
    - 5xx server errors
    - temporary network failures
    """
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()

        except requests.HTTPError as e:
            last_error = e
            status = e.response.status_code if e.response is not None else None

            if status in {403, 429, 500, 502, 503, 504} and attempt < MAX_RETRIES:
                wait_time = 15 * attempt
                print(f"HTTP {status} for {url}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue

            raise

        except requests.RequestException as e:
            last_error = e

            if attempt < MAX_RETRIES:
                wait_time = 15 * attempt
                print(f"Request failed for {url}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue

            raise

    raise last_error


# ============================================================
# Step 1: Fetch all object IDs from the Photographs department
# ============================================================

def fetch_ids(session):
    """
    Notes:
    Retrieve all object IDs from the Photographs department.
    """
    url = f"{API}/objects"
    params = {"departmentIds": DEPARTMENT_ID}

    print("Step 1: Fetching all object IDs from the Photographs department...")

    data = get_json_with_retry(session, url, params=params)
    ids = data.get("objectIDs", [])

    save_json(ids, IDS_FILE)

    print(f"Total department IDs retrieved: {len(ids)}")
    print(f"Saved ID cache to: {IDS_FILE}")

    return ids


# ============================================================
# Step 2: Fetch metadata and apply filters
# ============================================================

def fetch_objects(session, ids):
    """
    Notes:
    For each object ID:
    1. Fetch full metadata
    2. Keep only works whose artistNationality contains 'American'
    3. Keep only works whose date overlaps with 1951–2000
    4. Deduplicate by unique (title, artistDisplayName)
    5. Save progress periodically
    """
    results = []
    seen = set()
    error_count = 0
    consecutive_failures = 0

    print("Step 2: Fetching object metadata and applying filters...")

    for i, oid in enumerate(ids, start=1):
        try:
            obj_url = f"{API}/objects/{oid}"
            obj = get_json_with_retry(session, obj_url)

            # Reset failure streak after a successful request
            consecutive_failures = 0

            if not nationality_ok(obj):
                time.sleep(SLEEP_BETWEEN_REQUESTS)
                continue

            if not date_ok(obj):
                time.sleep(SLEEP_BETWEEN_REQUESTS)
                continue

            title = text(obj.get("title"))
            artist = text(obj.get("artistDisplayName"))

            # Deduplicate by title + artist
            key = (title.lower(), artist.lower())

            if key in seen:
                time.sleep(SLEEP_BETWEEN_REQUESTS)
                continue

            seen.add(key)
            results.append(build_record(obj))

            if len(results) <= 5:
                print("MATCH:", title, "|", artist)

            if len(results) % SAVE_EVERY == 0:
                save_json(results, OUTPUT_FILE)
                print(f"{len(results)} unique records collected and saved")

            if len(results) >= TARGET_COUNT:
                print(f"Reached target count: {TARGET_COUNT}")
                break

        except Exception as e:
            error_count += 1
            consecutive_failures += 1
            print(f"Error fetching objectID {oid}: {e}")

            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print(
                    f"Stopped early after {consecutive_failures} consecutive failures. "
                    "This likely indicates temporary API blocking."
                )
                break

        time.sleep(SLEEP_BETWEEN_REQUESTS)

        if i % 250 == 0:
            print(
                f"Checked {i} object IDs so far | "
                f"Collected: {len(results)} | "
                f"Errors: {error_count}"
            )

    print(f"Finished scanning. Total errors: {error_count}")
    return results


# ============================================================
# Step 3: Save final dataset
# ============================================================

def save_results(results):
    """
    Notes:
    Save the final filtered dataset as JSON.
    """
    save_json(results, OUTPUT_FILE)

    print("Step 3: Save complete.")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Total unique records: {len(results)}")


# ============================================================
# Main workflow
# ============================================================

def main():
    """
    Notes:
    Main workflow:
    1. Create a requests session
    2. Fetch all Photographs department IDs
    3. Fetch metadata one object at a time
    4. Filter for American artists and 1951–2000 overlap
    5. Deduplicate by (title, artist)
    6. Save progress and final output
    """
    with requests.Session() as session:
        session.headers.update(HEADERS)

        ids = fetch_ids(session)
        results = fetch_objects(session, ids)
        save_results(results)


if __name__ == "__main__":
    main()