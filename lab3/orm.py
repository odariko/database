from sqlalchemy.orm import relationship

import base
from sqlalchemy import Column, Integer, String, Date, ForeignKey


class Authors(base.Base):
    __tablename__ = 'Authors'
    full_name = Column('full_name', String(50),  primary_key=True)
    date_of_birth = Column('date_of_birth', Date)
    books_authors = relationship('BooksAuthors')
    readers_authors = relationship('ReadersAuthors')

    def __repr__(self):
        return "<Author(full_name='{}', date_of_birth='{})>"\
            .format(self.full_name, self.date_of_birth)


class Books(base.Base):
    __tablename__ = 'Books'
    title = Column('title', String(50), primary_key=True)
    pages = Column('pages', Integer)
    books_authors = relationship('BooksAuthors')
    readers_books = relationship('ReadersBooks')

    def __repr__(self):
        return "<Book(title='{}', pages={})>".format(self.title, self.pages)


class Readers(base.Base):
    __tablename__ = 'Readers'
    subscription_number = Column('subscription_number', Integer, primary_key=True);
    name = Column('name', String(50))
    readers_authors = relationship("ReadersAuthors")
    readers_books = relationship("ReadersBooks")

    def __repr__(self):
        return "<Readers(subscription_number='{}', name='{}')>"\
            .format(self.subscription_number, self.name)


class BooksAuthors(base.Base):
    __tablename__ = 'Books/Authors'
    title = Column('title', String(50), ForeignKey('Books.title'), primary_key=True)
    full_name = Column('full_name', String(50), ForeignKey('Authors.full_name'), primary_key=True)


class ReadersAuthors(base.Base):
    __tablename__ = 'Readers/Authors'
    subscription_number = Column('subscription_number', Integer,
                                 ForeignKey('Readers.subscription_number'), primary_key=True)
    full_name = Column('full name', String(50), ForeignKey('Authors.full_name'), primary_key=True)
    delivery_date = Column('delivery date', Date)


class ReadersBooks(base.Base):
    __tablename__ = 'Readers/Books'
    title = Column('title', String(50), ForeignKey('Books.title'), primary_key=True)
    subscription_number = Column('subscription_number', Integer,
                                 ForeignKey('Readers.subscription_number'), primary_key=True)


class Test(base.Base):
    __tablename__ = 'Test'
    id = Column(Integer, primary_key=True)
    num = Column('num', Integer)
    val = Column('val', String(50))

    def __repr__(self):
        return "<Test(num='{}', val='{}'>".format(self.num, self.val)


def get_class_by_tablename(tablename):

    for c in base.Base._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


if __name__ == '__main__':

    base.Base.metadata.drop_all(base.engine)
    base.Base.metadata.create_all(base.engine)
    # session = base.Session()

    print(get_class_by_tablename('Test'))
    print(Test)
    obj = Test()


