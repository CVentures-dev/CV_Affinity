#!/bin/bash
set -euo pipefail

# Only load .env if present AND we're not already in CI
# (GitHub Actions sets GITHUB_ACTIONS=true)
if [[ -f .env && -z "${GITHUB_ACTIONS:-}" ]]; then
  # Load without overriding existing vars
  # shellcheck disable=SC2046
  set -a
  source .env
  set +a
fi

# python -u ContrarianDeals/ContrarianDeals.py
python -u Investor50Deals/Investor50Deals.py
