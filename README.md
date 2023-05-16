# Welcome
<img src="https://i.imgur.com/vrASZMW.jpg" width="750px" align="center">

# Version 0.4 re-write

Although version 0.3 contains a full toolbox suite as well as a finctional program, version 0.4 a re-write,will be to supported version going forward. In order to provide a simplistic, readable, tidy, code base that allows for collaboration as well as ease of use for integration into scripts, nearly every line has been rebuilt from the ground up.
***improvements to 0.4
* The core database script is contained within "Chucklenuts_0.4" and has been re-written for readability and performance.
* The toolbox (almost complete, 1-3 days away) is a seperate script which __uses a standalone python resource pack__ to display the graphical aspects meaning, a custom resource pack is straightforward to create.
* The database config (how databases are listed to be built) is a seperate file which allows for easy editing and swapping it out to experiment

***working on
* Finishing the new toolbox script
* Easy config is on the to-do list
* Easy image and file storage is on the to-do list
* pep-8 standard cleanup is on the to-do list
 
A Python-based database management system utilizing sqlite3 module. Allows easy creation, deletion, and managment of database components and powerful console based applications for db interactions. This program stands out as an easy and fast solution to small application usages due to its tools for database visualization, creation and interaction.



# Changelog of Chucklenuts_DBL

## Version 0.4, **05/15/23** 

**NOTE:**
In search of improving the program, the entire library of functions has been redone with a cleaner, and better core. The scripts for database core, toolbox, config, and resource pack have also been moved into different files a better collaborative and user experience. The wiki must be completely redone as well to keep up to date with the program but older versions will still be available.

**0.4 FUNCTIONS**
db.retr_attr()
db.listall()
db.find()
fetch_db_inst()

refresh_database_structures() OR rds()
in_tuple()
serialize()
deserialize()
generate_blank_par()
input_one()
input_mult()
nest_detect()
select_one()
select_all()
execute()
pop_stored()
cond_input()
program_info()

**WORKING ON**
* Finishing the new toolbox script
* Easy config is on the to-do list
* Automatic dependency detection and resolution 
* Easy image and file storage is on the to-do list
* pep-8 standard cleanup is on the to-do list

## Version 0.3, **02/02/23** 

**NOTE:**
Major code restructuring and overall improvements came with 0.3. Also, data serialization is now supported! Python objects can be stored and retrieved from databases using JSON. No [Pickle](https://docs.python.org/3/library/pickle.html) serialization or [Marshal](https://docs.python.org/3/library/marshal.html) object serialization is supported to prevent risk of serialization being used as an attack vecor through stored data as described here: [pickle vuln](https://stackoverflow.com/questions/21752259/python-why-pickle) and [Marshal vuln](https://stackoverflow.com/questions/26931919/marshal-unserialization-not-secure)

**CHANGES:**
* Re-wrote “cond_input()” for efficiency, readability, and made to be modular with support for data serialization with JSON and changed the function.
* Now “cond_input()” does not expand list variables into multiple tuples, "in_tuple()" should be used before submission of data.
* Now “cond_input()” can submit Python objects to the database and retrieve them automatically u4sing JSON serialization.
* Altered multiple functions to have dependency funtions nested for de-cluttering and better scope.
* Altered "database_terminal()" so the command queue prefix is "*" instead of "-"

**FIXES**
* Fixed all PEP8 convention violations

**ADDITIONS:**
* Added “pop_stored()” with the ability to process a list and pass back all the items not in a database table.
* Added “serialize()” with funtion to serialize Python objects in a passed tuple or list of tuples.
* Added “deserialize()” with function to deserialize any viable Python objects in a tuple or list of tuples.
* Added 

**REMOVED**
* "Setup()" removed in favor on online dictionary and lighter weight code.



*ALIASES* (can call functions with alternate names)
* Added "ps()" function call for "pop_stored()"

## 0.2 Patch 1, **01/08/23**

**FIXES**
* Fixed sloppy syntax in "cond_input()"
* Fixes misc errors in "db_sel()"


## Version 0.2, **01/01/23** 

**ADDITIONS:**
* Added "cond_input()" which is used for entering data into a database only when it is not already there. Any of the passed input variables can be used as a condition when submitting the variables and the function is capable of inputing data from tuples containing a mix of lists and static variables.
refer to the wiki for documentation and usage.
* Added "in_tuple()" to generate a list of tuples with a combination of lists and static variables. Useful for database insertion using "input_mult()". refer to the wiki for documentation and usage.

*ALIASES* (can call functions with alternate names)
* Added "rds()" function alias for "refresh_database_structures()".
* Added "fds" function alias for "find_database_structure".
* Added "dbt" function alias for "database_terminal()".
* Added "g_dbv" function alias for "generate_db_visualizer()".
* Added "t_man()" function alias for "terminal_manager()".

**FIXES**
* Fixed visual error in "terminal_manager" function.
* Fixed sel_one() bug which returned "True" when the selection returned nothing .

**CHANGES:**
* Changed the order of functions to organize by type and function level.

## Version 0.1, **12/11/22**

**ADDITIONS:**

* Added "db_sel()" to select and return results for either a list of commands or a single command. Both can be used.
* Added "db_ex()" to run commands in a database easily and catch errors. Can run a list of commands or a single command string.

**CHANGES:**
* Added a failsafe to find and inform user of table names not accepted by Sqlite.
* Added a failsafe to catch when variables mentioned in table creation are not in the variable dictionary
	and prints the information before terminating.
* Added a failsafe to catch when tables in db_and_table_list and table_variable_keys don't match.
* Removed commands() function in favor of referencing the CNDBL wiki.


## BETA

Initial launch of CNDBL with most basic features and tools.



