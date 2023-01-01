import sqlite3
import time
import os
from pathlib import Path

cndbl_version = '0.2'
cwd = os.path.realpath(os.path.dirname(__file__))

# contains databases and their tables. use function() to view instructions on format
db_and_table_list = [('testing.db', ['tdata'])]

# tables and their variable keys.
table_variable_keys = {'tdata': [1, 2, 3, 4]}

# contained is variables and their data type in accordance with sqlite3 datatype format. these can be called in creation
# of tables as references for their variables
table_variables_dict = {1: ["name", "TEXT"],
						2: ["number", "REAL"],
						3: ["test_par1", "TEXT"],
						4: ["test_par2", "TEXT"]
						}


# clears the console for both Windows and Linux
def clear():
    os.system('clear')


# Make tables and databases if they do not exist as listed in startup section
def refresh_database_structures():
    global db_and_table_list
    # table names not accepted by Sqlite3
    variable_indexes = []
    ls = []
    fixit = ['table']
    fixit_list = []

    nfix = False
    # Make sure all the given table names are allowed and if not, return and print bad table names
    for item in db_and_table_list:
        for thing in item[1]:
            if thing in fixit:
                nfix = True
                fixit_list.append(thing)
            else:
                pass
        if nfix is True:
            errors_ = generate_var_par(fixit_list)
            print(f'::Error:: the following table names are not allowed by Sqlite:\n{errors_}\nterminating...')
            exit()
        else:
            pass

    # contains all finished commands to be executed later
    type_var_list = []

    # command = prefix+table_nm+start_b
    # for every item in bd_table_list, find the database, then grab table names and their variables,
    # types to be passed to command generation
    for database in db_and_table_list:
        type_var_list.clear()
        table_list = database[1]
        database_name = database[0]
        # print('\nVV'+database_name+'VV')

        for table in table_list:
            # print(table)
            try:
                variable_indexes = table_variable_keys[table]
            except KeyError:
                print(f'::Error:: table \"{table}\" in \"db_and_table_list\" is not in \"table_variable_keys\"')
                print('terminating...')
                exit()
            # print(len(variable_indexes))

            type_var_list.clear()
            for index in variable_indexes:
                try:
                    ls = table_variables_dict[index]
                except KeyError:
                    print(
                        f'::Error:: variable \"{index}\" from \"table_variable_keys\" is not in'
                        f' \"table_variables_dict\"')
                    print('terminating...')
                    exit()
                type_var_list.append(ls)

                # will see if all the variables for the current table are added to the list and submit them to be
                # made if they are
                if len(type_var_list) == len(variable_indexes):
                    generate_tables(database_name, table, type_var_list)
                # print(type_var_list)
                else:
                    pass


# constructs the commands from retrieved data. passed database name, passed table name, and passed list of variables
# and variable types
# format for variable+type lists is as follows "[['event', 'TEXT'], ['actor', 'TEXT'], ['unix', 'REAL']]" as an example


# constructs commands from formatted data and executes them
def generate_tables(db_nme, table_name, var_type_list):
    global cwd
    commandslist = []

    # makes sure that '.db is in the name so that the database is accessable by the program. will fix the
    # issue if it isn't'
    if '.db' in db_nme:
        db_name = db_nme
    else:
        db_name = db_nme + '.db'

    db_path = cwd + '/' + db_name

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # create blank command
    prefix = 'CREATE TABLE IF NOT EXISTS '
    start_b = '('
    command = prefix + table_name + start_b

    try:
        for count, item in enumerate(var_type_list):
            variable = item[0]
            var_type = item[1]
            command += variable + ' ' + var_type
            # print(variable, var_type)
            if count == len(var_type_list) - 1:
                command += ')'
            else:
                command += ', '
                pass
            commandslist.append(command)
        # print(command)
        c.execute(command)
    except ValueError as e:
        print('::ERROR:: in generation of sqlite3 command, (' + str(e) + ')')


# print(commandslist)


