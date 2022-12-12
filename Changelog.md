# Changelog of Chucklenuts_DBL

### Version 0.1, **12/11/22**

**ADDITIONS:**

* Added "db_sel()" to select and return results for either a list of commands or a single command. Both can be used
* Added "db_ex()" to run commands in a database easily and catch errors. Can run a list of commands or a single command string

**CHANGES:**
* Added a failsafe to find and inform user of table names not accepted by Sqlite.
* Added a failsafe to catch when variables mentioned in table creation are not in the variable dictionary
	and prints the information before terminating
* Added a failsafe to catch when tables in db_and_table_list and table_variable_keys don't match
* Removed commands() function in favor of referencing the CNDBL wiki


### BETA

Initial launch of CNDBL with most basic features and tools.

