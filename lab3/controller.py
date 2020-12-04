import sqlalchemy
from sqlalchemy import text

from orm import get_class_by_tablename
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
def search_easy(con, table_name, column_name, value):
    try:
        table_class = get_class_by_tablename(table_name)
        col_name = table_class.__dict__[column_name]
        filter_txt = '{} = {}'.format(column_name, value)
        query = con.query(table_class).filter(text(filter_txt)).order_by(col_name)
        print(*query.all())
    except (Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)


@timer
def search_is_null(con, table_name, column_name):
    try:
        table_class = get_class_by_tablename(table_name)
        filter_txt = '{} IS NULL'.format(column_name)
        query = con.query(table_class).filter(text(filter_txt))
        print(*query.all())
    except (Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)


@timer
def search_between(con, table_name, column_name, limit1, limit2):
    try:
        table_class = get_class_by_tablename(table_name)
        filter_txt = '{} BETWEEN {} AND {}'.format(column_name, limit1, limit2)
        query = con.query(table_class).filter(text(filter_txt))
        print(*query.all())
    except (Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)

def get_input_format(con, table_name):

    columns = get_class_by_tablename(table_name).__table__.columns.keys()
    print(columns)
    return columns
    # cur = con.cursor()
    # value = []
    #
    # cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS" \
    #             " WHERE TABLE_NAME = '{}'".format(table_name))
    # info = table_name
    # for column in cur.fetchall():
    #     value.append(*column)
    # print(value)
    # return value


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


def auto_gen_char(con, rows_number):
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
    try:

        obj = get_class_by_tablename(table_name)(**fields_name)
        self.session.add(obj)
        self.session.commit()
        return True
    except(Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)
        self.session.rollback()
        return False


def del_row1(self, table_name, key, value):
    try:
        table_class = get_class_by_tablename(table_name)
        filter_txt = "{} = '{}'".format(key, value)
        self.session.query(table_class).filter(text(filter_txt)).delete(synchronize_session=False)
        self.session.commit()
    except(Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)
        self.session.rollback()
        return False


def edit_value1(self, table_name, key, key_change, new_val, key_val):
    try:
        table_class = get_class_by_tablename(table_name)
        filter_txt = "{} = '{}'".format(key, key_val)
        update_values = {key_change: new_val}
        self.session.query(table_class) \
            .filter(text(filter_txt)) \
            .update(update_values, synchronize_session=False)
        self.session.commit()
    except(Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)
        self.session.rollback()
        return False