# will generate the blank question tuple used in insert commands for sqlite3
def generate_blank_par(number):
    variable = '?, ' * number
    v_len = (len(variable) - 2)
    fvariable = variable[0:v_len]
    prefix = '('
    postfix = ')'
    complete = f'{prefix}{fvariable}{postfix}'
    return complete


# generate a tuple from a list of strings and insert the variables into the tuple like so: ['one', 'two']
# >returns> ('one', 'two')
def generate_var_par(var_list):
    postfix = ')'
    body = '('
    for item in var_list:
        body += f'{item}, '

    body = body[0:(len(body) - 2)]
    body += postfix
    return body


# finds the number to represent variables
def db_table_decoder(database, table):
    global db_and_table_list
    # finds numerical representation of the variables used in that table
    keys = table_variable_keys[table]
    # finds the actual variables and their types for use in database construction
    variables = [table_variables_dict[item] for item in keys]
    # print(variables)

    return database, table.upper(), variables


# will return an array of lists with a database and their tables, and variables
def find_database_structure():
    global db_and_table_list

    # this section will find all the database, their tables, variables, types, and format the results to be read
    # in creation of visualizers
    structure_list = []
    for entry in db_and_table_list:

        temp = []
        for table in entry[1]:
            # each loop gathers a table and it's variables into a tuple to be used for other functions
            table_info = db_table_decoder(entry[0], table)
            temp.append(table_info[1:3])
        structure_list.append([entry[0], temp])
    return structure_list


# organizes the output of 'find_database_structure()' to be more visually appealing
def generate_db_visualizer():
    # contains each database, the tables, variables, and types. seperated in list form
    base_format = '''\n
                DATABASE
        TABLES		+======+
TYPE:VARIABLES	+====+		|		
+---------------+---------------+
| CHUCKLENUTS	|DBL		|
'''

    s1 = find_database_structure()
    addition = ''
    for entry in s1:
        database = entry[0]
        addition += f'+---------------+---------------+vv{database}\n'
        # a list containing table names [0] and the variable type pairs for [1] of each list "[table, [[var, type],
        # [var, type]]]"
        tbl_and_var = entry[1]

        for item in tbl_and_var:
            # contains the variables and types in a format to be added to the final result

            var_pairs = item[1]
            table = item[0]

            addition += f'+---------------+{table}\n'
            for entr in var_pairs:
                type_ = entr[1]
                var = entr[0]

                # adds a pair of variables and it's type
                addition += f'>{type_}: {var}\n'
        addition += '+---------------+---------------+^^\n\n'
    visualized = base_format + addition

    return True, visualized


# used to find table, database, or variable structure. documentation
# here: https://github.com/DrDoofinshmekel/Chucklenuts_DBL/wiki
def poke_dbs(database_nm, table):
    global db_and_table_list
    s1 = find_database_structure()

    # adds '.db' to the database name if it is missing
    if database_nm[(len(database_nm) - 3):len(database_nm)] == '.db' or len(database_nm) <= 0:
        pass
    else:
        database_nm += '.db'

    # if no table is provided, the returned statement will list all tables for the database given
    if database_nm == '':
        dbases = [item[0] for item in db_and_table_list]
        return True, dbases

    elif table == '':
        for thing in db_and_table_list:
            db = thing[0]
            if str(db.lower()) == str(database_nm.lower()):
                return True, thing[1]
            else:
                pass
        return False, f'database: \"{database_nm}\" does not exist'
    else:
        pass

    # searches all database names for the name passed
    for list_ in s1:
        if str(database_nm.lower()) == str(list_[0].lower()):
            for thing in list_[1]:
                if str(thing[0].lower()) == str(table.lower()):
                    return True, (thing[1])
                else:
                    pass
            return False, f'table: \"{table}\" does not exist within database: \"{database_nm}\"'

        else:
            pass
    return False, f'database: \"{database_nm}\" does not exist'


