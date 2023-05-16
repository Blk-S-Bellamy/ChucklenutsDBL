import time
import os
import CNDBL_0_4 as cn
from pathlib import Path
import resource_pack as rp

'''
# different code bookmarks, search to nav to the head of the section

vvv CORE FUNCTIONS vvv
vvv GRAPHICAL GENERATORS vvv
vvv NAVIGATION FUNCTIONS vvv
vvv QUEUE COMMANDS vvv
vvv PAGE UPDATE FUNCTIONS vvv
vvv PAGE FUNCTIONS vvv
vvv FOOTER VVV
'''

db_sel_state = False
cwd = os.path.realpath(os.path.dirname(__file__))
vars_types = {"str": "TEXT", 
              "int": "INTEGER",
              "float": "REAL",
              "null": "NULL",
              "images": "BLOB"
              }

# GLOBAL GRAPHIC VARIABLES vvv
# saves the checklist states as dictionaries 
gl_checklist_dict1 = {}
gl_checklist1 = []
gl_checklist_dict2 = {}
gl_checklist2 = []
gl_checklist_dict3 = {}
gl_checklist3 = []
gl_ui = ''
queue_history = []
queue_graphic = ''
results_graphic = ''
curr_db_name = ''
curr_dbs = []
# GLOBAL GRAPHIC VARIABLES ^^^
'''
vvv CORE FUNCTIONS vvv
'''


def clear():
    os.system('clear')


# turn a list of keys and a list of values into a dictionary
def create_dict(keys : list, values : list):
    dictionary = {}
    
    if len(keys) == len(values):
        for count, key in enumerate(keys):
            dictionary[key] = values[count]
        return dictionary
    else:
        print('''::ERROR:: at create_menu_dict. passed lists bust be of equal length''')            


# put a message in a box. submit quote blocks or short sentences with \n between lines
def boxify(message : str):
	def parse_message(message : str):
		try:
			parsed1 = str(message).splitlines()
		except (TypeError, ValueError) as e:
			print('FAIL')		
		return parsed1
    
	def calculate_box(parsed_message : list):
        # the width of the top and bottom variables 
		str_floor_width = len(rp.bottom)
		str_ceiling_width = len(rp.top)
		# takes a list of strings, makes a new list of the lengths of each string,
		#  sorts the list by value, and returns the highest value :D
		needed_width = sorted([len(sentence) for sentence in parsed_message])[-1]
        
        
		box_floor_tiles = round(needed_width/str_floor_width) + 1
		box_ceiling_tiles = round(needed_width/str_ceiling_width) + 1
		box_wall_height = len(parsed_message)

		total_width = str_floor_width * box_floor_tiles
		return box_floor_tiles, box_ceiling_tiles, total_width, parsed_message

	def construct_box(floor, ceiling, width, parsed_message):
		boxified = ''
        
		# add top pannel
		boxified += rp.top_left_corner + (rp.top * ceiling) + rp.top_right_corner 
		
        # add text and height
		for sentence in parsed_message:
			spaces = ' ' * ((width - len(sentence)))

			boxified += f'''\n{rp.left_wall}{sentence}{spaces}{rp.right_wall}'''
        
		# add floor
		boxified += '\n' + rp.bottom_left_corner + (rp.bottom * ceiling) + rp.bottom_right_corner 
		return boxified

	floor, ceiling, width, parsed_message = calculate_box(parse_message(message))
	return construct_box(floor, ceiling, width, parsed_message)


# write to a file with a message and a pathway TO BE FINISHED
def write_out(file_path : str, filename : str, message : str):
    file = Path(file_path + '/', filename)
    with open(file, 'w') as fh:
        try:
            fh.write(message)
        except FileNotFoundError:
            print(f'::ERROR:: in write_out(), check file pathway for errors, {file_path}')


# limit the lenth of a string or list of strings passed to the function
def len_limiter(data : (list, str), str_limit : int):
    limit_length = str_limit
    # if the data passed is a list of strings, iterate over each and limith the length
    if type(data) == list:
        try:
            new = [str(item)[0:limit_length] for item in data]
            return new
        except (TypeError, IndexError, ValueError) as e:
            print(f'::ERROR:: at "len_limiter()", input data cannot be iterated "{data}"')
    
    # if the data is passed as a string, limit the length and pass it back
    elif type(data) == str:
        try:
            return data[0:limit_length]
        except (TypeError, IndexError, ValueError) as e:
            print(f'::ERROR:: at "len_limiter()", input data cannot be iterated "{data}"')
    else:
        print(f'::ERROR:: at "len_limiter()", input data is not str or list type "{data}"')


