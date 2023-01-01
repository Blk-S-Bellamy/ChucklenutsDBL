# Chucklenuts_DBL
A Python-based database management system utilizing sqlite3 module. Allows easy creation, deletion, and managment of database components and powerful console based applications for db interactions. This program stands out as an easy and fast solution to small application usages due to its tools for database visualization, creation and interaction.

* Use functions for easy integration of a database into a program without the code bloating of direct integration into native functions
* Easily change database structure in seconds and update with a single function
* Search the database structure and data using console based tools, allowing remote maintenance.
* Have the entire database structure simplified so you can focus on your project, not missing data, tables, or sqlite errors!

* 🔺 CNDBL is under continuing development and as such, will have more features and branches added in the future. Any suggestions are greatly appreciated.

* 🔺 NOTE: Although incredibly fast, Sqlite3 for python is not capable of simultaneous database fetch requests and for this reason, this is not for applications such as web applications or any programs in need of multiple data requests in a single instance! For these uses, A MySQL database would be a better option.

*Need help with functions, setup, bugs, or suggestions? Visit the wiki and take a look around. All in-depth documentation is stored there and updates will see new content there*

## [Written in Python 3](https://docs.python.org/3/index.html)
<img src="https://i.imgur.com/NfdERT5.png" width="150px" align="center">

## [Uses Sqlite3 for Python](https://docs.python.org/3/library/sqlite3.html)
<img src="https://i.imgur.com/RA8FlnE.png" width="150px" align="center">

## Written on Linux for Linux (Windows being tested)
<img src="https://i.imgur.com/BNQ8q8W.png" width="150px" align="center">

## Create A Database in Moments!
Easily create multiple databases filled with custom tables and variables simply by adding variables, tables, and databases to lists and running the setup! 
All commands for database creation are handled by the program meaning, when a change is made to the structure, a function call will add the needed components.

<img src="https://i.imgur.com/qxmRary.png" width="1080px" align="center">

## Terminal Search Tool
Use a terminal based search tool to explore all characteristics of your database and generate full visual charts of the structure in a fraction of a second. This is a user friendly and console based utilizing the "poke_dbs()" function for finding certain database characteristics including list of all databases, all tables in a database, all variables in a database with their datatype, and generate sample commands for inputting data. A versatile and practical tool making bug testing and exploration of database structure easy.

<img src="https://i.imgur.com/CkNzmm6.png" width="1080px" align="center">

<img src="https://i.imgur.com/Ho5I6Wo.png" width="1080px" align="center">

## Data Search Tool
Using the console, switch between database, search for variables in the databases or use other sql commands. Multiple commands can be added to a queue and the queue altered before submission of command list. If you want to save results simple choose the option to save as a text file. Ease of use and simple but powerful console-graphical interface make this function a breeze to utilize. 

<img src="https://i.imgur.com/gr4RmlB.png" width="1080px" align="center">

<img src="https://i.imgur.com/EC86pxf.png" width="1080px" align="center">


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