# will generate a list of input commands for "poke_dbs_ui()". specialized and not meant for other usages
def poke_gen_input(database_nm, table, var_list):
    global cwd

    if database_nm[(len(database_nm) - 3):len(database_nm)] == '.db' or len(database_nm) <= 0:
        pass
    else:
        database_nm += '.db'

    db_connect = f"""conn = sqlite3.connect('{(cwd + '/' + database_nm)}')"""
    db_cur = """cursor = conn.cursor()"""

    i_variable = generate_blank_par(len(var_list))
    variables = '('
    for count, pair in enumerate(var_list):
        variables += pair[0]

        if (count + 1) == len(var_list):
            variables += ')'
        else:
            variables += ', '

    command_insert = f"""c.execute(\"\"\"INSERT INTO {table}{variables} VALUES{i_variable}\"\"\", (Variables))"""
    return db_connect, db_cur, command_insert


# a way to search the database structure WITHOUT having to re-run the program. will only return coded database
# info and will not look to see if they exist
def poke_dbs_ui():
    global cwd
    logo = """
 ▄▀▀ ██▀ ▄▀▄ █▀▄ ▄▀▀ █▄█   █▀▄ ▄▀▄ ▀█▀ ▄▀▄ ██▄ ▄▀▄ ▄▀▀ ██▀
 ▄██ █▄▄ █▀█ █▀▄ ▀▄▄ █ █   █▄▀ █▀█  █  █▀█ █▄█ █▀█ ▄██ █▄▄
"""

    # graphical lines used for menu navigation
    sepline = ('━══━' * 20)
    res_line = (('█' + '═━━═' * 25) + '█')

    cwd_p = f'Database Directory:{cwd}'
    db_res = f'{sepline}\nvv DATABASES vv\n{sepline}'

    poke_start = (f'''
{res_line}
{sepline}
{logo}
{sepline}
{res_line}
Press enter to see databases
Enter "database_name" to see its tables
Enter "database_name table_name" to see variables in a table
Enter "q" to exit OR press "v" to view full database structure

{cwd_p}
{sepline}
''')

    complete = False
    clear()
    print(poke_start)
    while not complete:

        search = str(input('>').lower())

        # print all database in structure
        if search == '':
            clear()
            data = poke_dbs('', '')[1]

            print(poke_start + db_res)
            for count, database_ in enumerate(data):
                print(f'{(count + 1)}: {database_}')
        # will break the loop
        elif search == 'q':
            complete = True
        # prints full database structure
        elif search == 'v':
            clear()
            print(poke_start + generate_db_visualizer()[1])

        elif len(search) >= 1 and ' ' not in search:
            succ, data = poke_dbs(search, '')
            db_tb_res = f'{res_line}\nvv TABLES IN DB:\"{search}\"vv\n{res_line}'

            # will ensure that the search finds an item
            if succ is False:
                clear()
                print(poke_start + db_tb_res + '\n database does not exist...')
            else:
                clear()
                print(poke_start + db_tb_res)
                for count, table in enumerate(data):
                    print(f'{(count + 1)}: {table}')

        elif search.count(' ') == 1:
            database, table = search.split()
            succ, data = poke_dbs(database, table)
            db_tb_var_res = f'{res_line}\nvv SEARCH FOR VARIABLES IN DB:{database}>TABLE:{table}> vv\n{res_line}'

            if succ is False:
                clear()
                print(poke_start + db_tb_var_res + '\n database or table does not exist...')
            else:
                clear()
                print(poke_start + db_tb_var_res)

                for count, var in enumerate(data):
                    print(f'{(count + 1)}: {var}')

                # generates the input command for that table
                connect, cursor, command = poke_gen_input(database, table, data)
                print(f'\n\n\n\n{res_line}\nvv COMMANDS FOR CURRENT TABLE vv\n{res_line}')
                print(f'Connect: {connect}\nCursor: {cursor}\nInsert: {command}')

        else:
            pass


sqlite3_dtypes = {'TEXT': str,
                  'INTEGER': int,
                  'REAL': float,
                  'BLOB': str,
                  'NONE': str
                  }

'''
For user functions, added because 'db_pathfinder' has too many reliant functions to change right now.
 will combine in the future
'''


