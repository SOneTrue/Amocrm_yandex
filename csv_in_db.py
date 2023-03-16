import pandas as pd
from sqlalchemy import create_engine

# Establish a connection
password = 'root'
engine = create_engine(f'postgresql://test:{password}@localhost:5432/test')
# conn = psycopg2.connect(database="postgres", user="postgres", password="root123!@#", host="localhost", port="5432")
# Create a new cursor
# Read the excel file
with open("cashe.csv", 'r') as f:
    with open("cashe_new.csv", 'w') as f1:
        next(f)  # skip header line
        for line in f:
            f1.write(line)
df = pd.read_csv("cashe_new.csv", sep='\t', encoding="utf8")
print(df)
df.to_sql(name='table_test', con=engine, if_exists='replace', index=False)
