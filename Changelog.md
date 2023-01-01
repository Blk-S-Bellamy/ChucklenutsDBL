# Changelog of Chucklenuts_DBL

## Version 0.2, **01/01/23** 

**ADDITIONS:**
* Added "cond_input()" which is used for entering data into a database only when it is not already there. Any of the passed input variables can be used as a condition when submitting the variables and the function is capable of inputing data from tuples containing a mix of lists and static variables.
refer to the wiki for documentation and usage.
* Added "in_tuple()" to generate a list of tuples with a combination of lists and static variables. Useful for database insertion using "input_mult()". refer to the wiki for documentation and usage

*ALIASES* (can call functions with alternate names)
* Added "rds()" function alias for "refresh_database_structures()".
* Added "fds" function alias for "find_database_structure".
* Added "dbt" function alias for "database_terminal()".
* Added "g_dbv" function alias for "generate_db_visualizer()".
* Added "t_man()" function alias for "terminal_manager()".

**FIXES**
* Fixed visual error in "terminal_manager" function
* Fixed sel_one() bug which returned "True" when the selection returned nothing 

**CHANGES:**
* Changed the order of functions to organize by type and function level

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