def db_findpath(name):
    global cwd
    db = name

    if name[(len(name) - 3):(len(name))] != '.db':
        db += '.db'
    else:
        db = name
    db_path = f'{cwd}/{db}'

    if os.path.exists(db_path) is True:
        return True, db_path
    else:
        return False, db_path


# primarily used in core functions to find the path of a database from a database name
def db_pathfinder(name):
    global cwd
    db = name

    if name[(len(name) - 3):(len(name))] != '.db':
        db += '.db'
    else:
        db = name
    db_path = f'{cwd}/{db}'

    return db, db_path


# [variable, variable2, list, unixvariable]
# will comb through a list or lists and make tuples using the variables for inserting into a database. 
def in_tuple(variable_list):
	tuple_count = 0  # number of tuple to be made
	tuple_count_l = []  # list of the lengths of lists passed to the function. stored to compare length
	list_num = 0  # number of lists passed to the function. multiple allowed if they are the same length
	tuples = []
	
	
	# sorting out any function call not containing a list or tuple of values as that would
	# negate using this function
	if type(variable_list) == list or type(variable_list) == tuple:
		# set the number of tuples to be created as the length of the first list
		for item in variable_list:
			if type(item) == list:
				tuple_count_l.append(len(item))
			else:
				pass
	else:
			print('::ERROR:: at \"in_tuple()\" function call, passed data container can only be a list or tuple type, (which can contain all data types)')
			return
		
	# make sure there is at least one list passed to the function
	if len(tuple_count_l) == 0:
		print('::ERROR:: at \"in_tuple()\" function call, passed data must contain at least one list. single data\
tuples can be inserted using the \"input_one()\" function')
		return
	else:
		pass
	
	# sets the tuple_count (the amount of tuples to be created)
	# set the tuple number as the only list length if there is only one passed
	if len(tuple_count_l) == 1:
		tuple_count = tuple_count_l[0]
	else:	
		base = tuple_count_l[0]
		for num in tuple_count_l:
			if base - num == 0:
				pass
			else:
				print(f'::ERROR:: at \'in_tuple\' call. passed data contains two lists of unequal length.\
lengths are as follows:{tuple_count_l} (must be equal)')
				return
		tuple_count = tuple_count_l[0]
	# generates the tuples to be passed to be passed back
	for i in range(tuple_count):
		constr = []
		for item in variable_list:
			if type(item) == list:
				constr.append(item[i]) 
			else:
				constr.append(item)
		tuples.append(tuple(constr)) 
	
	return tuples


# input one tuple of variables into a database table
def input_one(db_name, table, insert_tuple):
    # find the pathway to the database and correct name errors
    db, db_pathway = db_pathfinder(db_name)

    # find tables, variables, and generate command parts
    db_i = poke_dbs(db, table)
    db_l = len(db_i[1])
    par = generate_blank_par(int(db_l))

    try:
        conn = sqlite3.connect(db_pathway)
        c = conn.cursor()

        c.execute(f"""INSERT INTO {table} VALUES{par}""", insert_tuple)
        conn.commit()
        conn.close()
        return True
    except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        print(e)
        return False


# insert a list of tuples into a database table
# list_of_tuples would look like this: [('data', data), (data, data), (data, data)]
def input_mult(db_name, table, list_of_tuples):
    # find the pathway to the database and correct name errors
    db, db_pathway = db_pathfinder(db_name)

    db_i = poke_dbs(db, table)
    db_l = len(db_i[1])
    par = generate_blank_par(int(db_l))

    try:
        conn = sqlite3.connect(db_pathway)
        c = conn.cursor()
        c.executemany(f"""INSERT INTO {table} VALUES{par}""", list_of_tuples)
        conn.commit()
        conn.close()
        return True
    except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        print(e)
        return False


