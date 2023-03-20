import pandas as pd
from sqlalchemy import create_engine

# Establish a connection
password = 'root'
engine = create_engine(f'postgresql://test:{password}@localhost:5432/test')
# conn = psycopg2.connect(database="postgres", user="postgres", password="root123!@#", host="localhost", port="5432")
# Create a new cursor
# Read the excel file
df = pd.read_csv("cashe.csv", sep='\t', encoding="utf8")
# df = df.drop('ff', axis=1)
print(df)
df.to_sql(name='table_test', con=engine, if_exists='replace', index=False)
