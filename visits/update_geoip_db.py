"""Module is intended for updating geolite_max_mind database.

Module uses public database provided in csv files to update
database PostgreSQL. 
Must be used in command line mode to upload datinfornation to database
"""
import os
import sys
import psycopg2
from medsmartcom.settings import GEOLITE_DB_NAME, GEOLITE_DB_HOST, GEOLITE_DB_PORT, GEOLITE_DB_USER, GEOLITE_DB_CONNECTION_OPTION

commands = {'update': 'update database from csv files geolite2', 
            'info': 'show information about tables in database', 
            'help': 'show information about commands'}

progress_max = 0
progress_interval = 0

def init_progress(msg, total):
    """Initializes progress line in console"""
    progress_max = os.get_terminal_size().columns - 3 - len(msg)
    if progress_max > total:
        progress_max = total
    global progress_interval
    progress_interval = int(total/progress_max)
    print(msg, end = '', flush = True)
    print('[', end = '', flush = True)
    print(progress_max * ' ' + ']', end = '', flush = True)
    print((progress_max + 1) * '\b', end = '', flush = True)

def progress(i):
    """Shows progress of update process"""
    global progress_interval
    if (i%progress_interval) == 0:
        print('>', end = '', flush=True)
        print('\b', end = '', flush=True)
        print('=', end = '', flush=True)
   
def run_command(cmd, args):
    """Starts command selected by user"""
    cmd = cmd.lower().strip()
    for key in commands:
        if cmd == key or cmd == '--'+key or cmd == '-' + key[0]:
            if cmd == 'info':
                info()
            elif cmd == 'update':
                update(args)
            elif cmd == 'help':
                help_command()
            print('')
            print(key + ' command executed!')
            return
    print('Unknown command - ' + cmd.strip('-'))

def help_command():
    """Shows helps information about provided commands"""
    for key in commands:
        print('-' + key[0] + ', ' + '--' + key + '\t' + commands[key])

def normalize_line(line):
    """Normalizes text from csv file before parsing data columns"""
    inside_str = False
    str = ''
    for i in line:
        if i == '"':
            inside_str = not inside_str
        if not inside_str and i == ',':
            str += '#'
        else:
            str += i 
    str = str.replace('\'', '`')
    return str

def insert_into_table_from_file(table, file_path, msg):
    """Parses csv file and insert contained information to database"""
    cnt = get_count_of_rows_in_table(table)
    #if cnt != 0:
    #    print('Update canceled! There are ' + str(cnt) + ' rows in table ' + table)
    #    return
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        #cur.execute('delete from ' + table)
        #conn.commit()
        file = open(file_path, 'r')
        total_lines = 0;
        for line in file:
            total_lines += 1  
        total_lines -= 1
        file.close()
        file = open(file_path, 'r')
        i = -1
        init_progress(msg, total_lines)
        for line in file:
            i+= 1
            progress(i)
            if i <= cnt:
                continue
            items = normalize_line(line).split('#')
            columns = get_columns_of_table(table)
            cmd = 'insert into ' + table + '(' + ','.join(columns) + ') values(' + ','.join(['\'' + str(item) + '\'' if item.strip() != '' else 'null' for item in items]) + ')'
            cur.execute(cmd)
            if i % 100 == 0:
                conn.commit()
    finally:
        file.close()
        conn.commit()
        conn.close()
    print('')

def update(args):
    """Update command.
    
    Reads files form current work directory and inserts contained data
    to table. File and proper table are matched by names: 
    algorithm slice file names and table names for matching them
    """
    cwd = os.getcwd()
    if not args:
        for walk_gen in os.walk(cwd):
            args = walk_gen[2]
            break
    tables = get_tables()
    for file in args:
        file_ = file.lower()
        file_ = file_.replace('-', '_')
        file_ = file_.replace('.', '_')
        file_name_parts = file_.split('_')
        set_file_name_parts = set(file_name_parts)
        for table in tables:
            table_name_parts = table.split('_')
            set_table_name_parts = set(table_name_parts)
            if all(x in set_file_name_parts for x in set_table_name_parts):
                insert_into_table_from_file(table, cwd + '/' + file, file + ' => ' + table + ': ')

def get_tables():
    """Returns list of tables in database"""
    tables = list()
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute('select table_name from information_schema.tables where table_schema not in (\'information_schema\', \'pg_catalog\') order by 1')
        rows = cur.fetchall()
        for row in rows:
            tables.append(row[0])
    finally:
        conn.close()
    return tables

def get_columns_of_table(table):
    """Returns list of columns of table"""
    columns = list()
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute('select column_name from information_schema.columns where table_name =\'' + table + '\' and table_schema = \'public\'')
        rows = cur.fetchall()
        for row in rows:
            columns.append(row[0])
    finally:
        conn.close()
    return columns

def get_count_of_rows_in_table(table):
    """Returns count of rows of table"""
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute('select count(*) from ' + table)
        row = cur.fetchone()
        cnt = row[0]
        return cnt
    finally:
        conn.close()
    return 0

def info():
    """Informational command intended to show table information within database"""
    tables = get_tables()
    try:
        print('--------------------------------------------')
        print('tables in db:')
        for table in tables:
            print(table)
        for table in tables:
            print('--------------------------------------------')
            print(table + ': ' + str(get_count_of_rows_in_table(table)) + ' rows')
    except Exception:
        print('erorrrr!')
def connect_to_db():
    return psycopg2.connect(host=GEOLITE_DB_HOST, port = GEOLITE_DB_PORT, database=GEOLITE_DB_NAME, user=GEOLITE_DB_USER, options = GEOLITE_DB_CONNECTION_OPTION)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        run_command(cmd, sys.argv[2:])
    else:
        help_command()