# used for selecting from a database using a function call and then returning results
def db_sel(database_name, ex_):
	name, pathway = db_pathfinder(database_name)
	results_l = []

	# connect to a database and if it doesn't exist, terminate the function call
	try:
		conn = sqlite3.connect(Path(pathway))
		c = conn.cursor()
	except (sqlite3.OperationalError, sqlite3.ProgrammingError, FileNotFoundError):
		print(f'::ERROR:: database \"{name}\" does not exist, please check the database list')
		return False, ''

	# check if the passed command variable is a list or a string and execute accordingly
	if isinstance(ex_, list):
		# for every command in passed list, execute and save the result into a dictionary
		for item in ex_:
			try:
				c.execute(f'{item}')

				data = c.fetchall()
				for result in data:
					results_l.append(result)
			except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as err:
				print(err)
				exit()
		if len(results_l) >= 1:
			return True, results_l
		else:
			return False, results_l
	elif isinstance(ex_, str):
		# execute the single command givin in string form and return the result
		try:
			c.execute(f'{ex_}')
			results_s = c.fetchall()
			conn.close()
			if len(results_s) >= 1:
				return True, results_s
			else:
				return False, results_s
		except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as err:
			print(err)
			exit()
	else:
		print('::ERROR:: Passed select query must be either \'List\' or \'str\' type')
		exit()


# used for running commands without returning data
def db_ex(database_name, ex_):
    name, pathway = db_pathfinder(database_name)

    # connect to a database and if it doesn't exist, terminate the function call
    try:
        conn = sqlite3.connect(Path(pathway))
        c = conn.cursor()
    except (sqlite3.OperationalError, sqlite3.ProgrammingError, FileNotFoundError):
        print(f'::ERROR:: database \"{name}\" does not exist, please check the database list')
        return False

    # check if the passed command variable is a list or a string and execute accordingly
    if isinstance(ex_, list):
        # for every command in passed list, execute the string
        for item in ex_:
            try:
                c.execute(f'{item}')
            except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as err:
                print(err)
                exit()
        conn.commit()
        conn.close()
        return True
    elif isinstance(ex_, str):
        # execute the single command given in string form
        try:
            c.execute(f'{ex_}')
            conn.commit()
            conn.close()
            return True
        except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as err:
            print(err)
            exit()
    else:
        print('::ERROR:: Passed select query must be either \'List\' or \'str\' type')
        exit()


# generate the tuple containing lists into a list of tuples
def cond_generate_tup(input_data):
	has_list = False
	
	if type(input_data) == tuple:
		pass
	else:
		print(f'::ERROR:: at cond_generate_tup. Provided input data \"{input_data}\" is not in a tuple')
		exit()
	
	
	# determine if there is a list in the tuple
	for entry in input_data:
		if type(entry) is list:
			has_list = True
			break
		else:
			pass
	
	# create the tuples used to submit data to the database
	if has_list is True:
		ulst = in_tuple(input_data)
		# create input and select command for the function next
		
	else:
		ulst = input_data
	return has_list, ulst
	
	
# SELECT * FROM table WHERE variable = in AND variable2 = in2;
def cond_sel_filter(db_name, table, input_tup, cond_list, has_list):
	# for every insert tuple, use the indexes of the conditions to create a select command and then execute it.
	base_sel = f"SELECT * FROM {table} WHERE"
	
	search = poke_dbs(db_name, table,)
	t_vars = [var[0] for var in search[1]]
	
	commands = []
	cmd = ''
	
	# check if there is a list to expand in the 
	if has_list is True:
		for tup in input_tup:
			cmd = base_sel
			
			for count, number in enumerate(cond_list):		
				tvar = t_vars[number]
				qvar = tup[number]

				# make sure numbers are submitted without quotation marks
				try:
					int(qvar)
					cmd += f' {tvar} = {qvar}'
				except ValueError:
					cmd += f''' {tvar} = "{qvar}"'''
					
				if (count + 1) == len(cond_list):
					cmd += ';'
				else:
					cmd += ' AND'
			commands.append(cmd)

	
	# for single tuple in theory
	else:
		cmd = base_sel
		for count, number in enumerate(cond_list):
			tvar = t_vars[number]
			qvar = input_tup[number]

			# make sure numbers are submitted without quotation marks
			try:
				int(qvar)
				cmd += f' {tvar} = {qvar}'
			except ValueError:
				cmd += f''' {tvar} = "{qvar}"'''
				
			if (count + 1) == len(cond_list):
				cmd += ';'
			else:
				cmd += ' AND'
		commands.append(cmd)
	
	uq_sub = []
	for count, select in enumerate(commands):
		in_db, tr = db_sel(db_name, select)
		if in_db is True:
			pass
		else:
			if has_list is True:
				uq_sub.append(input_tup[count])
			else:
				uq_sub.append(input_tup)
				
	# if there are any results, the first return is True, if none, it is false
	if len(uq_sub) == 0:
		return False, uq_sub
	else:
		return True, uq_sub

