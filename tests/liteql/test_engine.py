import pandas_liteql as lql
import sqlalchemy
import unittest


class TestLiteQLEngine(unittest.TestCase):
    def test_engine(self):
        """
        Testing the creation of the SQLAlchemy engine (LITEQL_ENGINE) instance.

        This engine instance represents a connection to an in-memory SQLite session.
        This instance is created upon importing 'pandas_liteql'.
        """
        self.assertIsInstance(lql.LITEQL_ENGINE, sqlalchemy.engine.Engine)


if __name__ == '__main__':
    unittest.main()
