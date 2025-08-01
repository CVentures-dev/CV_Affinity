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