# CHECKLIST CREATION FUNCTIONS vvv
# put items into a checklist format and create a dictionary to go with it
def create_checklist(checklist_dict : dict, prefix_id : str):
    graphic = ''

    for count, key in enumerate(checklist_dict):
        graphic += f'''{prefix_id}{count + 1}.[{rp.t_f_standins[checklist_dict[key]]}] {key}\n'''
    graphic = graphic[0:-1]
    return graphic


def create_checklist_dict(items : list, default_val : bool):
    mixed_d = {}
    
    for item in items:
        mixed_d.update({item : default_val})
    
    return mixed_d
# CHECKLIST CREATION FUNCTIONS ^^^


# used by [execute_queries]
# fetch one result for a query
def retrieve_all(database : str, queries : list):
    r = cn.select_all(database, queries)
    return r


# used by [execute_queries]
# fetch all results for a query
def retrieve_one(database : str, queries : list):
    r = cn.select_one(database, queries)
    return r


# used by [execute_queries]
# fetch a certain number of results
def retrieve_some(database : str, queries : list, result_limit : int):
    r = cn.select_all(database, queries)
    return r


# execute a list of queries in a particular database and return resulting list with results to parent function
def execute_queries(database : str, queries : list, limit_results=False, results_limit=1):
    results = []
    mult_q = False

    # determine if there are more than one queries in the list for efficiency
    if len(queries) >= 2:
        mult_q = True
    else:
        mult_q = False

    if limit_results is False:
        results = retrieve_all(database, queries)
    elif limit_results is True and results_limit == 1:
        results = retrieve_one(database, queries)
    else:
        results = retrieve_some(database, queries,results_limit)
    
    return results


# must have [["database", ["table", ["var", "var"]], ["table2", ["var", "var"]]]]
db_search_params = [['testing', ['tdata', ['firstname', 'lastname']], ['adata', ['t1', 't2']] ]]

# for db in db_search_params add this search string
search_string = ''
and_list = ['ass', 'butt', 1, 3]
or_list = ['balls', 'taint']

# add prefix "LIMIT"
results_limit = 0


# when passed the base information will format it into sql query(or queries)
def sql_query_generator(db_search_params, and_list, or_list, limit_results=False, results_limit=1):

    def deconstruct_params(db_search_params, limit_results, results_limit, and_list, or_list):
        # for database list in the search params,
        result_sets = []
        for lst in db_search_params:
            database = lst[0]
            results = []

            # iterate through the table, variable sets in the current databases list and isolate the table name and var list
            for i in range(len(lst) - 1):
                tb_vars = lst[i + 1]
                table = tb_vars[0]
                var_list = tb_vars[1]
                results.extend(construct_sql_query(database, table, var_list, limit_results, results_limit, and_list, or_list))    
            result_sets.append(results)
        
        return result_sets


    def construct_search_string(var_name, and_list, or_list):
        string = ''
        
        for thing in and_list:
            try:
                string += f'{var_name}={int(thing)} AND '
            except (TypeError, ValueError):
                string += f'{var_name}="{thing}" AND '
        string = string[0:-5]
        
        for stuff in or_list:
            try:
                string += f' OR {var_name}={int(stuff)}'
            except (TypeError, ValueError):
                string += f' OR {var_name}="{stuff}"'
            
        return string


    def construct_sql_query(database : str, table : str, variables : list, limit_results, results_limit, and_list, or_list):
        limit_insert = f'LIMIT {results_limit}'
        var_insert = ''
        finished_query = []

        # parse variables to create a string in accordance with SQL
        for var in variables:
            search_params_insert = construct_search_string(var, and_list, or_list)

            query = f'SELECT * FROM {table} WHERE {search_params_insert}'
            finished_query.append(query)
        return finished_query




    # deconstruct_params(db_search_params, limit_results, results_limit)
    search_commands = deconstruct_params(db_search_params, limit_results, results_limit, and_list, or_list)
    return search_commands


