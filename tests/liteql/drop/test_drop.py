import logging
import pandas as pd
import pandas_liteql as lql
import sqlalchemy.exc
import unittest


# Enable console logging at DEBUG level
logging.basicConfig(level=logging.DEBUG)


class TestLiteQLDrop(unittest.TestCase):
    def test_drop(self):
        """
        Test of dropping a table from the in-memory SQLite session.

        After loading a DataFrame as a table to the in-memory SQLite database, the table will be dropped
        and no longer available to query
        """
        people_df = pd.read_csv(filepath_or_buffer='../people.csv')

        people = lql.load(df=people_df, table_name='people')

        # Proof of no exception when querying existing table
        names_df = lql.query(f'SELECT first_name FROM {people.name}')

        lql.drop(table_name=f'{people.name}')

        # Assert that the liteql table was successfully removed
        # by asserting on SQLAlchemy OperationalError (table not found)
        with self.assertRaises(sqlalchemy.exc.OperationalError):
            names_df = lql.query(f'SELECT first_name FROM {people.name}')


if __name__ == '__main__':
    unittest.main()