def cond_input(database, table, insert_data, cond_list):
	# stop tuples and empty conditions lists from reaching definitions of variables
	if type(cond_list) == list:
		if len(cond_list) == 0:
			print(f'::ERROR:: at \"cond_input\" call. Conditions list: \"{cond_list}\" is empty, there must be at lease one index.') 
			return
		else:
			pass	
	else:
		print(f'::ERROR:: at \"cond_input\" call. The provided conditions list is a tuple but must be a list')
		return
		
	# make sure that the database and table exist. also verify the number of passed variables matches the
	# number of variables in the passed table and make sure a db+table is passed before continuing
	search = poke_dbs(database, table)
	# the count of variables in the given table.
	v_len = len(search[1])
	# list with indexes representing variables to search for before inputting tuple
	cond_index = []
	
	# check to make sure the database and table exist before processing request and that passed
	# database and table are not blank
	if search[0] is False:
		print(f'::ERROR:: at \'cond_input()\' call. {search[1]}')
		return
	elif table == '' or database == '':
		print(f'::ERROR:: at \'cond_input()\' call. a table and database must be given and not (a) blank string(s) >> \"\"')
		return
	else:
		pass
		
	# will add all numbers to a list and generate all number ranges into numbers
	try:
		for num in cond_list:
			if ':' in str(num):
				start, stop = num.split(':')
				# turns the range into individual numbers so duplicates can be found
				res = [item for item in range(int(start), int(stop)+1)]
				
				for n in res:
					cond_index.append(n)
			else:
				cond_index.append(num)
	except (TypeError, ValueError) as e:
		print(f'::ERROR:: at \'cond_input()\' call. given condition list contains non integer: {cond_list} >or> {e} ')
		return
	
	# sorts and then removes duplicates from number list
	cond_index = [*set(cond_index)]
		
	# find the names of the table variables and make sure the conditions list is no longer 
	# than the amount of table variables 
	t_vars = [var[0] for var in search[1]]
	cond_index.sort()	
	compare = cond_index[-1]
	compare2 = len(t_vars)
	
	# check to make sure the number of conditions is no higher than the number of table variables
	# check to make sure condition call contains all numbers
	try:
		if (compare2- 1) >= compare:
			pass
		else:
			print(f'::ERROR:: at \"cond_input()\" call. number in passed conditions \n \"{compare}\"\
is higher than the number of table variables: \"{table}\" with \"0-{compare2 - 1}\"')
			return
	except TypeError as e:
		print(f'::ERROR:: at \"cond_input()\" call. Passed condition list contains non-numbers: \"{cond_list}\"')
		return 
	# t_vars is the list of variable names from the selected table in order.
	# cond_index is the list of numbers used to determine conditional inputting
	
	# convert any lists within the input tuple in a list of tuples or keep normal tuples the same
	has_list, inputs = cond_generate_tup(insert_data)
	
	# will use condition list, table, db name, and input tuple(s) to search and remove existing data tuples from the
	# list of data to be entered 
	unq = inputs_list = cond_sel_filter(database, table, inputs, cond_index, has_list)
	
	# input the data into a database
	if has_list is True and unq[0] is True:
		input_mult(database, table, unq[1])
	elif has_list is False and unq[0] is True:
		single = unq[1]
		input_one(database, table, single[0])
	else:
		pass
	return 
	
	
	# finish the command generation!! then:
	# code to select the given indexes and compare them to the input indexes
	# delete all indexes found to be duplicate using pop(index) wit two versions of the list <<
	# then submit all remaining of the inserts to input_mult function
	
	

