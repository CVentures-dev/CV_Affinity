import re
import pycountry


def define_status(companyHQ, companyStage, industrySector):
    if not is_compatible_geo(companyHQ):
        return 15214638, "Out of Scope"
    
    if not is_early_stage(companyStage):  
        return 15214638, "Out of Scope"
    
    if not is_valid_industry(industrySector):
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
    if not isinstance(industrySector, list):  # Ensure it's a list
        return True  

    for sector in industrySector:
        cleaned_sector = re.sub(r"[\[\]]", "", sector).strip()
        cleaned_sector = cleaned_sector.replace(" and ", " & ")
        
        if cleaned_sector == "Food & Agriculture":
            return False  # If at least one matches, return False

    return True  # If no match, return True
