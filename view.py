def view_add_row(func, table_name, fields_name):
    a = func(table_name, fields_name)
    if not a: print('Try again. This value doesnt exist in parent table!')
    elif a: print("{} was pushed sucssefully".format(fields_name))


def view_del_row(func, table_name, key, value):
    a = func(table_name, key, value)
    if a: print(f"{key} {value} was deleted")
    else:
        print("Try again")
        func(input(), input(), input())


def view_edit(func,  table_name, key, key_change, new_val, key_val):
    a = func(table_name, key, key_change, new_val, key_val)
    if a: print("Was edited succesfully")
    else:
        print("Try again")
        func(input(), input(), input(), input(), input())
