from time_decor import *
import psycopg2


def show(con, table_name):
    try:
        cur = con.cursor()
        cur.execute("""SELECT * FROM {}""".format(table_name))
        return cur.fetchall()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

@timer
def search_between(con, table_name, column_name, limit1, limin2):
        try:
            cur = con.cursor()
            cur.execute("""SELECT * FROM public."{}" 
            WHERE {} BETWEEN {} AND {}""".format(table_name, column_name, limit1, limin2))
            print(*cur.fetchall())
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

@timer
def search_is_null(con, table_name, column_name):
        try:
            cur = con.cursor()
            cur.execute("""SELECT * FROM public."{}" 
            WHERE {} = '0' """.format(table_name, column_name, column_name, column_name ))
            print(cur.fetchall())
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

@timer
def search_easy(con, table_name, column_name, value):
        try:
            cur = con.cursor()
            cur.execute("""SELECT * FROM public."{}" 
            WHERE {} = '{}' ORDER BY {}""".format(table_name, column_name, value, column_name))

            print(cur.fetchall())
            return cur.fetchall()[0]
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

def get_input_format(con, table_name):
        cur = con.cursor()
        value = []

        cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS" \
                    " WHERE TABLE_NAME = '{}'".format(table_name))
        info = table_name
        for column in cur.fetchall():
            value.append(*column)
        print(value)
        return value

def check_for_present(con, column_name, *tabels):
        for el in tabels:
            val_list = []
            print(el)
            columns = get_input_format(con, el)
            if column_name not in columns:
                print('{} is not in {} table'.format(column_name, el))
                return False
        return True

def get_list_of_tabels(con):
        cur = con.cursor()
        cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in cur.fetchall():
            print(table)

def get_column_type(con, table, column):
        try:
            cur = con.cursor()
            cur.execute("""SELECT column_name, data_type FROM information_schema.columns
               WHERE table_name = '{}'""""".format(table))
            for table in cur.fetchall():
                if column in table: return table[1]
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

def auto_gen_int(con, rows_number):
            try:
                cur = con.cursor()
                cur.execute("SELECT num "
                                "FROM GENERATE_SERIES(1, {}) AS s(num) "
                                "ORDER BY RANDOM() "
                                "LIMIT {}".format(rows_number, rows_number))
                return cur.fetchall()
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)

def  auto_gen_char(con, rows_number):
    try:
        cur = con.cursor()
        lst = []
        for i in range(rows_number):
            cur.execute("SELECT CHR(trunc(65 + random()*25)::int) || "
            "CHR(trunc(97 + random())::int) || CHR(trunc(97 + random()*25)::int) || "
            "CHR(32) || CHR(trunc(65 + random()*25)::int) || "
            "CHR(trunc(97 + random()*25)::int) || CHR(trunc(97 + random()*25)::int)")
            lst.append(cur.fetchall()[0][0])
        return tuple(lst)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def column_data(con, table_name, column_name):
        try:
            cur = con.cursor()
            cur.execute('SELECT {} FROM public."{}"'.format(column_name, table_name))
            values = []
            for val in cur.fetchall():
                values.append(*val)
            return values
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

def add_row1(self, table_name, fields_name):
        i, y = '', ''
        values = ''
        for el in fields_name.keys():
            i += el + ','
            y += '%s,'
            values += "'{}',".format(fields_name[el])
        table = 'INSERT INTO public."{}"({}) VALUES({});'.format(table_name, i[:len(i) - 1], y[:len(y) - 1])
        try:
            cur_execute = """cur.execute(table, ({}))""".format(values[:len(values) - 1])
            cur = self.connection.cursor()
            exec(cur_execute)
            self.connection.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Try again")
            self.add_row(input(), {input(): input(), input(): input()})

def del_row1(self, table_name, key, value):
        try:
            cur = self.connection.cursor()
            cur.execute("DELETE FROM {} WHERE {} = %s".format(table_name, key), (value,))
            rows_deleted = cur.rowcount
            self.connection.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

def edit_value1(self, table_name, key, key_change, new_val, key_val):
        try:
            cur = self.connection.cursor()
            cur.execute("UPDATE {} Set {} = %s WHERE {} = %s;".format(table_name, key_change, key), (new_val, key_val))
            updated_rows = cur.rowcount
            self.connection.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
