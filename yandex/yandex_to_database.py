import pandas as pd
from sqlalchemy import create_engine

# Establish a connection
password = 'root'
engine = create_engine(f'postgresql://test:{password}@localhost:5432/test')

# Read the excel file
df1 = pd.read_csv("./yandex_data_one.csv", sep='\t', encoding="utf8")
df2 = pd.read_csv("./yandex_data_two.csv", sep='\t', encoding="utf8")
df3 = pd.read_csv("./yandex_data_three.csv", sep='\t', encoding="utf8")
print(df1)
print(df2)
try:
    df1.to_sql(name='table_test', con=engine, if_exists='append', index=False)
    df2.to_sql(name='table_test', con=engine, if_exists='append', index=False)
    df3.to_sql(name='table_test', con=engine, if_exists='append', index=False)
except:
    df1.to_sql(name='table_test', con=engine, if_exists='replace', index=False)
    df2.to_sql(name='table_test', con=engine, if_exists='append', index=False)
    df3.to_sql(name='table_test', con=engine, if_exists='append', index=False)
