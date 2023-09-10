import logging
import pandas as pd
import pandas_liteql as lql
import unittest


# Enable console logging at DEBUG level
logging.basicConfig(level=logging.DEBUG)


class TestLiteQLAccessor(unittest.TestCase):
    def test_accessor(self):
        """
        Test of querying a DataFrame with the liteql accessor extension.

        Using the 'sql' method within the liteql accessor performs the 'load' and 'query' functions in succession
        to easily query and return the results back as a pandas DataFrame. However, it does not allow for the
        passthrough of additional arguments to pandas methods at work under the hood.
        """
        people = pd.read_csv(filepath_or_buffer='../people.csv')

        people_under_18 = people.liteql.sql('SELECT id, first_name, age FROM liteql WHERE age < 18')
        #print(people_under_18)

        self.assertIsInstance(people_under_18, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
