header_identifier = 13241241434555123123  # not yet important

# contains databases and their tables. the keys define the database names, the values are lists with the pre-defined table names from "custom_tables"

# !!DB NAMES MUST END IN .db OR CONFIG IS NOT VALID!!
# contains all databases the user wants to create and a list with the tables to be put in each
custom_databases = {'testing.db': ['tdata', 'adata'],
                    'testing2.db': ['tdata'],
                    'testing3.db': ['test1', 'test2', 'test3']
                   }

# keys are defining table names, values are the names of defined variables from "custom_vars"
custom_tables = {'tdata': ["firstname", "lastname"],
                 'adata': ["t1", 't2'],
                 'test1': ["aa", "bb"],
                 'test2': ["aa", "t1"],
                 'test3': ["bb", "t2"]
                }

# custom variables for table construction. the keys are the variable names, the values are the type of data being stored from "vars_types".
custom_vars = {"firstname": "str",
               "lastname": "str",
               "t1": "int",
               "t2": "int",
               "aa": "str",
               "bb": "images"
              }

# default available variables types for variable construction. All sqlite3 data types are represented
vars_types = {"str": "TEXT",
              "int": "INTEGER",
              "float": "REAL",
              "null": "NULL",
              "images": "BLOB"
              }


