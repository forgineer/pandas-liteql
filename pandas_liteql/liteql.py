import logging
import pandas
import sqlalchemy

from typing import Any


# Define the SQLAlchemy engine for LiteQL (in-memory sqlite under the hood)
LITEQL_ENGINE = sqlalchemy.create_engine('sqlite:///:memory:')


class LiteQL:
    name: str
    schema: pandas.DataFrame

    def __init__(self, table_name: str):
        self.name = table_name

        liteql_inspect = sqlalchemy.inspect(LITEQL_ENGINE)
        columns_table = liteql_inspect.get_columns(table_name)

        self.schema = pandas.DataFrame.from_dict(columns_table)


def lite_logger(func: callable) -> Any:
    def wrapper(*args, **kwargs) -> Any:
        logging.debug(f'Entering LiteQL.{func.__name__}')

        result = func(*args, **kwargs)

        logging.debug(f'Exiting LiteQL.{func.__name__}')

        return result
    return wrapper


@lite_logger
def load(df: pandas.DataFrame, table_name: str, **pandas_args) -> LiteQL:
    """
    Loads a pandas DataFrame to the SQLite in-memory session.

    :param df: A pandas DataFrame.
    :param table_name: The name of the new table.
    :param **pandas_args: Additional pandas keyword arguments related to the pandas.to_sql method.
    :return: A LiteQL class object containing the table name and schema loaded.
    """
    df.to_sql(name=table_name, con=LITEQL_ENGINE, **pandas_args)

    litql_cls = LiteQL(table_name=table_name)

    return litql_cls


@lite_logger
def query(sql: str, **pandas_args) -> pandas.DataFrame:
    """
    Queries the SQLite in-memory session.

    :param sql: An SQLite compatible SQL string.
    :return: A pandas DataFrame containing the queried data.
    """
    # Remove the 'sql' or 'con' arguments if somehow included in 'pandas_args'
    pandas_args.pop('sql', None)
    pandas_args.pop('con', None)

    data = pandas.read_sql(sql=sql, con=LITEQL_ENGINE, **pandas_args)

    return data


@lite_logger
def drop(table_name: str) -> None:
    """
    Drops the table from the SQLite in-memory session (if exists).

    :param table_name: The name of the loaded SQLite table.
    :return: None.
    """
    LITEQL_ENGINE.execute(f'DROP TABLE IF EXISTS {table_name}')


@pandas.api.extensions.register_dataframe_accessor("liteql")
class LiteQLAccessor:
    _df: pandas.DataFrame

    def __init__(self, pandas_obj: pandas.DataFrame):
        self._df = pandas_obj

    def sql(self, accessor_sql: str) -> pandas.DataFrame:
        """
        A method of the liteql accessor (extension) to load and query a pandas DataFrame.

        :param accessor_sql: An SQLite compatible SQL string.
        :return: A pandas DataFrame containing the queried data.
        """
        load(df=self._df, table_name='liteql', if_exists='replace')

        return query(accessor_sql)


if __name__ == '__main__':
    pass
