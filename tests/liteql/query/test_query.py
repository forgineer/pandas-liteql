import logging
import pandas as pd
import pandas_liteql as lql
import unittest


# Enable console logging at DEBUG level
logging.basicConfig(level=logging.DEBUG)


class TestLiteQLQuery(unittest.TestCase):
    def test_query(self):
        """
        Test of querying a data set from the in-memory SQLite session.

        After loading a table into the in-memory SQLite session, a query can be submitted against the table and return
        a pandas DataFrame with the resulted data.
        """
        people_df = pd.read_csv(filepath_or_buffer='../people.csv')

        people = lql.load(df=people_df, table_name='people', index=False)
        #print(people.schema)

        people_over_30_df = lql.query('SELECT id, email, age FROM people WHERE age > 30')
        #print(people_over_30_df)

        self.assertIsInstance(people_over_30_df, pd.DataFrame)

    def test_query_w_pandas_args(self):
        """
        Test of querying a data set from the in-memory SQLite session with the addition of pandas arguments passthrough.

        The 'query' function is a wrapper around the 'read_sql' pandas method and should support additional keyword args
        supported by pandas.
        """
        people_df = pd.read_csv(filepath_or_buffer='../people.csv')

        people = lql.load(df=people_df, table_name='people', index=False, if_exists='replace')
        #print(people.schema)

        # The 'sql' argument supports using the table name as the query and enables column selection
        people_over_30_df = lql.query(sql=f'{people.name}', columns=['id', 'email', 'age'])
        #print(people_over_30_df)

        self.assertIsInstance(people_over_30_df, pd.DataFrame)

    def test_query_join_tables(self):
        """
        Test of querying or joining two tables within the same shared in-memory SQLite session.
        """
        people_df = pd.read_csv(filepath_or_buffer='../people.csv')
        cars_df = pd.read_csv(filepath_or_buffer='../cars.csv')

        # Multiple pandas DataFrames can be loaded into the same in-memory SQLite session
        people = lql.load(df=people_df, table_name='people', index=False, if_exists='replace')
        cars = lql.load(df=cars_df, table_name='cars', index=False, if_exists='replace')

        prepared_sql = f"""
            SELECT
                p.id
                , p.first_name
                , c.make
                , c.model
                , c.year
            FROM {people.name} p
            INNER JOIN {cars.name} c
                ON p.id = c.people_id
        """

        # With two tables loaded inside the shared in-memory SQLite session, they can both be joined together.
        people_with_cars = lql.query(sql=prepared_sql)
        #print(people_with_cars)

        self.assertIsInstance(people_with_cars, pd.DataFrame)

    def test_query_datetime(self):
        """
        Test of querying a table with datetime parameters.
        """
        people_df = pd.read_csv(filepath_or_buffer='../people.csv')

        # Optional conversion of the datetime field to datetime data type prior to loading
        #people_df['create_datetime'] = pd.to_datetime(people_df['create_datetime'], format='%Y-%m-%dT%H:%M:%SZ')

        people = lql.load(df=people_df, table_name='people', index=False, if_exists='replace')

        # SQLite does not support date or datetime data types, but offers the 'date()' function for date conversion
        people_created_before_2021 = lql.query(sql=f"""
            SELECT * FROM {people.name} 
            WHERE create_datetime < datetime('2021-01-01 00:00:00')
            ORDER BY create_datetime
        """)
        #print(people_created_before_2021)

        self.assertIsInstance(people_created_before_2021, pd.DataFrame)

    def test_query_agg(self):
        """
        Test of querying a table with aggregate functions.
        """
        people_df = pd.read_csv(filepath_or_buffer='../people.csv')

        people = lql.load(df=people_df, table_name='people', index=False, if_exists='replace')

        # SQLite does not support date or datetime data types, but offers the 'date()' function for date conversion
        people_count = lql.query(sql=f'SELECT COUNT(*) FROM {people.name}')
        people_age_agg = lql.query(sql=f'SELECT MIN(age), MAX(age), AVG(age) FROM {people.name}')
        people_index_by_gender = lql.query(sql=f"""
            SELECT 
                gender
                , GROUP_CONCAT(id) as ids 
            FROM {people.name}
            WHERE gender is not NULL
            GROUP BY gender
            ORDER BY gender
        """)

        #print(people_count)
        #print(people_age_agg)
        #print(people_index_by_gender)

        self.assertIsInstance(people_count, pd.DataFrame)
        self.assertIsInstance(people_age_agg, pd.DataFrame)
        self.assertIsInstance(people_index_by_gender, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
