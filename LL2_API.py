import requests
import datetime
import time
import json
import os
import pandas as pd

def get_past_launches():
    now = datetime.datetime.now(datetime.UTC)

    # Format dates
    date_now = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    date_start = "1957-01-01T00:00:00Z"

    # CSV resume logic
    save_path = "launch_data.csv"
    seen_ids = set()

    if os.path.exists(save_path):
            existing_df = pd.read_csv(save_path)
            seen_ids = set(existing_df['id'].astype(str))
            
            if 'net' in existing_df.columns and not existing_df['net'].empty:
                existing_df['net_datetime'] = pd.to_datetime(existing_df['net'], errors='coerce', utc=True)
                latest_net_date = existing_df['net_datetime'].max()

                if pd.notna(latest_net_date):
                    date_start = (latest_net_date + datetime.timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
                    print(f"Resuming collection from: {date_start}")
    else:
        existing_df = pd.DataFrame()



    base_url = "https://ll.thespacedevs.com/2.3.0/launches/"
    params = {
        'net__gte': date_start,
        'net__lte': date_now,
        'limit': 100,
        'ordering': 'net',
        'mode': 'detailed'
    }

    # CSV resume logic
    save_path = "launch_data.csv"
    seen_ids = set()
    if os.path.exists(save_path):
        existing_df = pd.read_csv(save_path)
        seen_ids = set(existing_df['id'].astype(str))
    else:
        existing_df = pd.DataFrame()

    results = []

    new_launches_count = 0
    report_milestone = 100

    while base_url:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print("Failed to fetch data:", response.status_code)
            break

        data = response.json()

        for launch in data['results']:
            launch_id = str(launch.get("id"))
            if launch_id in seen_ids:
                continue

            results.append({
                "id": launch_id,
                "name": launch.get("name"),
                "status": launch.get("status", {}).get("name"),
                "net": launch.get("net"),
                "window_start": launch.get("window_start"),
                "window_end": launch.get("window_end"),
                "is_crewed": launch.get("is_crewed"),

                # Rocket details
                "rocket_name": launch.get("rocket", {}).get("configuration", {}).get("name"),
                "rocket_full_name": launch.get("rocket", {}).get("configuration", {}).get("full_name"),
                "rocket_manufacturer": launch.get("rocket", {}).get("configuration", {}).get("manufacturer", {}).get("name"),

                # Provider (launch agency)
                "provider": launch.get("launch_service_provider", {}).get("name"),

                # Mission details
                "mission_type": launch.get("mission", {}).get("type") if launch.get("mission") else None,
                "orbit": launch.get("mission", {}).get("orbit", {}).get("name") if launch.get("mission") else None,

                # Location info
                "pad_name": launch.get("pad", {}).get("name"),
                "location_name": launch.get("pad", {}).get("location", {}).get("name"),
                "location_country": launch.get("pad", {}).get("location", {}).get("country_code"),
            })
            seen_ids.add(launch_id)

        launches_added_this_run = len(data['results'])
        new_launches_count += launches_added_this_run

        if launches_added_this_run > 0:
            new_launches_count += launches_added_this_run

            if new_launches_count >= report_milestone:
                print(f"✅ SESSION PROGRESS: Collected {new_launches_count} new launches so far...")
                report_milestone += 100


        base_url = data.get("next")
        params = {}
        time.sleep(1)

    # Save to CSV
    if results:
        new_df = pd.DataFrame(results)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_csv(save_path, index=False)
        print(f"✅ Saved {len(new_df)} new launches, total: {len(combined_df)}")
    else:
        print("No new launches to save.")

if __name__ == "__main__":
    get_past_launches()