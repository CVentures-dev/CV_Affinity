#!/bin/bash
set -e

# Load environment variables
export $(cat .env | xargs)

# Run your scripts
python ContrarianDeals/ContrarianDeals.py
python Investor50Deals/Investor50Deals.py