import re

def replace_spaces_with_percent20(company_name):
    # Replace spaces with %20 for URL query compatibility
    return company_name.replace(" ", "%20")

def extract_domain(input_string):
    # If the input looks like a URL (contains 'http' or 'www'), process it
    if re.match(r'https?://', input_string) or 'www.' in input_string:
        # Ensure it starts with https:// if no protocol is present
        if not input_string.startswith(('http://', 'https://')):
            input_string = 'https://' + input_string
        
        # Use regex to extract the domain part of the URL
        match = re.search(r'https?://([a-zA-Z0-9.-]+)', input_string)
        if match:
            domain = match.group(1)  # Extract the domain
            return domain.replace('www.', '')  # Remove 'www.' if present

    # If it's not a URL, just return the input string as is
    return input_string


def print_green(text):
    print(f"\033[32m{text}\033[0m")

def print_red(text):
    print(f"\033[91m{text}\033[0m")
