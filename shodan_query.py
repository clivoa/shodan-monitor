import shodan
import pandas as pd
import os
from datetime import datetime, timedelta, timezone

# ===== CONFIGURATION =====
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")  # Define this as a GitHub Secret
ASN_FILE = "asns.csv"
OUTPUT_DIR = "queries"

# ===== DATE SETUP =====
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")

file_today = f"{OUTPUT_DIR}/{today}.csv"
file_yesterday = f"{OUTPUT_DIR}/{yesterday}.csv"
file_alerts = f"{OUTPUT_DIR}/{today}_alerts.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== READ ASN LIST =====
asns_df = pd.read_csv(ASN_FILE)
asn_list = asns_df['asn'].dropna().unique()

api = shodan.Shodan(SHODAN_API_KEY)
all_data = []

for asn in asn_list:
    print(f"Searching Shodan for ASN: {asn}")
    try:
        results = api.search(f"asn:{asn}")
        for r in results['matches']:
            all_data.append({
                "ip": r.get("ip_str"),
                "port": r.get("port"),
                "hostnames": ",".join(r.get("hostnames", [])),
                "org": r.get("org"),
                "asn": r.get("asn"),
                "location": r.get("location", {}).get("country_name"),
                "timestamp": r.get("timestamp"),
                "service": r.get("product", "Unknown"),
                "banner": r.get("data", "").strip().replace("\n", " ")[:500]
            })
    except Exception as e:
        print(f"[ERROR] Failed to query ASN {asn}: {e}")

# ===== PROCESS RESULTS =====
df_today = pd.DataFrame(all_data)
df_today["key"] = df_today["ip"] + ":" + df_today["port"].astype(str)
df_today.to_csv(file_today, index=False)
print(f"[OK] Results saved to {file_today}")

# ===== COMPARISON =====
if os.path.exists(file_yesterday):
    df_yesterday = pd.read_csv(file_yesterday)
    if "key" not in df_yesterday.columns:
        df_yesterday["key"] = df_yesterday["ip"] + ":" + df_yesterday["port"].astype(str)

    keys_yesterday = set(df_yesterday["key"])
    keys_today = set(df_today["key"])

    new_keys = keys_today - keys_yesterday
    df_new = df_today[df_today["key"].isin(new_keys)]

    if not df_new.empty:
        df_new.to_csv(file_alerts, index=False)
        print(f"[ALERT] New services detected! Exported to {file_alerts}")
    else:
        print("[INFO] No new services detected.")
else:
    print(f"[WARN] Yesterday's file ({yesterday}) not found. No comparison made.")
