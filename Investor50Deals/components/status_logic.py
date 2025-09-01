import os
import re
import pycountry

from components.email_body import generate_geo_decline, generate_sector_decline, generate_topic_decline, generate_stage_decline
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()  # This will load the variables from your .env file

EMAIL_ADDRESS  = "dealflow@cventures.vc"            # sender address 
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
# TO_ADDRESS     = "benjaminas@cventures.vc"      # where to send the email
print(EMAIL_PASSWORD)

def define_status(companyHQ, companyStage, industrySector, investor_name, company_name, email):
    if not is_compatible_geo(companyHQ):
        subject, body = generate_geo_decline(investor_name.strip(), company_name.strip(), companyHQ)
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = email
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"Email sent to {email} regarding geo incompatibility: {companyHQ}")
        return 15214638, "Out of Scope"
    
    if not is_early_stage(companyStage):
        subject, body = generate_stage_decline(investor_name.strip(), company_name.strip())
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = email
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"Email sent to {email} regarding stage incompatibility: {companyStage}")
        return 15214638, "Out of Scope"
    
    if not is_valid_industry(industrySector):
        subject, body = generate_sector_decline(investor_name.strip(), company_name.strip())
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = email
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"Email sent to {email} regarding sector incompatibility: {industrySector}")
        return 15214638, "Out of Scope"
    
    return 20860360, None



def is_compatible_geo(companyHQ: str) -> bool:
    # Get a list of all European countries
    compatible_countries = {country.name for country in pycountry.countries if country.alpha_2 in [
        "AL", "AD", "AM", "AT", "AZ", "BY", "BE", "BA", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
        "GE", "DE", "GR", "HU", "IS", "IE", "IT", "KZ", "XK", "LV", "LI", "LT", "LU", "MT", "MD", "MC",
        "ME", "NL", "MK", "NO", "PL", "PT", "RO", "RU", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "TR",
        "UA", "GB", "VA", ""
    ]}
    compatible_countries.add("Israel") 
    compatible_countries.add("Europe") 
    compatible_countries.add("Ireland (Republic)")

    return companyHQ in compatible_countries

is_compatible_geo("Sweden")




def is_early_stage(companyStage: str) -> bool:
    early_stages = {"pre-seed", "seed", "pre seed", "seed+", "series a"} 
    return companyStage.lower() in early_stages 

is_early_stage("Pre-Seed")



def is_valid_industry(industrySector):
    if not isinstance(industrySector, list):  # check if it's not a list
        cleaned_sector = re.sub(r"[\[\]]", "", industrySector).strip()
        cleaned_sector = cleaned_sector.replace(" and ", " & ")

        if cleaned_sector == "Food & Agriculture":
            return False
        return True  

    for sector in industrySector:
        cleaned_sector = re.sub(r"[\[\]]", "", sector).strip()
        cleaned_sector = cleaned_sector.replace(" and ", " & ")
        
        if cleaned_sector == "Food & Agriculture":
            return False  # If at least one matches, return False

    return True  # If no match, return True

# print(is_valid_industry("Food & Agriculture"))  # False