'''
^^^ CORE FUNCTIONS ^^^
'''

'''
vvv GRAPHICAL GENERATORS vvv
'''


# turn a list of strings into a formated one line string for displaying information
def inline_list_format(rdata : list, entry_max : int):
    data = len_limiter(rdata, entry_max)

    inline = ''
    for count, entry in enumerate(data):
        inline += entry

        if count == len(data):
            pass
        else:
            inline += rp.inline_separator
    return inline


# iterate over the database config to generate a visual of a database
def core_db_generator(database : str, inc_vars_types : bool):
    conn, tables, vars, rawtypes = cn.db.retr_attr(database)
    types = [item for item in rawtypes]
    
    # Add database header, db and it's prefix as well as the table section header
    visual = f'''{rp.db_header}
{boxify(rp.db_prefix + conn)}
{rp.table_header}'''

    for count, table in enumerate(tables):
        # add table prefix and table
        visual += f'\n{rp.table_prefix}{table}'
        
        # if include variables and types is true, iterate and add them to the string
        if inc_vars_types is True:
            # select the set of variables and variable types for the current table
            vrset = vars[count]
            tyset = types[count]
            # add the variables and their types with preceding headers
            visual += '\n' + rp.var_types_header
            for num in range(len(vars[count])):
                visual += f'''\n{rp.var_prefix}{vrset[num]}'''
                visual += f'''\n{rp.types_prefix}{vars_types[tyset[num]]}'''
        else:
            visual += rp.opt_table_postfix
    return visual   


# return a formatted graphic of one selected database
def db_visual_1(database : str, inc_vars_types : bool):
    return core_db_generator(database, inc_vars_types)


# return a formatted graphic of all the databases 
def dbs_visual_1(inc_vars_types : bool, boxed : bool()):
    result = ''
    for dbname in cn.db_inst:
        if boxed is True:
            result += "\n" + boxify(core_db_generator(dbname, inc_vars_types) + '\n')
        else:
            result += core_db_generator(dbname, inc_vars_types) + '\n'
    return result


# return a formatted graphic list of all databases and their connection paths,
# also returns a list of the databases
def dbs_visual_2(boxed : bool):
    visual = ''
    db_names = []

    visual += rp.alt_db_header
    for count, item in enumerate(cn.db_inst):
        visual += f"""\n{count + 1}.{item}"""
        visual += f"""\n┗█CONNECTION PATH: {(cn.db.find(item, 'conn'))}\n"""
        db_names.append(item)
    if boxed is True:
        return boxify(visual), db_names
    elif boxed is False:
        return visual, db_names
    else:
        print(f'::ERROR:: at vis_db_list. passed variable "{boxed}" must be bool')


'''
^^^ GRAPHICAL GENERATORS ^^^
'''

'''
vvv NAVIGATION FUNCTIONS vvv
'''


# used to create dictionaries for menu navigation. 
def create_nav_dict(page_name : str, opt_keys=[], opt_values=[]):
    def_keys = []
    def_values = []
    #every function dictionary maker should have a 'd'before their function name to avoid collision
    def dpage_template():
        keys = []
        values = []
        return keys, values
    
    # main menu navigation items
    def dpage_main():
        keys = ['1', '2', '3', '4', '5']
        values = [page_sql_search, page_dis_dbs, '', '', '']
        return keys, values

    # search page navigation items 
    def dpage_sql_search():
        keys = ['<', '<write', '<<', '<del', '<clear', '<sel']
        values = ['', '', del_last_queue, slice_queue, clear_queue, select_db]
        return keys, values

    def dpage_mult_db():
        keys = ['<r', '<a']
        values = [reset_dbs, sel_all_dbs]
        return keys, values

    # vvv REMEMBER TO ADD NEW LISTINGS vvv
    # contain calls to the different pages used. must be updated for navigation to work
    pages = {'dpage_main':dpage_main,
             'dpage_sql_search':dpage_sql_search,
             'dpage_mult_db':dpage_mult_db}
    try:
        def_keys, def_values = pages[page_name]()
    except (KeyError):
        print(f'::ERROR:: the page you requested "{page_name}" is not in the index or the function call is incorrect')
        exit()
    
    # add any extra options the user passes
    if len(opt_keys) >= 1:
        def_keys.extend(opt_keys)
        def_values.extend(opt_values)
    else:
        pass
    return create_dict(def_keys, def_values)
    

