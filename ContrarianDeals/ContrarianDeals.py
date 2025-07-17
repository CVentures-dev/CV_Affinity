import os
import re
import pandas as pd
from pyairtable import Api
import requests

from components.affinity import add_to_list, check_if_in_list, create_organisation, create_person, fill_all_fields
from components.helper import extract_domain, print_green, print_red, replace_spaces_with_percent20
from components.airtable_pull import airtable_pull

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))


from dotenv import load_dotenv
load_dotenv()  # This will load the variables from your .env file


AFFINITY_API_KEY = os.getenv('AFFINITY_API_KEY')
    



# Airtable Types:
# 1: First name
# 2: Email address
# 3: Pitch Deck *
# 4: Company name *
# 5: Industry Sector *
# 6: Company Stage *
# 7: Carbon hate level
# 8: Company HQ *
# 9: Company website *

# Affinity Types:
# 1: Status *
# 2: Reason for Passing *
# 3: Main Industry *
# 4: Round Being Raised *
# 5: Geo *
# 6: Lead Origination *
# 7: Pitchdeck *




##### AIRTABLE PULL into df
df = airtable_pull('app1IeYSmdK3FK93x', 'tbl1PrGax7sKkYPgp')



#### LOOP THROUGH THE DF
c = 0
for index, row in df.iterrows():
    c+=1
    print(f"{c}/{df.shape[0]} | {row['Company name']}")



#### CHECK IF THE ORG ALREADY EXISTS IN AFFINITY
    name_url = replace_spaces_with_percent20(row['Company name'])
    domain_url = extract_domain(row['Company website'])
    url = f"https://api.affinity.co/organizations?term={name_url}+{domain_url}"

    response = requests.get(url, auth=("", AFFINITY_API_KEY))

    print("Status code:", response.status_code)
    print("Response text:", response.text)

    organizations = response.json().get('organizations', [])
    print(organizations)

    # Record all the important values into vars (can skip that, but I used that in dev)
    name = row['Company name']
    first_name = row['First name']
    email = row['Email address']
    domain = extract_domain(row['Company website'])
    industrySector = row["Industry sector"]
    companyStage = row["Company stage"]
    company_stage = "Series B and later" if company_stage == "Series B and Later" else company_stage
    companyHQ = row["Company HQ"]
    pitchdeck = row['Pitch Deck']




#### IF IT DOES 
    if organizations:

        company_name = organizations[0].get('name', 'Unknown')  # Get the company name from the first result
        org_id = organizations[0].get('id', None)  # Get the company ID from the first result

        
        print_green(f"The company {company_name} already exists.")


        #### CHECK IF THE ORG ALREADY EXISTS IN THE NEEDED LIST bn
        is_in_list = check_if_in_list(org_id)
        if is_in_list == True:
            print_green(f"The company {company_name} already exists in the Deals list. Skipping...")
            continue
        else:
            print(f"The company {company_name} doesn't exist in the Deals list. Adding it now...")

    
      
        create_person(first_name, email, org_id)
  
        list_entry_id = add_to_list(first_name, org_id)

        fill_all_fields(org_id, list_entry_id, companyHQ, pitchdeck, industrySector, companyStage)



#### IF IT DOESN'T
    else:
        
        organisation_id = create_organisation(name, domain)
        if not organisation_id:
            continue

        create_person(first_name, email, organisation_id)
  
        list_entry_id = add_to_list(name, organisation_id)

        fill_all_fields(organisation_id, list_entry_id, companyHQ, pitchdeck, industrySector, companyStage)
   