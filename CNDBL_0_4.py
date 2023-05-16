import sqlite3
import time
import os
from pathlib import Path
import json
import logging as lg
import CNDBL_config as cf

# used to check if all dependencies are currently there >>NOT FINISHED<<
dependencies = [["python import", "sqlite3"], 
                ["python import", "time"],
                ["python import", "os"],
                ["python import", "pathlib"],
                ["python import", "json"],
                ["python import", "logging"]
                ]

# :--:USER CONFIGURATIONS:--:

# -database name checks
check_chars = True
disallowed_chars = ["<", ">", ":", "/", "|", "?", "*"]
num_of_periods = 1

# -config
verify_config = False 
header_identifier = "13241241434555123123"
header_salt = ""
# -logging
print_errors = True
error_logging = True
process_logging = False


# :--:SCRIPT STATES:--:
config_complete = False

# :--:BACKEND:--:

# -version
cndbl_version = '0.4'
# -pathway and time vars
cwd = os.path.realpath(os.path.dirname(__file__))
unix = time.time()
# -logging congigurations
log_loc = Path(cwd, "CNDBL.log")
lg.basicConfig(filename=log_loc,
encoding='utf-8',
level=lg.DEBUG, 
format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

# :--:DICTIONARIES AND LISTS:--:

# database class instances which are searchable by name: instance = db_inst[name]
db_inst = {}
# -imported config dictionaries
db_w_tables = {}
tables_w_vars = {}
vars_w_types = {}
# -sqlite3 datatype equivalents for python datatypes
vars_types = {"str": "TEXT", 
              "int": "INTEGER",
              "float": "REAL",
              "null": "NULL",
              "images": "BLOB"
              }


# clears the console for both Windows and Linux
def clear():
    sys_logging("clear()", "called", "info")
    os.system('clear')


# simple adds ".db" to a db name if it is not already there (takes lists or ind names)
# and  optionally can check names for disallowed characters and filesystem syntax errors
def db_name_correction(db_s : str):

    def character_check(sng):
        global disallowed_chars, num_of_periods
        for char in sng:
            if char not in disallowed_chars:
                pass
            else:
                print(f"::ERROR:: database name \"{sng}\" contains disallowed",
                f"characters {disallowed_chars} \n TERMINATING PROGRAM")
                exit()
        
        if sng.count(".") == num_of_periods:
            return sng
        else:
            print(sng)
            print(f"::ERROR:: number of periods in \"{sng}\" is greater than \"{num_of_periods}\" \nTERMINATING PROGRAM")
            exit()

    # check a list or tuple of names (in string format)
    def lst_correction(lst):
        global check_chars
        tpe_correction = type(lst)
        corrected = []
        for name in lst:

            if name[-3:] == ".db":
                add = (name)
            else:
                add = (name + ".db")
            
            # check if configured to check filesystem syntax errors
            if check_chars is True:
                character_check(add)
            else:
                pass

            corrected.append(add.lower())
        
        return tpe_correction(corrected)

    # correct a single name in string format
    def sng_correction(sng):
        global check_chars
        if sng[-3:] == ".db":
            corrected = sng
        else:
            corrected = sng + ".db"

        # check if configured to check filesystem syntax errors
            if check_chars is True:
                character_check(corrected)
            else:
                pass

        return corrected.lower()
    
    mults = (list, tuple)
    if type(db_s) in mults:
        output = lst_correction(db_s)
    elif type(db_s) == str:
        output = sng_correction(db_s)
    return output



def sys_logging(mfunction: str, mstring: str, type_: str):
    global error_logging, process_logging, unix, print_errors
    prog = ["prog", "program", "info"]
    err = ["debug"]
    display = f"[{int(unix)}]at \"{mfunction}\": {mstring}"

    if process_logging is True and type_ in prog:
        lg.info(display)
        return
    elif process_logging is False and type_ in prog:
        return
    elif error_logging is True:
        type_log = {"debug": lg.debug,
                    "info": lg.info,
                    "warning": lg.warning,
                    "warn": lg.warning,
                    "error": lg.error,
                    "critical": lg.critical
                    }
        try:
            cmd = type_log[str(type_.lower())]
            cmd(display)
            if print_errors is True:
                print(f"""at \"{mfunction}\": \"{mstring}\"""")
            else:
                pass
        except KeyError:
            lg.error(f"passed logging type \"{type_}\" does not exist, log failed")
    else:
        return
    return


def fetch_db_inst(name : str):
    global config_complete
    try:
        return db_inst[db_name_correction(name)]
    except KeyError:
        if config_complete is False:
            print(f'::ERROR:: config was not refreshed at runtime, please do so with \"rds()\" at the start of the script')
        else:
            print(f'::ERROR:: passed database name {db_name_correction(name)} could not be found in database dict')
        exit()


class db:
    # global dictionaries for constructing the database instances from initial calls
    global db_w_tables, tables_w_vars, vars_types
    # makes a class obj with relevant information in memory
    def __init__(self, name_, pathway_):
        self.dbname = name_
        self.dbpath = pathway_
        self.dbtables = db_w_tables[name_]
        self.conn_path = self.dbpath + "/" + self.dbname
        
        self.vars = [cf.custom_tables[table] for table in self.dbtables ]
        # print(self.vars, 'VARS')
        
        t = []
        for item in self.vars:
            t.append([vars_w_types[var] for var in item])
        self.types = t

    # the following take a name (str) and return information on a database for ease of access VV
    def find(database, find):
        queries = {'path': db.rpath,
                   'conn': db.rconn,
                   'name': db.rname,
                   'tables': db.rtables,
                   'vars': db.rvars,
                   'types': db.rtypes
                   }
        
        ins = fetch_db_inst(database)

        try:
                ex = queries[find]
                found = ex(ins)
        except KeyError as e:
            db.error(f'::passed \"find\" arg (\"{find}\") is not a valid option::\nOPTIONSVV')
            for item in queries:
                print(f'>{item}')
            exit()
        return found

    # end of ease of access functions. the remaining require the database instance to call. ^^
    def error(error):
        global config_complete
        # err!!
        if config_complete is False:
            print('::ERROR:: config has not been refreshed with \'rds()\' at runtime')
            exit()
        else:
            print(error)

    def listall():
        global db_inst
        lst = [item for item in db_inst]
        return lst

    # returns path, tables, vars and types
    def retr_attr(database : str):
        ins = fetch_db_inst(database)
        a, b, c, d = ins.rall()
        return a, b, c, d
    
    def rall(self):
        return self.conn_path, self.dbtables, self.vars, self.types
    
    def rpath(self):
        return self.dbpath

    def rname(self):
        return self.dbname
    
    def rtables(self):
        return self.dbtables

    def rvars(self):
        return self.vars

    def rtypes(self):
        return self.types

    def rconn(self):
        return self.conn_path


# parse through the easy config and set config variables that way instead of using dictionaries 
def parse_ez_config():
    pass


def apply_db_changes():
    def run_command(command, path):
        try:
                
            conn = sqlite3.connect(path)
        except sqlite3.OperationalError as e:
            print(f"Pathway is not valid {path}")
            exit()

        c = conn.cursor()

        try:
            c.execute(command)
            conn.commit
        except (sqlite3.Error, sqlite3.OperationalError) as e:
            print(e, f"Passed command not valid {command}")
        pass
    pass

    def construct_commands():
        global db_w_tables, tables_w_vars, vars_w_types, db_inst
        # fetch all database class instances to retrieve their structure
        instances = [name for name in db_inst]
        # fetch tables, path, variables, and variable types for the database
        for ins in instances:
            conn, tables, vars, rawtypes = db.retr_attr(ins)
            types = [item for item in rawtypes]

            for count, table in enumerate(tables):
                # create command base and add the table name to it.
                base = f"CREATE TABLE IF NOT EXISTS {table.lower()}("
                vrset = vars[count]
                tyset = types[count]
                # add the variables and their types to the command
                for num in range(len(vars[count])):
                   base += f'''{vrset[num]} {vars_types[tyset[num]]}, '''
                command = base[:-2] + ")"
                
                # rund the command with the current database pathway
                run_command(command, conn)

    construct_commands()



def refresh_database_structures():
    global cwd, header_identifier, header_salt, verify_config
            
    def load_config():
        global db_w_tables, tables_w_vars, vars_w_types, db_inst
        # load the config components into memory to speed queries
        # and prevent identifier bypassing
        db_w_tables = cf.custom_databases
        tables_w_vars = cf.custom_tables
        vars_w_types = cf.custom_vars
        return db_w_tables, tables_w_vars, vars_w_types
    
    def run_config_verification():
        # will cryptographically ensure header is verified every "rds call"
        load_config()

    # create all of the database instances for class:db. and make searchable in db_inst
    def create_db_instances():
        global config_complete
        for database in db_w_tables:
            # db name
            name = db_name_correction(database)
            # create db instance
            database = db(name, cwd)
            # creating a new dict entry to db_dict so the inst is callable by the str name
            db_inst[name] = database
        config_complete = True
    
    # check if config verification is enabled
    if verify_config is True:
        run_config_verification()
    elif verify_config is False:
        load_config()
    else:
        # "::ERROR::"
        print("VERIFY CONFIG MUST BE SET TO EITHER \'TRUE\' OR \'FALSE\'")

    create_db_instances()
    apply_db_changes()



    


# take a tuple with lists and expand them into a list of tuples.
def in_tuple(data_tuple : tuple):
    # finds the length of every list in the tuple and then find the longest list out of them all.
    iterations = sorted([len(item) for item in data_tuple if type(item) == list])[-1]
    data_list = []

    for i in range(iterations):
        tup = []
        for index in data_tuple:

            if type(index) == list:
                try:
                    tup.append(index[i])
                except IndexError:
                    tup.append(None)
            else:
                tup.append(index)
        data_list.append(tup)

    return data_list


def serialize(data, nested : bool):
    dtypes = [list, dict, tuple]

    def ser_nested(data):
        data_mult = []
        wrap_type = type(data)

        for obj in data:

            if type(obj) in dtypes:
                try:
                    data_mult.append(json.dumps(obj))
                except (ValueError, TypeError, json.JSONDecodeError):
                    # err
                    print('::ERROR:: in serialize')
            else:
                data_mult.append(obj)
        return wrap_type(data_mult)

    if nested is True:
        return ser_nested(data)
    else:

        return json.dumps(data)


# turns serialized data to python objects and return them.
def deserialize(data, nested : bool):
    dtypes = [list, dict, tuple]

    def sser_nested(data):
        data_mult = []
        wrap_type = type(data)

        for obj in data:
            try:
                data_mult.append(json.loads(obj))
            except (ValueError, TypeError, json.JSONDecodeError):
                data_mult.append(obj)

        return wrap_type(data_mult)
    
    # if nested is true, first serialize inner indexes and then return result
    if nested is True:
        return sser_nested(data)
    else:
        # else if nested isn't selected, serialize the whole object and return it
        try:
            ret = json.loads(data)
            return ret
        except (ValueError, TypeError, json.JSONDecodeError):
            print(f'::ERROR:: in deserialize, passed object(s) {data} cannot be deserialized')
            return


"""
INPUT AND DATABASE DATA MANAGMENT
"""


# will generate the blank question tuple used in insert commands for sqlite3 example: (?, ?, ?, ?)
def generate_blank_par(number):
    variable = '?, ' * number
    v_len = (len(variable) - 2)
    fvariable = variable[0:v_len]
    prefix = '('
    postfix = ')'
    complete = f'{prefix}{fvariable}{postfix}'
    return complete


# input one tuple of variables into a database table
def input_one(db_name, table, insert_tuple):
    # find the pathway to the database and correct name errors
    db_pathway = db.find(db_name, 'conn')

    # find tables, variables, and generate command parts
    db_tbls = db.find(db_name, 'tables')
    tbls_len = len(db_tbls)
    par = generate_blank_par(tbls_len)

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
def input_mult(db_name : str, table : str, list_of_tuples : list):
    # find the pathway to the database and correct name errors
    db_pathway = db.find(db_name, 'conn')

    # find tables, variables, and generate command parts
    db_tbls = db.find(db_name, 'tables')
    tbls_len = len(db_tbls)
    par = generate_blank_par(tbls_len)

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


# detect nested objects
def nest_detect(list_, nested_type):
    try:
        result = any(isinstance(i, nested_type) for i in list_)
    except TypeError as e:
        print(f'::ERROR:: in nest_detect with inputs ({list_}, {nested_type}) \"{e}\"')
        exit()
    return result


# select one item from a database and it's table
def select_one(database : str, query_ : (str, list)):
    conn_path = db.find(database, 'conn')
    data = retrieve_(conn_path, query_, False)
    return data


# select multiple items from a database and it's table
def select_all(database : str, query_ : (str, list)):
    conn_path = db.find(database, 'conn')
    data = retrieve_(conn_path, query_, True)
    return data


# used by the select functions to gather results from a database
def retrieve_(conn_path, query_s, all_tf : bool):
    def submit(conn_path, query_s, all_tf):
        # connect, and submit the query to the database then return the result
        try:
            conn = sqlite3.connect(conn_path)
            c = conn.cursor()
            c.execute(query_s)
            if all_tf is True:
                data = c.fetchall()
            elif all_tf is False:
                data = c.fetchone()
            conn.close()

            return data
        except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            print(e)
            return False
    
    # if there are multiple commands, create a list with the results in order
    result = ()
    multresult = []
    if isinstance(query_s, list):
        for q in query_s:
            multresult.append(submit(conn_path, q, all_tf))
        return multresult
    elif isinstance(query_s, str):
        result = submit(conn_path, query_s, all_tf)
        return result
    else:
        print(f"::ERROR:: in \"retrieve_()\" with query \"{query_s}\". input should be list or str datatypes")


# simple command execution to a select database
def execute(database, command : (str, list)):
    def submit(database, command):
        conn_path = db.find(database, 'conn')
        conn = sqlite3.connect(conn_path)
        c = conn.cursor()
        try:
            c.execute(command)
            conn.commit()
            conn.close()
        except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            print(e)
    
    # determine if there are multiple commands or just one
    if isinstance(command, list):
        for com in command:
            submit(database, com)
    elif isinstance(command, str):
        submit(database, command)
    else:
        print(f"::ERROR:: in \"execute()\" with query \"{command}\". input should be list or str datatypes")


'''
pop_stored() functions vv 
'''


def pop_stored(database : str, table : str, data_tuple: (tuple, list), indexes : list):
    
    def expand_indexes(indexes_n):
        cond_index = []
        try:
            for num in indexes_n:
                if isinstance(num, str):
                    start, stop = num.split(':')
                    res = [item for item in range(int(start), int(stop) + 1)]

                    for n in res:
                        cond_index.append(n)
                else:
                    cond_index.append(num)
        except (TypeError, ValueError) as e:
            print(
                f'::ERROR:: at \'pop_stored()\' call. given condition list contains non integer: {cond_list} >or> {e} ')
            return e
        cond_index = [*set(cond_index)]
        return cond_index


    def construct_query(database, table, finished_indexes, data_tuple : tuple):
        global tables_w_vars
        base = f"SELECT * FROM {table} WHERE"
        table_list = tables_w_vars[table]

        # loop through the number of indexes to search
        try:
            for i in range(len(finished_indexes)):
                try:
                    addition = f''' {table_list[i]} = "{int(data_tuple[i])}" AND'''
                except (ValueError) as e:
                    addition = f''' {table_list[i]} = "{str(data_tuple[i])}" AND'''
                base += addition
            return base[0:-4]

        except (KeyError, IndexError) as e:
            print(f'::ERROR:: at \"pop_stored\" or \"ps()\" with indexes input \"{finished_indexes}\"',
            f'passed indexes are more than the number of variables in the table ({i})')


    # check a database with a premade select command and return a True or False output
    def check_db(database : str, command : str):
        result = select_all(database, command)
        if len(result) <= 0:
            return False
        else:
            return True


    # iterate through the data provided and remove all duplicates
    def filter_stored(done_indexes, database, table, data_tuple):
        if isinstance(data_tuple, tuple):
            result = check_db(database, construct_query(database, table, done_indexes, data_tuple))
            if result is False:
                return data_tuple
            else:
                return []

        elif isinstance(data_tuple, list):
            non_repeats = []
            
            # iterate through the list of tuples and remove any that are in the database already
            try:
                for item in data_tuple:
                    result = check_db(database, construct_query(database, table, done_indexes, item))
                    if result is False:
                        non_repeats.append(item)
                    else:
                        pass
                return non_repeats

            except:
                print('fail')
        else:
            print(f'::ERROR:: at \"pop_stored()\" or \"ps()\" with input \"{data_tuple}\" (must be str or list)')

    # expand the search indexes 
    done_indexes = expand_indexes(indexes)
    # return the result of a lookup of all data tuples provided
    return filter_stored(indexes, database, table, data_tuple)

'''
pop_stored() functions ^^ 
'''


def cond_input(database : str, table : str, data_tuple: (tuple, list), indexes : list):
    remaining = pop_stored(database, table, data_tuple, indexes)
    print(remaining)

    # if user passed a single insert data it will be in tuple form
    if isinstance(remaining, tuple):
        try:
            input_one(database, table, remaining)
        except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            print(f'::ERROR:: in cond_input(). passed data is in tuple form but ',
            'contains more than one insert tuple or wrong characters: presort={data_tuple}, postsort=\"{remaining}\"')
    
    # if user passed list of tuples the tuples will be stored in list form.
    elif isinstance(remaining, list):
        try:
            input_mult(database, table, remaining)
        except (KeyError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            print(f'::ERROR:: in cond_input(). passed data is in tuple form but ',
            'contains more than one insert tuple or wrong characters: presort={data_tuple}, postsort=\"{remaining}\"')
    else:
        print(f'::ERROR:: in cond_input(). passed data is not compatible with input parameters,',
        'please refer to docutmentation for correct command usage input=\"{data_tuple}\"')


def program_info():
    sys_logging("program_info()", "called", "info")
    info = (f'''   
-------------------------------------------------------------
    Chucklenuts_DBL.{cndbl_version} Program information:
-------------------------------------------------------------
____________
LICENSE:
GNU General Public License v4.0
____________
OS VERSIONS: 
Linux, supported on: (debian, ubuntu, pop OS)
Windows, supported on: (windows 10, Windows 11)
MAC OS, (NOT SUPPORTED)
_________________
WEB CONNECTIVITY:
All functions are offline
_________
DBMS:
Chucklenuts_DBL.{cndbl_version} uses SQlight3 for Python
_______________
THREAD USAGE: 1
_______________
DEVELOPER: DrDoofinshmekel
GITHUB: https://github.com/DrDoofinshmekel'''
)
    print(info)


rds = refresh_database_structures

# function aliases (can be used to call a given function)
ps = pop_stored