# uses a page name to generate dicts and everything else for navigating menus 
def menu_navigation(page_name, page_func, prec_func=None, exit_char='<<<'):
    dict_name = f'd{page_name}'
    nav_dict = create_nav_dict(dict_name)

    # run any preceding functions needed
    if prec_func != None:
        try:
            prec_func()
        except NameError:
            print(f'::ERROR:: passed preceding function "{prec_func}" is not callable')

    complete = False
    error = ''
    user_i = ''
    while complete is False: 
        clear()
        page_func()
        print(error)
        error = ''
        
        user_i = input()
        if user_i == exit_char:
            return
        else:
            pass

        try:
            ex = nav_dict[user_i]
            try:
                ex()
                pass
            except TypeError:
                error = "░░oops, that option is not finished yet, sorry░░"          
        except KeyError as e:
            error = f"░░oops, please choose an available option, \"{user_i}\" is not an option!░░"


# # execute functions to alter live graphics without navigating to another page
def option_nav(page_name, page_func, failfunc=None, exit_char='<<<'):
    global gl_ui
    dictionary = create_nav_dict(f'''d{page_name}''')
    error = ''
    gl_ui = ''
    complete = False

    while complete is False:
        clear()
        page_func()
        print(error)

        gl_ui = input()

        # return to parent function if the user input is == to the exit character
        if gl_ui == exit_char:
            return
        else:
            pass
        
        # to to find the user input in the current navigation dictionary
        try:
            ex = dictionary[gl_ui]
            # try to execute result from dictionary and if it fails it is not finished yet
            try:
                ex()
            except TypeError:
                error = f"░░oops, that option \"{ex}\" cannot be called, sorry░░"
        except KeyError:
            if failfunc == None:
                error = f"░░oops, please choose an available option, \"{gl_ui}\" is not an option!░░"
            else:
                try:
                    failfunc()
                except NameError:
                    error = f"░░oops, that option \"{failfunc}\" cannot be called, sorry░░"
        gl_ui = ''


'''
^^^ NAVIGATION FUNCTIONS ^^^
'''

'''
vvv QUEUE COMMANDS vvv
'''


# remake the queue and renumber items for display
def update_queue():
    global gl_ui, queue_graphic, queue_history

    queue_graphic = ''
    if gl_ui != '':
        queue_history.append(gl_ui)
    else:
        pass

    for count, item in enumerate(queue_history):
        if count == 0:
            queue_graphic += f'''{rp.queue_prefix}{count}.{item}'''
        else:
            queue_graphic += f'''\n{rp.queue_prefix}{count}.{item}'''


# allows user to remove a specific command from the queue when called
def slice_queue():
    global gl_ui, queue_history, queue_graphic
    gl_ui = ''
    error = ''

    complete = False
    while not complete:
        update_queue()
        clear()
        print(rp.queue_slice)
        print(rp.bl_cmd_queue)
        print(queue_graphic)
        print(rp.bl_cmd_queue_footer)
        print(error)
        error = ''
        ui = input()
        
        if ui == '<<<':
            return
        else:
            try:
                del queue_history[int(ui)]
            except (TypeError, ValueError, IndexError) as e:
                error = f'''┃░oops, "{ui}" is not a valid option░┃'''


# clears the command queue when called
def clear_queue():
    global queue_history, gl_ui
    gl_ui = ''
    queue_history.clear()
    update_queue()
    return


def del_last_queue():
    global queue_history, gl_ui
    gl_ui = ''
    del queue_history[-1]
    update_queue()
    return


'''
^^^ QUEUE COMMANDS ^^^
'''

'''
vvv PAGE UPDATE FUNCTIONS vvv
'''


def checklist_dbs():


def page_mult_db():
    option_nav('page_mult_db', print_mult_db, exit_char='<')


def print_mult_db():
    global gl_checklist1

    database_checklist_init(False, False)
    header = rp.dbs_sel_header
    checklist = create_checklist(gl_checklist_dict1, '')
    main = f"""{header}
{checklist} """
    print(main)


def reset_dbs():
    database_checklist_init(True, False)


