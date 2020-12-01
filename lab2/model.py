import psycopg2
import controller as ctrl
from controller import *
from view import *

class DB:
    def __init__(self):
        self.connection = psycopg2.connect(database='postgres', user='postgres',
                               password='nvidia123', host='localhost')
        # 1st task
    def add_row(self, table_name, fields_name):
        try:
            add_row1(self, table_name, fields_name)
        except(Exception, self.connection) as error:
            print(error)
            return False

    def del_row(self, table_name, key, value):
        try:
            del_row1(self, table_name, key, value)
        except(Exception, self.connection) as error:
            print(error)
            return False

    def edit_value(self, table_name, key, key_change, new_val, key_val):
        try:
            edit_value1(self, table_name, key, key_change, new_val, key_val)
        except(Exception, self.connection) as error:
            print(error)
            return False

        # 2nd task

    def auto_gen(self, table_name, column_name, number):
        try:
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
        except(Exception, self.connection) as error:
            print(error)
            return False


        # 3rd task

    def search(self, column_name, *tabels):
        try:
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
        except(Exception, self.connection) as error:
            print(error)
            return False

    def __del__(self):
        self.connection.close()
