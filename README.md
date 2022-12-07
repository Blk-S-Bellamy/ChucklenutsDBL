# Chucklenuts_DBL
A Python-based database management system utilizing sqlite3 module. Allows easy creation, deletion, and managment of database components and powerful console based applications for db interactions. This program stands out as an easy and fast solution to small application usages due to its tools for database visualization, creation and interaction.

<img src="https://i.imgur.com/NfdERT5.png" width="150px" align="center">

## Written in Python 3

<img src="https://i.imgur.com/RA8FlnE.png" width="150px" align="center">

## Uses Sqlite3 for Python

<img src="https://i.imgur.com/BNQ8q8W.png" width="150px" align="center">

## Written on Linux for Linux (Windows being tested)

Variable Creation
```python
table_variables_dict = {1: ["data", "TEXT"],
                  	2: ["active", "TEXT"],
		        3: ["unix", "INTEGER"],
		        4: ["event", "TEXT"]}
```
Table Creation
```python
table_variable_keys = {'runtime_log': [1, 2, 3],
		       'sessions': [2, 1],
		       'crash_logs': [4, 1]}
```
Database Creation
```python
db_and_table_list = [('general.db', ['sessions', 'runtime_log', 'crash_logs'])]
```
