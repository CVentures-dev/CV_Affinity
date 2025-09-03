import os
from pyairtable import Api
from pyairtable.formulas import Field, GTE, DATETIME_DIFF, NOW
import pandas as pd

from dotenv import load_dotenv
load_dotenv()  

# Load the Airtable API key from environment variables

AIRTABLE_API_KEY = Api(os.getenv('AIRTABLE_API_KEY')) 

def airtable_pull(base_id, table_id):
    table = AIRTABLE_API_KEY.table(base_id, table_id)

    # Get the formula to pick only rows that were created in the last 8 hours
    myFormula = GTE(8, DATETIME_DIFF(NOW(), Field("fldIu763gT4BlKWT7"), "hours"))
    data = table.all(formula=myFormula)

    if not data:
        # Empty result -> return empty DataFrame
        print("No new Airtable rows in the last 8 hours.")
        return pd.DataFrame()

   # Convert data into DataFrame
    df = pd.DataFrame([entry['fields'] for entry in data])


    if df.empty:
        # Safety (shouldn't happen if data truthy, but just in case)
        print("No new Airtable rows after field extraction.")
        return df
    
    # Normalize col names
    df.columns = df.columns.astype(str).str.strip()


    # Convert 'created' column to datetime format
    df['created'] = pd.to_datetime(df['created'], utc=True)

    # Sort by 'created' in descending order (latest first)
    df = df.sort_values(by='created', ascending=False)

    # Drop duplicates based on 'Company name', keeping the latest entry (first after sorting)
    df = df.drop_duplicates(subset='Company name', keep='first')

    print(f"{df.shape[0]} unique companies were submitted in the last 24 hours")

    return df
