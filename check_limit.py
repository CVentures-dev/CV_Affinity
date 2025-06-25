import requests
import os
from dotenv import load_dotenv

# Load API key from .env file or environment
load_dotenv()
AFFINITY_API_KEY = os.getenv("AFFINITY_API_KEY")

if not AFFINITY_API_KEY:
    print("❌ Error: AFFINITY_API_KEY not found in environment.")
    exit()

# Set up basic auth (Affinity uses API key as password, blank username)
response = requests.get(
    "https://api.affinity.co/rate-limit",
    auth=("", AFFINITY_API_KEY)
)

try:
    response.raise_for_status()
    data = response.json()
    rate = data["rate"]

    org_monthly = rate["org_monthly"]
    api_minute = rate["api_key_per_minute"]

    print("🔁 Per-Minute API Key Limit:")
    print(f"  Limit:     {api_minute['limit']}")
    print(f"  Used:      {api_minute['used']}")
    print(f"  Remaining: {api_minute['remaining']}")
    print()

    print("📅 Monthly Org-Wide Quota:")
    print(f"  Limit:     {org_monthly['limit']}")
    print(f"  Used:      {org_monthly['used']}")
    print(f"  Remaining: {org_monthly['remaining']}")

except requests.exceptions.RequestException as e:
    print("❌ Request failed:", e)
    print("Response:", response.text)

except KeyError as e:
    print(f"❌ KeyError: Missing key {e}")
    print("Response JSON:", response.json())