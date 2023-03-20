import pandas as pd
from sqlalchemy import create_engine

# Establish a connection
password = 'root'
engine = create_engine(f'postgresql://test:{password}@localhost:5432/test')

# Read the excel file
df = pd.read_csv("yandex_data.csv", sep='\t', encoding="utf8")
# df = df.drop('ff', axis=1)
print(df)
try:
    df.to_sql(name='table_test', con=engine, if_exists='append', index=False)
except:
    df.to_sql(name='table_test', con=engine, if_exists='replace', index=False)
