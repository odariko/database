from model import *
import view

if __name__ == "__main__":
    db = DB()
    db.search(input(), input())

    #db.add_row('Authors', {'full_name': 'Author0', 'date_of_birth': '1992-10-14'})
    #db.add_row('Authors', {'full_name': 'Author1', 'date_of_birth': '1980-10-14'})

    #db.edit_value('Authors', 'full_name', 'date_of_birth', '1999-10-14', 'Author1')
    #db.del_row('Authors', 'full_name', 'Author1')

    #db.add_row('Test', {'num': 666})
    #db.edit_value('Test', 'num', 'val', 'ok222ok', 222)
    #db.del_row('Test', 'num', 666)
