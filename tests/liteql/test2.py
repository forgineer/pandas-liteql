import logging
import pandas as pd
import pandas_liteql as pl

#print(type(pl.LITEQL_ENGINE))

logging.basicConfig(level=logging.DEBUG)

people_df = pd.read_csv(filepath_or_buffer='../people.csv')
cars_df = pd.read_csv(filepath_or_buffer='../cars.csv')

people = pl.load(df=people_df, table_name='people')
cars = pl.load(df=cars_df, table_name='cars')

#print(people.columns)
#print(cars.columns)

join_cars = f"""
SELECT *
FROM {people.name} p
LEFT JOIN {cars.name} c
    ON p.id = c.people_id
LIMIT 10
"""

joined_df = pl.query(join_cars)

print(joined_df)

joined_df.to_csv(path_or_buf='joined_df.csv')
