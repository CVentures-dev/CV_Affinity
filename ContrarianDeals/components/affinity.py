
#  Create ORGANISATION
import os
import re
import requests

from components.api import addFieldValue, addGlobalFieldValue
from components.status_logic import define_status
from components.helper import *




from dotenv import load_dotenv
load_dotenv()  # This will load the variables from your .env file


AFFINITY_API_KEY = os.getenv('AFFINITY_API_KEY')
LIST_ID = 153042 # Deals list ID


headers = {
    "Content-Type": "application/json"
}


def create_organisation(name, domain):
    url = "https://api.affinity.co/organizations"

    data = {
        "name": name,
        "domain": domain,
        "person_ids": [133557225]
    }
    response = requests.post(url, auth=("", AFFINITY_API_KEY), json=data, headers=headers)

    if response.status_code == 200:
        print_green(f"Organization created: {name}")
        organisation_id = response.json().get('id')
    else:
        print(f"Failed to create an organisation for {name}")
        print(response.json())
            
    return organisation_id


def check_if_in_list(org_id):
            url = f"https://api.affinity.co/organizations/{org_id}"
            response = requests.get(url, auth=("", AFFINITY_API_KEY))

            lists = response.json().get('list_entries', [])
            list_ids = [item['list_id'] for item in lists]
            
            # Check if that org is already in the list of Deals (id of Deals list = 153042)
            if LIST_ID in list_ids:
                return True
            else:
                return False




def create_person(name, email, org_id):
           # Create a PERSON 
        URL = "https://api.affinity.co/persons"

        # Split full name into first and last name
        name_parts = name.strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else "Unknown"


        data = {
            "first_name": first_name,
            "last_name": last_name,
            "type": 0,
            "emails": [email],
            "organization_ids": [org_id],
        }
        
        response = requests.post(URL, headers=headers, auth=("", AFFINITY_API_KEY), json=data)

       
        if response.status_code == 200:
            print_green(f"Added {name, email} as a Person ")
        else:
            print(f"Failed to add {name, email} as a Person")
        
    
        # print(response.status_code)
        print(response.json())  # Print the response data

        return



def add_to_list(name, organisation_id):
    # Add ORG to list
    URL = f"https://api.affinity.co/lists/{LIST_ID}/list-entries"

    data = {
    "entity_id": organisation_id,
    }

    response = requests.post(URL, headers=headers, auth=("", AFFINITY_API_KEY), json=data)

    # print(response.status_code)
    # print(response.json())  # Print the response data
    list_entry_id = response.json().get('id')
    if response.status_code == 200:
        print(f"Added {name} to the Deals list")
    else:
        print(f"Failed to add {name} to the Deals list")
        print(response)


    return list_entry_id


def fill_all_fields(organisation_id, list_entry_id, companyHQ, pitchdeck, industrySector, companyStage, investor_name, company_name):

    # Filling in the features
    URL =f"https://api.affinity.co/field-values"


    # Lead Origination --------------------------------------
    response_code, response = addFieldValue(URL, org_id=organisation_id, field_id="4702464", row_id=list_entry_id, value="Contrarian Website")
    if response_code == 200:
        print(f"SUCCESS: Added Lead Origination")
    else:
        print_red(f"FAILED to add Lead Origination")
        print(response)
 


    # Geo ----------------------------------------------------
    response_code, response = addFieldValue(URL, org_id=organisation_id, field_id="3523812", row_id=list_entry_id, value=companyHQ)
    if response_code == 200:
        print(f"SUCCESS: Added Geo")
    else:
        print_red(f"FAILED to add Geo")
        print(response)

        


    # # Amount Raising EURm -------------------------------------
    # response_code, response = addFieldValue(URL, org_id=organisation_id, field_id="5033148", row_id=list_entry_id, value=eurRaising)
    # if response_code == 200:
    #     print(f"SUCCESS: Added EURm Raising")
    # else:
    #     print_red(f"FAILED to add EURm Raising")



    # Pitchdeck  -----------------------------------------------
    response_code, response = addFieldValue(URL, org_id=organisation_id, field_id="5250612", row_id=list_entry_id, value=pitchdeck)
    if response_code == 200:
        print(f"SUCCESS: Added Pitchdeck")
    else:
        print_red(f"FAILED to add the Pitchdeck")
        print(response)

    # Responsible Person  -----------------------------------------------
    response_code, response = addFieldValue(URL, org_id=organisation_id, field_id="3005662", row_id=list_entry_id, value=234799453)  # Vlad Stoicescu's ID
    if response_code == 200:
        print(f"SUCCESS: Added Responsible Person")
    else:
        print_red(f"FAILED to add the Responsible Person")
        print(response)
        


    # Status  --------------------------------------------------
    status, reason_for_passing = define_status(companyHQ, companyStage, industrySector, investor_name, company_name)

    response_code, response = addFieldValue(URL, org_id=organisation_id, field_id="4683272", row_id=list_entry_id, value=status)
    if response_code == 200:
        print(f"SUCCESS: Added Status")
    else:
        print_red(f"FAILED to add the Status")
        print(response)


    if reason_for_passing is not None:
        response_code, response = addFieldValue(URL, org_id=organisation_id, field_id="4714311", row_id=list_entry_id, value=reason_for_passing)
        if response_code == 200:
            print(f"SUCCESS: Added Reason for Passing")
        else:
            print_red(f"FAILED to add the Reason for Passing")
            print(response)

        



    # Industry Sector -------------------------------------------
    response_code, response = addGlobalFieldValue(URL, org_id=organisation_id, field_id="3292656", value=industrySector)

    if response_code == 200:
        print(f"SUCCESS: Added Main Insutry")
    else:
        print_red(f"FAILED to add the Main Industry")
        print(response)
    # --------------------------------------------------------------------------------------------------------------------------------





    # Company Stage ------------------------------------------
    # Define the valid dropdown options
    dropdown_options = [
        {"id": 14861311, "text": "Growth"},
        {"id": 7863690, "text": "None"},
        {"id": 7440825, "text": "Pre-Seed"},
        {"id": 6376697, "text": "Seed"},
        {"id": 7446731, "text": "Seed+"},
        {"id": 6376698, "text": "Series A"},
        {"id": 20859700, "text": "Series B and later"}
    ]

    # Extract the valid stage names (texts)
    valid_stages = {option["text"] for option in dropdown_options}

    # Check if companyStage is valid, otherwise set it to "None"
    if companyStage not in valid_stages:
        companyStage = "None"

    # Now call your addFieldValue function
    response_code, response = addGlobalFieldValue(URL, org_id=organisation_id, field_id="3005664", value=companyStage)
    if response_code == 200:
        print(f"SUCCESS: Added Round Being Raised")
    else:
        print_red(f"FAILED to add the Round Being Raised")
    #  -------------------------------------------------------------------------------------------------------------------------------



    print_green(f"Filled out all the features of name")