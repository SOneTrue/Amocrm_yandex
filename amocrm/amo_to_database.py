import pandas as pd
from sqlalchemy import create_engine

from amocrm.column_drop import column
from config import load_config

# Establish a connection
config = load_config(".env")
database = f'postgresql://{config.db.user_db}:{config.db.password_db}@{config.db.address_db}:{config.db.port_db}/{config.db.name_db}'
engine = create_engine(database)

# Read the excel file
df_csv = pd.read_csv(r'./amocrm_export_leads.csv', encoding="utf-8")
df_csv = df_csv.drop(column, axis=1)
print(df_csv)

try:
    df_csv.to_sql(name='excel', con=engine, if_exists='append', index=False)
except:
    df_csv.to_sql(name='excel', con=engine, if_exists='replace', index=False)
