import logging
import pandas as pd
import pandas_liteql as pl

#print(type(pl.LITEQL_ENGINE))

logging.basicConfig(level=logging.DEBUG)

people_df = pd.read_csv(filepath_or_buffer='../people.csv')

# 2021-03-23T09:26:48Z (date format)

people_df['create_datetime'] = pd.to_datetime(people_df['create_datetime'], format='%Y-%m-%dT%H:%M:%SZ')

#print(people_df.dtypes)

people = pl.load(df=people_df, table_name='people', index=False)

print(people.columns)

people_df = pl.query(f"SELECT * FROM {people.name} where create_datetime < date('2020-03-28 00:00:00')")

print(people_df)