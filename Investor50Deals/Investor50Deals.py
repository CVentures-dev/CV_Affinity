import os
import re
import pandas as pd
from pyairtable import Api
import requests

from components.affinity import add_to_list, check_if_in_list, create_organisation, create_person, fill_all_fields
from components.helper import extract_domain, print_green, print_red, replace_spaces_with_percent20
from components.airtable_pull import airtable_pull

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))


from dotenv import load_dotenv
load_dotenv()  # This will load the variables from your .env file


AFFINITY_API_KEY = os.getenv('AFFINITY_API_KEY')
    
BASE_ID = "appB2XATaLCyRuzrM"
TABLE_ID = "tbl9f0RegFtwXsGgq"

def main():
    ##### AIRTABLE PULL into df
    df = airtable_pull(BASE_ID, TABLE_ID)

    if df.empty:
        print("Investor50Deals: no new Airtable records. Nothing to report.")
        return 0



    #### LOOP THROUGH THE DF
    c = 0
    for index, row in df.iterrows():
        c+=1
        print(f"{c}/{df.shape[0]} | {row['Company name']}")
    
    
    #### CHECK IF THE ORG ALREADY EXISTS IN AFFINITY
        name_url = replace_spaces_with_percent20(row['Company name'])
        domain_url = extract_domain(row['Company website'].strip())
        url = f"https://api.affinity.co/organizations?term={name_url}+{domain_url}"
    
        response = requests.get(url, auth=("", AFFINITY_API_KEY))
        organizations = response.json().get('organizations', [])
        # print(organizations)
    
    
    
    
    # Record all the important values into vars (can skip that, but I used that in dev)
        name = row['Company name']
        first_name = row['First Name']
        email = row['E-mail address']
        domain = domain_url
        industrySector = row["Industry sector"]
        companyStage = row["Company stage"]
        companyHQ = row["Company's HQ (backup)"]
        val = pd.to_numeric(row["EUR raising"], errors="coerce")
        eurRaising = val / 1000.0
        pitchdeck = row['Pitchdeck'][0]['url'] if isinstance(row['Pitchdeck'], list) and row['Pitchdeck'] else None
    
    
    
    
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
    
        
          
            create_person(row['First Name'], row['E-mail address'], org_id)
      
            list_entry_id = add_to_list(row['First Name'], org_id)
    
            fill_all_fields(org_id, list_entry_id, companyHQ, eurRaising, pitchdeck, industrySector, companyStage, first_name, name)
    
    
    
    #### IF IT DOESN'T
        else:
            
            organisation_id = create_organisation(name, domain)
            if not organisation_id:
                continue
    
            create_person(first_name, email, organisation_id)
      
            list_entry_id = add_to_list(row['First Name'], organisation_id)
    
            fill_all_fields(organisation_id, list_entry_id, companyHQ, eurRaising, pitchdeck, industrySector, companyStage, first_name, name)

    return 0

if __name__ == "__main__":
    sys.exit(main())
