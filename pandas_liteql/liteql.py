import logging
import pandas
import sqlalchemy

from typing import Literal


# Define the SQLAlchemy engine for LiteQL (in-memory sqlite under the hood)
LITEQL_ENGINE = sqlalchemy.create_engine('sqlite:///:memory:')


class LiteQL:
    name: str
    columns: pandas.DataFrame

    def __init__(self, table_name: str):
        self.name = table_name

        insp = sqlalchemy.inspect(LITEQL_ENGINE)
        columns_table = insp.get_columns(table_name)

        self.columns = pandas.DataFrame.from_dict(columns_table)


def load(df: pandas.DataFrame,
         table_name: str,
         table_schema: dict | None = None,
         if_table_exists: Literal["fail", "replace", "append"] = "fail",
         include_index: bool | None = True,
         chunk_size: int | None = 1000) -> LiteQL:
    """
    Loads a pandas DataFrame to the SQLite in-memory session.

    :param df: A pandas DataFrame.
    :param table_name: The name of the new table.
    :param table_schema: A custom schema defined for the table.
    :param if_table_exists: Behavior when table already exists.
    :param include_index: Indicator to load the pandas index (True) or not (False)
    :param chunk_size: The number of chunks to write into the table at one time.
    :return: The name of the loaded table.
    """
    logging.debug('Entering LiteQL.load')

    df.to_sql(name=table_name,
              con=LITEQL_ENGINE,
              schema=table_schema,
              if_exists=if_table_exists,
              index=include_index,
              chunksize=chunk_size)

    litql_cls = LiteQL(table_name=table_name)

    logging.debug('Exiting LiteQL.load')

    return litql_cls


def query(sql: str) -> pandas.DataFrame:
    """
    Queries the SQLite in-memory session.

    :param sql: An SQLite compatible SQL string.
    :return: A pandas DataFrame containing the queried data.
    """
    logging.debug('Entering LiteQL.query')

    data = pandas.read_sql(sql=sql,
                           con=LITEQL_ENGINE)

    logging.debug('Exiting LiteQL.query')

    return data


@pandas.api.extensions.register_dataframe_accessor("liteql")
class LiteQLAccessor:
    _df: pandas.DataFrame

    def __init__(self, pandas_obj: pandas.DataFrame):
        self._df = pandas_obj

    def sql(self, accessor_sql: str) -> pandas.DataFrame:
        load(df=self._df, table_name='liteql', if_table_exists='replace')

        return query(accessor_sql)


if __name__ == '__main__':
    pass