refresh_database_structures()

l3 = [1, 2, 3, 4, 5]
# print(cond_generate_tup(('one', l1, 'two'))[1])	
	
cond_input('testing', 'tdata', ('testing', 1, 'data1', 'data2'), [0])


def program_info():
    info = (f'''   
-------------------------------------------------------------
    Chucklenuts_DBL.{cndbl_version} Program information:
-------------------------------------------------------------
____________
OS VERSIONS: 
Linux, tested on: (debian, ubuntu, pop OS)
Windows, (NOT SUPPORTED)
MAC OS, (NOT SUPPORTED)
_________________
WEB CONNECTIVITY:
All functions are offline
_________
DBMS: 
Chucklenuts_DBL.{cndbl_version} uses SQlight3 for Python
_______________
THREAD USAGE: 1
DEVELOPER: DrDoofinshmekel
GITHUB: https://github.com/DrDoofinshmekel'''
            )
    print(info)


def terminal_manager():
    sepline = ('━══━' * 20)
    res_line = (('█' + '═━━═' * 25) + '█')
    complete = False
    change_m = f"""
{res_line}
{sepline}	
 ▄▀▀ █▄ █ █▀▄ ██▄   ▀█▀ ██▀ █▀▄ █▄ ▄█ █ █▄ █ ▄▀▄ █     █▄ ▄█ ▄▀▄ █▄ █ ▄▀▄ ▄▀  ██▀ █▀▄
 ▀▄▄ █ ▀█ █▄▀ █▄█    █  █▄▄ █▀▄ █ ▀ █ █ █ ▀█ █▀█ █▄▄   █ ▀ █ █▀█ █ ▀█ █▀█ ▀▄█ █▄▄ █▀▄
{sepline}
{res_line}
DATABASE: SELECTING
PATHWAY: N/A

please select a database with the corresponding index
or enter 'q' to exit Terminal Manager

{sepline}	
"""

    while not complete:
        clear()
        print(change_m)
        dbl = poke_dbs('', '')[1]
        for count, database in enumerate(dbl):
            print(f'{count}.{database}')
        index = input('>')

        if index == 'q':
            return
        else:
            try:
                db = dbl[int(index)]
                print(db)
                database_terminal(str(db))
            except (KeyError, TypeError, ValueError, IndexError):
                print(f'\'{index}\' is not a valid option, please try again!')


ex = []


