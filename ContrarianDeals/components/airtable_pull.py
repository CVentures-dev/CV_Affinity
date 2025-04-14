import os
from pyairtable import Api
from pyairtable.formulas import Field, GTE, DATETIME_DIFF, NOW
import pandas as pd

from dotenv import load_dotenv
load_dotenv()  



AIRTABLE_API_KEY = Api(os.getenv('AIRTABLE_API_KEY')) 

def airtable_pull(base_id, table_id):
    table = AIRTABLE_API_KEY.table(base_id, table_id)

    # Get the formula to pick only rows that were created in the last 24 hours 
    myFormula = GTE(24, DATETIME_DIFF(NOW(), Field("fldvrIIlg2tbgHldw"), "hours"))
    data = table.all(formula=myFormula)

    if not data:
        raise ValueError("No data was pulled from Airtable")

   # Convert data into DataFrame
    df = pd.DataFrame([entry['fields'] for entry in data])


    if not df.empty:
        df.columns = df.columns.astype(str).str.strip()


    # Convert 'created' column to datetime format
    df['created'] = pd.to_datetime(df['Created time'], utc=True)

    # Sort by 'created' in descending order (latest first)
    df = df.sort_values(by='created', ascending=False)

    # Drop duplicates based on 'Company name', keeping the latest entry (first after sorting)
    df = df.drop_duplicates(subset='Company name', keep='first')

    print(f"{df.shape[0]} unique companies were submitted in the last 24 hours")

    return df


# Example usage
df = airtable_pull('app1IeYSmdK3FK93x', 'tbl1PrGax7sKkYPgp')
print(df)
