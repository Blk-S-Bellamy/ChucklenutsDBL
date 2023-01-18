# Welcome
Thanks for using CNDBL, the following are the basics of using the program. Sticking to common sense is all that is needed to utilize the useful functions and for that reason, A lot of errors can be avoided simply by thinking about what one is doing.

## Function Types
The CNDBL source code functions are always one of three types:

1. __**Core Function**__

These are the heart of CNDBL capabilities and are called by a user for everything from database creation to inputting information to a file. All of the core function can be found in the wiki.

2. __**Secondary Function**__

Although these can serve important roles, they are designed as small functions to outsource tasks off a core function. Most of these are specialized to helping a function to such a degree that their use case is limited and for this reason, secondary functions are not included in the user guide as callable functions.

3. __**Tool Functions**__

Small console programs launched with a single function. This allows remote access and data analysis through a fast, efficient method. Tools use core functions to operate but provide a UI with which to use them.

## __Functions__
All of the current functions will be listed here. Any other not listed are not made for use by a user but instead secondary functions to accomplish important specific tasks.
```python
# when using CNDBL as an import, it is advisable to redefine the library as something simple. like so:
import cndbl

cn = cndbl

# to call a function, just add a '.' and the function name:
cn.program_info() 


```


### 🔻program_info
Print the CNDBL the program information to the console/terminal

EXAMPLE:
```python
program_info()
```
🔠SYNTAX:` program_info()`

🔁RETURNS:` None`

### 🔻setup
Print setup information to the console screen.

EXAMPLE:
```python
setup()
```
🔠SYNTAX:` setup()`

🔁RETURNS:` None`

### 🔻refresh_database_structures
All database structures defined in the setup will be created if they do not already exist.

EXAMPLE:
```python
refresh_database_structures()
```
🔠SYNTAX:` refresh_database_structures()`

🔁RETURNS:` None`

### 🔻in_tuple
Will use input tuples with lists or a mix of lists and variables to generate tuples.

EXAMPLE: 
```python
# generate a list of tuples using all lists
list1 = [1, 2, 3]
list2 = ["a", "b", "c"]
tuples = in_tuple((list1, list2))
# this would generate:
[(1, "a"), (2, "b"), (3, "c")]

# Generating using a mix:
list1 = [1, 2, 3]
tuples = in_tuple((list1, "CNDBL"))
# this would generate:
[(1, "CNDBL"), (2, "CNDBL"), (3, "CNDBL")]
```

🔠SYNTAX:` in_tuple(variable_list)`

🔁RETURNS:` tuple_list`

### 🔻input_one
input one tuple into a database table, tuple should contain an input for every variable in the database table.
EXAMPLE: if inputting into a table with variables 'v1|v2|v3|v4' the tuple would be (str, str, str, str).

EXAMPLE:
```python
# a database named general has been created with a table called tdata. 
# the variables in tdata are, `|name, TEXT|place, TEXT|timestamp, REAL|`

tuple_ = ('bob', 'US', 1670650011)

insert_one('general', 'tdata', tuple_)
```
TABLE:
|(rowid)|name|place|timestamp|
| --- | --- | --- | --- |
|0|bob|US|1670650011|
|1||||

🔠SYNTAX:` input_one(db_name, table, insert_tuple) `

🔁RETURNS:` boolean`

### 🔻input_mult
insert a list of tuples into a database table. Tuples should contain an input for every variable in the database table. if inputting into a table with variables '|v1|v2|v3|v4|' the tuple would be (str, str, str, str). After constructing all tuples, simply put them into a list like so: [(),(),()] and pass to the function.

EXAMPLE: 
```python
# a database named general has been created with a table called tdata. 
# the variables in tdata are, `|name, TEXT|place, TEXT|timestamp, REAL|`

tuple_list = [('bob', 'US', 1670650011), ('steve', 'UK', 1670650011)]

insert_mult('general', 'tdata', tuple_list)
```

TABLE:
|(rowid)|name|place|timestamp|
| --- | --- | --- | --- |
|0|bob|US|1670650011|
|1|steve|UK|1670650011|
|2||||

🔠SYNTAX:` input_mult(db_name, table, list_of_tuples)`

🔁RETURNS:` boolean`

### 🔻db_sel
Select data from a database and return the result. The input can be a list of query or a single query in the form of a string, the function will detect whichever is passed. If the function failed, a False will be returned but if commands go through, a True will be returned.

```python
# selecting with a single command from a database "general.db" and table "sessions"
results1 = db_sel('general', 'SELECT * FROM SESSIONS')

# selecting with a list of commands from a database "general.db" and table "sessions"
commands = ['SELECT * FROM SESSIONS', 'SELECT name FROM SESSIONS LIMIT 3']
results2 = db_sel('general', commands)
```
🔠SYNTAX:` db_sel(database_name, query_string)` OR `db_sel(database_name, query_list)`

🔁RETURNS:` boolean, results`

### 🔻db_ex
Execute a command in a database or list of commands. The input can be a list of commands or a single command in the form of a string, the function will detect whichever is passed. If the function failed, a False will be returned but if commands go through, a True will be returned.

```python
# executing a single command in a database "general.db" with a table "sessions"
db_ex('general', 'DELETE FROM sessions')

# executing a list of commands in a database "general.db" with a table "sessions"
commands = ['DELETE FROM SESSIONS', 'DROP TABLE sessions']
db_ex('general', commands)
```
🔠SYNTAX:` db_ex(database_name, command_string)` OR `db_ex(database_name, command_list)`

🔁RETURNS:` boolean`

### 🔻cond_input()
(Added V-0.2)
Allows data to be submitted only if it is not already in the database. Function can be used to submit data in list form or in single tuple form. Custom errors will assist in any syntax errors a user may write.

