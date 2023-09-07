import sqlalchemy
import unittest

from pandas_liteql import liteql as lql

"""
Testing the creation of the SQLAlchemy engine (LITEQL_ENGINE) instance
"""
class TestLiteQLEngine(unittest.TestCase):
    def test_engine(self):
        self.assertIsInstance(lql.LITEQL_ENGINE, sqlalchemy.engine.Engine)


if __name__ == '__main__':
    unittest.main()