# opens a terminal to search a database using sql
def database_terminal(db_name):
    global ex
    db, db_pathway = db_pathfinder(db_name)
    qline1 = '	┗━══━━══━━══━━══━━══━━══━━══━━══━━══━'
    qspace2 = ('	' + '┃-')
    sepline = ('━══━' * 20)
    res_line = (('█' + '═━━═' * 25) + '█')
    logo = f"""
{res_line}
{sepline}	
 █▀▄ █▄▄   ▀█▀ ██▀ █▀▄ █▄ ▄█ █ █▄ █ ▄▀▄ █  
 █▄▀ █▄█    █  █▄▄ █▀▄ █ ▀ █ █ █ ▀█ █▀█ █▄▄
{sepline}
{res_line}
DATABASE: {db}
PATHWAY: {db_pathway}

!!db_terminal is to be used for searching database variables, all command outputs are printed to the terminal.!!
            enter commands to add them to the queue

'<' executes all commands in the queue
'<out' executes all commands in the queue and writes the output to a text file in the server directory
'<<' deletes the last command added to the queue
'<del' delete a specific queued command
'<clear' clear the queue
'<q' quit the virtual terminal
{res_line}
"""
    result_m = f"""
{res_line}
{sepline}
:|█▀▄ ██▀ ▄▀▀ █ █ █   ▀█▀ ▄▀▀|:
:|█▀▄ █▄▄ ▄██ ▀▄█ █▄▄  █  ▄██|:
{sepline}
{res_line}
"""
    queue_m = f"""
        ╔━══━━══━━══━━══━━══━━══━━══━━══━━══━
        ┃▄▀▀ █▄ ▄█ █▀▄   ▄▀█ █ █ ██▀ █ █ ██▀
        ┃▀▄▄ █ ▀ █ █▄▀   ▀▄█ ▀▄█ █▄▄ ▀▄█ █▄▄
        ┃                  ▀▀
"""

    # execute, format results, and print to screen the commands in the 'ex' list
    def execute_q():
        global ex
        results = []

        # try to execute the list of commands and add results or error to a list
        for item in ex:
            try:
                c.execute(f'{item}')
                results.append(c.fetchall())
            except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as err:
                results.append(err)
        # prints the results menu graphics
        print(result_m)

        # loops through the sets of results and prints the query information
        for count, item2 in enumerate(results):
            print(f"""======\nCOMMAND: \'\'\'{ex[count]}\'\'\'\nCOMPLETE\n======""")

            # will print either a list of results or and error code from sqlite3
            try:
                for line in item2:
                    print(line)
            except TypeError:
                print(item2)
        input('press any key to continue...')
        ex.clear()

    def write_out():
        global ex, cwd
        results = []

        # try to execute the list of commands and add results or error to a list
        for item in ex:
            try:
                c.execute(f'{item}')
                results.append(c.fetchall())
            except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as err:
                results.append(err)
        # prints the results menu graphics
        print(result_m)

        # loops through the sets of results and prints the query information
        filename = f'cndb_query_data_{str(time.time())}'
        file = Path(str(cwd) + '/' + filename)

        # loops through, prints, and also
        with open(file, 'w') as fh:
            for count, item2 in enumerate(results):
                print(f"""======\nCOMMAND: \'\'\'{ex[count]}\'\'\'\nCOMPLETE\n======""")
                q_info = f"""======\nCOMMAND: \'\'\'{ex[count]}\'\'\'\nCOMPLETE\n======"""

                # will print either a list of results or and error code from sqlite3
                try:
                    for line in item2:
                        print(line)

                        # add to file and also add the query as well
                        if q_info == "":
                            fh.write(str(line) + '\n')
                        else:
                            fh.write(str(q_info) + '\n')
                            fh.write(str(line) + '\n')
                            q_info = ""
                except TypeError:
                    print(item2)
        fh.close()
        input('press any key to continue...')
        ex.clear()

    def del_last():
        ex.pop()

    def del_index():
        failed = False
        print(sepline[0:10] + '\ntype the number of the command you want removed from the queue or \'c\' to cancel')

        while not failed:
            index = input('>')

            if index.lower() == 'c':
                failed = True
            else:
                try:
                    ex.pop(int(index))
                    failed = True
                except (KeyError, TypeError, ValueError, IndexError):
                    print(f'\'{index}\' is not a valid entry, please try again')

    def clear_q():
        ex.clear()
        return

    def print_q():
        queue = queue_m
        for count, item in enumerate(ex):
            queue += f'{qspace2}{count}.{item}\n'
        queue += qline1
        print(queue)

    options = {'<': execute_q,
               '<out': write_out,
               '<<': del_last,
               '<del': del_index,
               '<clear': clear_q,
               }

    # if a name was provided, connect to the database name given
    if poke_dbs(db_name, '')[0] is True and db_name != '':
        pass
    else:
        return False

    try:
        conn = sqlite3.connect(db_pathway)
        c = conn.cursor()
    except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        print(e)
        return False, f'FAILED TO CONNECT TO {db_pathway}'

    full = False
    # loop and edit the commands queue
    while not full:
        clear()
        print(logo)
        print_q()
        command = input('>')
        if command[0] == '<':
            if command[0:2] == '<q':
                full = True
            else:
                try:
                    run = options[command]
                    run()
                except KeyError:
                    print(f'\"{command}\" is not a valid option, please try again')

        else:
            ex.append(f'''{command}''')
    return True


# function aliases (can be used to call a given function)
fds = find_database_structure  # find_database_structure()
rds = refresh_database_structures  # refresh_database_structure()
t_man = terminal_manager  # terminal_manager()
dbt = database_terminal  # database_terminal()
g_dbv = generate_db_visualizer  # generate_db_visualizer()


