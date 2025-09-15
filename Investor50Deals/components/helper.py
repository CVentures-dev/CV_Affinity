import requests
import re
from urllib.parse import urlparse

def replace_spaces_with_percent20(company_name):
    # Replace spaces with %20 for URL query compatibility
    return company_name.replace(" ", "%20")

# ── 1. Bare-domain validator ────────────────────────────────────────────────
DOMAIN_RE = re.compile(
    r"""^(?=.{1,253}$)            # whole thing ≤ 253 chars
        (?:                       # one or more labels:
            [a-zA-Z0-9]           #   start with alnum
            [a-zA-Z0-9-]{0,61}    #   middle chars
            [a-zA-Z0-9]           #   end with alnum
            \.
        )+
        [A-Za-z]{2,63}$           # TLD (last label)
    """,
    re.VERBOSE,
)

def is_valid_domain(domain: str) -> bool:
    """Return True if *domain* looks like example.com (IDNA not handled)."""
    return bool(DOMAIN_RE.match(domain))

# ── 2. Drop-in replacement for your extract_domain ──────────────────────────
def extract_domain(input_string: str) -> str:
    """
    • Accepts either a bare domain or any URL.
    • Returns the canonical host (without www.) *iff* it passes validation,
      otherwise the sentinel 'wrong-format.com'.
    """
    candidate = input_string.strip()

    # If there's whitespace, definitely wrong
    if " " in candidate:
        return "wrong-format.com"

    # Add scheme if missing so urlparse understands it
    if not candidate.startswith(("http://", "https://")):
        candidate = "https://" + candidate

    host = urlparse(candidate).hostname or ""
    host = host.lstrip("www.")     # optional: peel off leading www.

    return host if is_valid_domain(host) else "wrong-domain-format-submitted.com"


def print_green(text):
    print(f"\033[32m{text}\033[0m")

def print_red(text):
    print(f"\033[91m{text}\033[0m")

def download_file_as_variable(url):
    """
    Downloads a file from a URL and returns its binary content.
    Returns None if the download fails or the URL is not provided.
    """
    if not url:
        print("No URL provided to download.")
        return None
        
    try:
        # Define a User-Agent header to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Pass the headers with the request
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()
        
        print(f"File successfully downloaded from {url}")
        
        # Return the content of the response in bytes.
        return response.content
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during download: {e}")
        return None
    
def send_to_n8n_webhook(webhook_url, file_content, org_id):
    """
    Sends a file's binary content and an organization ID to an n8n webhook.

    Args:
        webhook_url (str): The URL of the n8n webhook.
        file_content (bytes): The binary content of the file.
        org_id (str): The organization ID.

    Returns:
        bool: True if the request was successful, False otherwise.
    """
    # The `files` dictionary handles the file upload.
    # The tuple format is: (filename, file_content, content_type)
    files = {
        'file': ('pitchdeck.pdf', file_content, 'application/pdf')
    }
    
    # The `data` dictionary handles the additional form fields.
    data = {
        'org_id': org_id
    }
    
    print(f"Sending data to n8n webhook at {webhook_url}...")
    
    try:
        response = requests.post(
            webhook_url,
            files=files,
            data=data
        )
        response.raise_for_status()
        
        print("Data successfully sent to n8n webhook!")
        # n8n webhooks often return a simple "OK" message.
        print("n8n response:", response.text)
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending data to n8n: {e}")
        return False