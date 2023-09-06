import logging
import pandas as pd
import pandas_liteql as pl

#print(type(pl.LITEQL_ENGINE))

logging.basicConfig(level=logging.DEBUG)

people_df = pd.DataFrame({
    'id': [1, 2],
    'name': ['Blake', 'Melinda'],
    'age': [37, 35]
})

address_df = pd.DataFrame({
    'id': [1, 2],
    'address_line1': ['4011 NW 95th Ter', '4011 NW 95th Ter'],
    'people_id': [1, 2]
})

people = pl.load(df=people_df, table_name='people')
address = pl.load(df=address_df, table_name='address')

print(people.columns)

prepared_sql = f"""
SELECT
    p.id
    , p.name
    , p.age
    , a.address_line1
FROM {people.name} p
INNER JOIN {address.name} a
    ON p.id = a.people_id
"""

people_address = pl.query(sql=prepared_sql)

print(people_address)

one_person = people_df.liteql.sql("SELECT * FROM liteql LIMIT 1")
one_address = address_df.liteql.sql("SELECT * FROM liteql LIMIT 1")

print(one_person)
print(one_address)
