import psycopg2
import controller as ctrl
from view import *

class DB:
    def __init__(self):
        self.connection = psycopg2.connect(database='postgres', user='postgres',
                               password='nvidia123', host='localhost')
        # 1st task
    def add_row(self, table_name, fields_name):
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

    def del_row(self, table_name, key, value):
        try:
            cur = self.connection.cursor()
            cur.execute("DELETE FROM {} WHERE {} = %s".format(table_name, key), (value,))
            rows_deleted = cur.rowcount
            self.connection.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    def edit_value(self, table_name, key, key_change, new_val, key_val):
        try:
            cur = self.connection.cursor()
            cur.execute("UPDATE {} Set {} = %s WHERE {} = %s;".format(table_name, key_change, key), (new_val, key_val))
            updated_rows = cur.rowcount
            self.connection.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

        # 2nd task

    def auto_gen(self, table_name, column_name, number):
        if 'int' in ctrl.get_column_type(self.connection, table_name, column_name):
            value_list = ctrl.auto_gen_int(self.connection, number)
            existing_value = ctrl.column_data(self.connection, table_name, column_name)

            def value_dict(val):
                val_dict = {}
                for el in ctrl.get_input_format(self.connection, table_name):
                    if el == column_name:
                        val_dict.update({el : val})
                    elif 'int' in ctrl.get_column_type(self.connection, table_name, el):
                        val_dict.update({el : 0})
                    elif 'char' in ctrl.get_column_type(self.connection, table_name, el):
                        val_dict.update({el : "NULL"})
                return val_dict

            for el in value_list:
                if el[0] not in existing_value:
                    self.add_row(table_name, value_dict(el[0]))


        # 3rd task

    def search(self, column_name, *tabels):
        if ctrl.check_for_present(self.connection, column_name, *tabels):
            for el in tabels:
                print("Please input filter type for each column: ")
                filter = input()
                if filter.lower() == 'between':
                    print("Please input column name and first and second limits")
                    ctrl.search_between(self.connection, el, input(), input(), input())
                elif filter.lower() == 'is null':
                    print("Please input column name")
                    ctrl.search_is_null(self.connection, el, input())
                elif filter.lower() == 'easy':
                    print("Please input column name and value")
                    ctrl.search_easy(self.connection, el, input(), input())
                else:
                    print("Missing option")

    def __del__(self):
        self.connection.close()
