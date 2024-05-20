import logging
import pandas as pd
import pandas_liteql as lql
import sqlalchemy
import unittest


# Enable console logging at DEBUG level
logging.basicConfig(level=logging.DEBUG)


class TestLiteQLLoad(unittest.TestCase):
    def test_load(self):
        """
        Test of loading a data set to the in-memory SQLite session.

        Upon loading a DataFrame (without error), a LiteQL class object should be created containing:
        1. The name of the table.
        2. A pandas DataFrame of the table schema as loaded by SQLAlchemy.
        """
        people_df = pd.read_csv(filepath_or_buffer='../people.csv')

        people = lql.load(df=people_df, table_name='people')

        logging.info(f'Table name: {people.name}')
        #print(people.schema)

        people.log_schema()

        self.assertIsInstance(people, lql.LiteQL)
        self.assertEqual(people.name, 'people')
        self.assertIsInstance(people.schema, pd.DataFrame)

    def test_load_w_pandas_args(self):
        """
        Test of loading a data set to the in-memory SQLite session with the addition of pandas arguments passthrough.

        The 'load' function is a wrapper around the 'to_sql' pandas method and should support additional keyword args
        supported by pandas.
        """
        people_df = pd.read_csv(filepath_or_buffer='../people.csv')

        # Define table schema change
        schema = {"invoice_amount": sqlalchemy.types.BIGINT}

        people = lql.load(df=people_df, table_name='people',
                          index=False, dtype=schema, if_exists='replace')

        logging.info(f'Table name: {people.name}')
        #print(people.schema)

        people.log_schema()

        self.assertIsInstance(people, lql.LiteQL)
        self.assertEqual(people.name, 'people')
        self.assertIsInstance(people.schema, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
