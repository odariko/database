import base
import controller as ctrl
from controller import *


class DB:
    def __init__(self):

        # self.connection = psycopg2.connect(database='postgres', user='postgres',
        #                                    password='nvidia123', host='localhost')

        self.session = base.Session()
        # 1st task

    def add_row(self, table_name, fields_name):
        try:
            add_row1(self, table_name, fields_name)
        except(Exception, self.session) as error:
            print(error)
            return False

    def del_row(self, table_name, key, value):
        try:
            del_row1(self, table_name, key, value)
        except(Exception, self.session) as error:
            print(error)
            return False

    def edit_value(self, table_name, key, key_change, new_val, key_val):
        try:
            edit_value1(self, table_name, key, key_change, new_val, key_val)
        except(Exception, self.session) as error:
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
                            val_dict.update({el: val})
                        elif 'int' in ctrl.get_column_type(self.connection, table_name, el):
                            val_dict.update({el: 0})
                        elif 'char' in ctrl.get_column_type(self.connection, table_name, el):
                            val_dict.update({el: "NULL"})
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
            if ctrl.check_for_present(self.session, column_name, *tabels):
                for el in tabels:
                    print("Please input filter type for each column: ")
                    filter = input()
                    if filter.lower() == 'between':
                        print("Please input column name and first and second limits")
                        ctrl.search_between(self.session, el, input(), input(), input())
                    elif filter.lower() == 'is null':
                        print("Please input column name")
                        ctrl.search_is_null(self.session, el, input())
                    elif filter.lower() == 'easy':
                        print("Please input column name and value")
                        ctrl.search_easy(self.session, el, input(), input())
                    else:
                        print("Missing option")
        except(Exception, self.session) as error:
            print(error)
            return False

    def __del__(self):
        #self.connection.close()
        self.session.close()


if __name__ == '__main__':
    # print(get_class_by_tablename('Readers'))
    db = DB()
    #db.edit_value('Test', 'num', 'val', 'ok222ok', 222)
    #db.del_row('Test', 'num', 666)
    #db.search(input(), input())
