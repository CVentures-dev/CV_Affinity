import os
import requests

from dotenv import load_dotenv
load_dotenv()  # This will load the variables from your .env file
AFFINITY_API_KEY = os.environ['AFFINITY_API_KEY']


headers = {
    "Content-Type": "application/json"
}


def addFieldValue(URL, org_id, field_id, row_id, value):
    data = {
        "field_id": field_id,
        "entity_id": org_id,
        "list_entry_id": row_id,
        "value": value,
    }
    response = requests.post(URL, headers=headers, auth=("", AFFINITY_API_KEY), json=data)

    return response.status_code, response.json()


def addGlobalFieldValue(URL, org_id, field_id, value):
    data = {
        "field_id": field_id,
        "entity_id": org_id,
        "value": value,
    }
    response = requests.post(URL, headers=headers, auth=("", AFFINITY_API_KEY), json=data)

    return response.status_code, response.json()
