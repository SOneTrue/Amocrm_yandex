import pandas as pd
from sqlalchemy import create_engine

# Establish a connection
password = 'root'
engine = create_engine(f'postgresql://test:{password}@localhost:5432/test')

# Read the excel file
df = pd.read_csv(r'./amocrm_export_leads.csv', encoding="utf-8")
print(df.info())
try:
    df.to_sql(name='excel', con=engine, if_exists='append', index=False)
except:
    df.to_sql(name='excel', con=engine, if_exists='replace', index=False)
