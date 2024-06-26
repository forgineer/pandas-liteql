<div align="center">
    <img src="https://forgineer.pythonanywhere.com/static/pandas_liteql/pandas-liteql-feather-logo-large.png" alt="pandas-liteql-logo.png"><br>
</div>

---

# What is pandas-liteql?
**pandas-liteql** is a simple [pandas](https://pandas.pydata.org/) extension that enables users to execute SQL statements against DataFrames using in-memory [SQLite](https://www.sqlite.org/index.html). It is meant to streamline data manipulation and analysis tasks. For more detailed information and examples on **pandas-liteql**, visit the [documentation pages](https://forgineer.pythonanywhere.com/pandas-liteql).

# What pandas-liteql is not
**pandas-liteql** is not a competitor to libraries such as [PySpark](https://spark.apache.org/docs/latest/api/python/index.html) or [DuckDB](https://duckdb.org/) that can perform SQL queries on larger data sets and perform more advanced data science use-cases. Rather, it is inspired by those projects and similar libraries that have performed the same function, but have since been abandoned or were not as user-friendly.

# Installing pandas-liteql
**pandas-liteql** requires a minimum of Python 3.7 and the following libraries:

| Library    | Version      |
|------------|--------------|
| Pandas     | `>= 1.3.5`   |
| SQLAlchemy | `>= 1.4.36`  |

Assuming these prerequisites are already installed, adding **pandas-liteql** is as simple as...

```
pip install pandas-liteql
```

# Examples
Below are some usage examples to load, query, and drop data from the in-memory SQLite sessions established with **pandas-liteql** and pandas DataFrame integration.

## Loading
Start by loading your DataFrame with the `load` function. When **pandas-liteql** is imported, an in-memory SQLite session is created where data can be loaded to.

```python
import pandas as pd
from src import pandas_liteql as lql

# Data set creation
person_data = {
    'name': ['Bill', 'Ted', 'Abraham', 'Genghis', 'Napoleon'],
    'age': [25, 24, 56, 64, 51],
    'email': ['bill@excellent.com', 'ted@excellent.com',
              'lincoln@excellent.com', 'khan@excellent.com',
              'bonaparte@excellent.com']
}

# DataFrame creation
person_df = pd.DataFrame(data=person_data)

# Loading the DataFrame to in-memory SQLite as the 'person' table
# The 'person' variable is also a LiteQL class containing the table name and schema information
person = lql.load(df=person_df, table_name='person')

print(f'Table name: {person.name}')
print(person.schema)
```

Output:
```
Table name: person
    name    type  nullable default autoincrement  primary_key
0  index  BIGINT      True    None          auto            0
1   name    TEXT      True    None          auto            0
2    age  BIGINT      True    None          auto            0
3  email    TEXT      True    None          auto            0
```

## Querying
Next, query the table using the `query` function. Using SQL syntax, the loaded table can be queried and the results will be returned as a pandas DataFrame.

```python
bill_and_ted = lql.query(sql='SELECT * FROM person WHERE age < 30')

print(bill_and_ted)
```

Output:
```
   index  name  age               email
0      0  Bill   25  bill@excellent.com
1      1   Ted   24   ted@excellent.com
```

## Dropping
If finished with a table within the flow of a script, you can simply drop it with the `drop` function to preserve memory.

```python
lql.drop(table_name='person')
```

## The DataFrame SQL Accessor
Lastly, for a more simplistic approach, you can use the `liteql.sql` accessor to perform the same functions above in one line and return the result as a pandas DataFrame. This approach requires that you query from the `liteql` table that is loaded from the DataFrame, queried, and then dropped.

```python
import pandas as pd
import pandas_liteql as lql

# Data set creation
person_data = {
    'name': ['Bill', 'Ted', 'Abraham', 'Genghis', 'Napoleon'],
    'age': [25, 24, 56, 64, 51],
    'email': ['bill@excellent.com', 'ted@excellent.com',
              'lincoln@excellent.com', 'khan@excellent.com',
              'bonaparte@excellent.com']
}

# DataFrame creation
person_df = pd.DataFrame(data=person_data)

bill_and_ted = person_df.liteql.sql('SELECT * FROM liteql WHERE age < 30')

print(bill_and_ted)
```

Output:
```
   index  name  age               email
0      0  Bill   25  bill@excellent.com
1      1   Ted   24   ted@excellent.com
```


# Contributing
Currently, **pandas-liteql** will not be receiving any additional updates. Contributions will not be accepted here, but feel free to fork this project if you desire.