TABLE: (figure 1, database:"employees.db", table:"information")
|(rowid)|name|place|timestamp|
| --- | --- | --- | --- |
|0|bob|US|1670650011|
|1|steve|UK|1670650011|
|2||||

The database name and table name are self explanatory. The insert tuple is a tuple with the variables to be inserted into the table. It must have the same number of variables as the table. For example: figure 1 would need a tuple with 3 total variable OR list OR a mix (var, var, var) OR (var, list, var) OR (list, list, list)

**Tuple with no Lists**
* A user can simply use a tuple with all the values to be input in it and the function will check against the database and either submit the data or not depending on it's presence in the database. For example: ("bob", "US", 1670650011) contains all static variables.

**Tuple with Lists**
* A user can have a list or lists in place of a variable in the tuple. This will allow a user to submit vast amounts of data without converting to tuples first. The lists will be used to make as many tuples as the list or lists are long and the static variable(s) passed will be the same in all the tuples when they are compared and submitted or rejected. For example: ("bob", list, 1670650011) and list = ["US", "UK"] would create ("bob", "US", 1670650011) and ("bob", "UK", 1670650011). One can replace all static variables with lists as long as the lists are the same length.

**conditions_index**
* A list containing the indexes of the insert tuple variables a user wants to be checked before submitting the data tuple to the database. For example: if submitting a single tuple: ("bob", "US", 1670650011) using [0, 1, 2] OR a range ["0:2"] will search the database for a row containing all three tuple variables and will only submit the tuple to the database if one does not exist.

* If using lists in an insert tuple, the same applies. For example: if a tuple with ("bob", list, 1670650011) and condition list [0, 1, 2] is used, the list will be used to generate as many tuples as there are items in the list and each tuple will then be treated the same way.


EXAMPLE:
```python
# submitting data using a single tuple
# because a row with "bob", "US" and 1670650011 already exists in our table (figure 1) it would not be input into the database
cond_input("employees", "information", ("bob", "US", 1670650011), [0, 1, 2])
# one could also use the following conditions_index for the same result: ["0:2"], [0, "1:2"]

# submitting data using data lists and static variables
names = ["bob", "tom"]
countries = ["US", "UK"]
cond_input("employees", "information", (names, countries, 1670650011), ["0:2"])

# the following tuples would be generated and then index 0 through 2 would be searched to see if all appear in a single row before submitting
("bob", "US", 1670650011)
("tom", "UK", 1640610020)
# only "tom" would be added to the database because there is no row matching the selected condition of 0:2 (figure 1)

```
🔠SYNTAX:` cond_input(database_name, table_name, insert_tuple, conditions_index)`

🔁RETURNS:` None`

### 🔻db_findpath
Return the path to a database if it exists.  the database name returned is the name with '.db' attached. Example: 'testing' >returns> 'testing.db'. The function will work without '.db' at the end of the database_name.

EXAMPLE:
```python
# a database named general has been created with a table called tdata.

# dbname checks and makes sure the input ends in ".db" and if not, adds ".db" and returns the name
# t_f is if that database exists or not
t_f, dbname, pathway = db_findpath('general')
```

🔠SYNTAX:` db_pathfinder(database_name)`

🔁RETURNS:` database_name, database_path`

### 🔻find_database_structure
Return all database, tables, variables, and their data types in the form of a nested list.

EXAMPLE:
```python
# all databases defined in the setup of CNDBL will be included in the list
st = find_database_structure()
print(st)
```

🔠SYNTAX:` find_database_structure()`

🔁RETURNS:` structure_string`

### 🔻generate_db_visualizer
Return a printable variable showing a flow chart of all programmed databases, their tables, variables, and data types.

EXAMPLE:
```python
# all databases defined in the setup of CNDBL will be included in the database visualizer string
db_v = generate_db_visualizer()
print(db_v)
```

🔠SYNTAX:` generate_db_visualizer()`

🔁RETURNS:` boolean, printable_string`

### 🔻poke_dbs
Search for a all databases, tables in a database, or variable-type sets in a table by leaving the table, or table and database_name variables in the function call as an empty string.

```python
# find all databases defined in startup section:
t_f, databases = poke_dbs('', '')

# find all tables in a predefined database called 'general'
t_f, tables = poke_dbs('general', '') 

# find all variables and their types in a database 'general' and table 'tdata'
t_f, var = poke_dbs('general', 'tdata')

# a user input can be confirmed to be a real database through using the return boolean to loop until the database can be found
confirmed = False
while not confirmed:
    dbi = input('Please type the name of a database')
    t_f, database = poke_dbs(dbi, '')
    
    # check to make sure the user input something and it corresponds with a database
    if t_f is False or dbi == '':
        pass
    else:
        confirmed = True
```

🔠SYNTAX:` poke_dbs(database_name, table)`

🔁RETURNS:` boolean, results`

### 🔻poke_dbs_ui
Call a terminal based tool which enables easy searching without repeated function calls. Also provides additional information regarding table variables.

Example:
```python
poke_dbs_ui()
```
🔠SYNTAX:` poke_dbs_ui()`

🔁RETURNS:` None`

### 🔻database_terminal
Call a terminal based tool which allows the entering of SQL commands individually or in succession using a command queue. Other uses are for fetching and exporting database information without writing and running code.

Example:
```python
database_terminal()
```
🔠SYNTAX:` database_terminal(database_name)`

🔁RETURNS:` None`

### 🔻terminal_manager
Call a terminal based tool which allows opening and closing database SQL terminals in all the CNDBL databases with a UI. a database selector menu for database_terminal().

Example:
```python
terminal_manager()
```
🔠SYNTAX:` terminal_manager()`

🔁RETURNS:` None`


