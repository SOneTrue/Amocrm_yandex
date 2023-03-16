import pandas as pd
from sqlalchemy import create_engine, String

# Establish a connection
password = 'root'
engine = create_engine(f'postgresql://test:{password}@localhost:5432/test')
# conn = psycopg2.connect(database="postgres", user="postgres", password="root123!@#", host="localhost", port="5432")
# Create a new cursor
# Read the excel file
df = pd.read_csv(r'amocrm_export_leads_2023-03-16.csv', encoding="utf-8")
print(df.info())
df.to_sql('excel', engine, if_exists='replace', index=False)
# df.to_sql('excel', engine, if_exists='append', index=False)
# df.to_sql(name='excel', con=engine, if_exists='append', index=False)
