import json
import time
import requests
from pathlib import Path


def fetch_met_data(test_mode=True, test_limit=50):
    # --------------------------------------------------
    # Step 1: Set up file paths
    # This makes sure the output is always saved inside:
    # assignment_2/data/raw/
    # no matter where you run the script from.
    # --------------------------------------------------
    base_dir = Path(__file__).resolve().parent.parent
    raw_dir = base_dir / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    output_path = raw_dir / "met_photography_raw.json"

    # --------------------------------------------------
    # Step 2: Define the search endpoint and parameters
    # We use a broader search here:
    # - departmentId=19 corresponds to Photography
    # - hasImages=True keeps only objects with images
    # - q="photograph" is used to retrieve photography-related objects
    #
    # We do NOT filter by country or date here, because the search
    # endpoint is not reliable enough for the kind of structured
    # filtering we want. We will filter later using object details.
    # --------------------------------------------------
    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {
        "departmentId": 19,
        "hasImages": True,
        "q": "photograph"
    }

    # --------------------------------------------------
    # Step 3: Request a list of matching object IDs
    # --------------------------------------------------
    print("Fetching object ID list from the Met API...")
    response = requests.get(search_url, params=params, timeout=30)
    response.raise_for_status()
    search_data = response.json()

    object_ids = search_data.get("objectIDs", [])

    if not object_ids:
        print("No matching objects found.")
        return

    print(f"Found {len(object_ids)} objects in total.")

    # --------------------------------------------------
    # Step 4: Test mode
    # During testing, only fetch a small number of objects first.
    # This helps check:
    # - whether the API works
    # - whether the fields are correct
    # - whether the file is saved in the right place
    # --------------------------------------------------
    if test_mode:
        object_ids = object_ids[:test_limit]
        print(f"Test mode ON: fetching the first {len(object_ids)} objects.")
    else:
        print("Test mode OFF: fetching the full dataset.")

    results = []

    # --------------------------------------------------
    # Step 5: Loop through object IDs and fetch details
    # For each object, we call the /objects/{id} endpoint
    # to get metadata such as title, date, country, etc.
    # --------------------------------------------------
    for i, obj_id in enumerate(object_ids, start=1):
        obj_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"

        try:
            res = requests.get(obj_url, timeout=30)

            if res.status_code == 200:
                data = res.json()

                # --------------------------------------------------
                # Step 6: Extract the fields we may need later
                # These fields are useful for:
                # - title happiness analysis
                # - country filtering
                # - time-period filtering
                # --------------------------------------------------
                record = {
                    "objectID": data.get("objectID"),
                    "title": data.get("title", ""),
                    "artistDisplayName": data.get("artistDisplayName", ""),
                    "objectDate": data.get("objectDate", ""),
                    "objectBeginDate": data.get("objectBeginDate"),
                    "objectEndDate": data.get("objectEndDate"),
                    "department": data.get("department", ""),
                    "classification": data.get("classification", ""),
                    "country": data.get("country", ""),
                    "culture": data.get("culture", ""),
                    "medium": data.get("medium", "")
                }

                # --------------------------------------------------
                # Step 7: Keep only records with a non-empty title
                # Since our project analyzes title happiness scores,
                # objects without titles are not useful.
                # --------------------------------------------------
                if record["title"]:
                    results.append(record)

            # --------------------------------------------------
            # Step 8: Print progress every 10 objects
            # --------------------------------------------------
            if i % 10 == 0:
                print(f"Fetched {i} objects...")

            # --------------------------------------------------
            # Step 9: Pause briefly between requests
            # This is polite API usage and reduces the chance of
            # sending too many requests too quickly.
            # --------------------------------------------------
            time.sleep(0.1)

        except Exception as e:
            print(f"Error fetching ID {obj_id}: {e}")

    # --------------------------------------------------
    # Step 10: Save the raw results to a JSON file
    # --------------------------------------------------
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # --------------------------------------------------
    # Step 11: Print confirmation so we can verify:
    # - where the file was saved
    # - how many records were collected
    # --------------------------------------------------
    print("Data extraction complete!")
    print(f"Saved {len(results)} records to: {output_path}")
    print(f"File exists: {output_path.exists()}")


if __name__ == "__main__":
    # --------------------------------------------------
    # Step 12: Run the function
    # Start with test_mode=True so you only fetch a small sample.
    # Once everything works, change to:
    # fetch_met_data(test_mode=False)
    # --------------------------------------------------
    fetch_met_data(test_mode=True, test_limit=50)