def sel_all_dbs():
    global db_sel_state
    if db_sel_state is False:
        db_sel_state = True
        database_checklist_init(True, True)
    elif db_sel_state is True:
        db_sel_state = False
        database_checklist_init(True, False)
    else:
        pass
    


# if called, reset all the databases to be set to false in the dict if the list is empty
def database_checklist_init(reset : bool, default : bool):
    global gl_checklist1, gl_checklist_dict1
    
    if gl_checklist1 == [] or reset is True:
        cn.rds()
        # fetch all the database names
        gl_checklist1 = [db for db in cn.db_inst]
        # create a dict with the database names and a default boolean value
        gl_checklist_dict1 = create_checklist_dict(gl_checklist1, default)
    else:
        pass
    return


# [select database] loops through and ask the user to select the database to be used with a tool
def select_db():
    global curr_db_name
    error = ''

    db_names = dbs_visual_2(False)[1]
    complete = False
    while not complete:  
        print_select_db()
        print(error)
        error = ''
        user_i = input()
        try:
            if int(user_i) <= len(db_names) and int(user_i) >= 1:
                curr_db_name = db_names[(int(user_i) - 1)]
                print(curr_db_name)
                complete = True
            else:
                error = rp.select_db_fail
        except (TypeError, ValueError):
            error = rp.select_db_fail
    return


# [select database] prints the graphical component for the select_db function
def print_select_db():
    
    main = f'''{rp.select_db_menu}
{dbs_visual_2(True)[0]}
'''
    clear()
    print(main)


'''
^^^ PAGE UPDATE FUNCTIONS ^^^
'''

'''
vvv PAGE FUNCTIONS vvv
'''


# [page main] will startup the toolbox menu and tools
def startup():
    menu_navigation('page_main', page_main)
    return


# [page main] displays the toolkit main page
def page_main():
    # the main page of the toolkit main
    main = f'''{rp.toolkit_main_menu}
{dbs_visual_2(True)[0]}
CNDBL v-{cn.cndbl_version}'''
    print(main)


def page_sql_search():
    global curr_db_name
    if curr_db_name == "":
        select_db()
    else:
        pass

    option_nav('page_sql_search', print_sql_page_search, failfunc=update_queue)
    return


def print_sql_page_search():
    global queue_graphic, results_graphic, curr_db_name
    main = f'''{rp.bl_search_db}
{boxify(rp.db_prefix + cn.db.find(curr_db_name, 'conn'))}
{rp.bl_cmd_queue}
{queue_graphic}
{rp.bl_cmd_queue_footer}
{boxify(rp.results_header)}
{results_graphic}'''
    print(main)


# [page display dbs] display the databases and their components
def page_dis_dbs():
    print_page_dis_dbs()
    input('press [ENTER] to return to menu')
    return


# [page display dbs]
def print_page_dis_dbs():
    # print the main page for toolkit display dbs
    clear()
    main = f'''{rp.bl_all_db_header}
    {dbs_visual_1(True, True)}'''
    print(main)


def page_crit_search():
    # checklist globals are used for creating dynamic menus like table, database, and variable selection
    global gl_checklist1, gl_checklist_dict1
    global gl_checklist2, gl_checklist_dict2

    database_checklist_init(False, False)
    db_sel_graphic = create_checklist(gl_checklist_dict1, '')

    print(gl_checklist_dict1)
    print(db_sel_graphic)

    # print(rp.bl_criteria_search_db)


'''
^^^ PAGE FUNCTIONS ^^^
'''

'''
vvv FOOTER VVV
'''


# cn.rds()

# qlist = ['SELECT firstname FROM tdata WHERE firstname="stuff"', 'SELECT lastname FROM tdata']


'''
ass AND butt OR balls OR ass

ass AND butt OR balls
SELECT firstname FROM tdata WHERE firstname="ass" AND firstname="butt" OR firstname="balls" LIMIT 2

'''

# a = sql_query_generator(db_search_params, and_list, or_list)
# for t in a:
#     for thing in t:
#         print(thing)
cn.rds()
# page_mult_db()

# database_checklist_init(True, False)
# print(create_checklist(gl_checklist_dict1, ''))

# database_checklist_init(True, True)
# print(create_checklist(gl_checklist_dict1, ''))

# database_checklist_init(True, False)
# print(create_checklist(gl_checklist_dict1, ''))