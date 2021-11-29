#Danny Hong ECE-464 Databases Problem Set 1 Part 2

import pytest

from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.sql.selectable import subquery

engine = create_engine(
      "mysql+pymysql://root:danny0515@127.0.0.1:3306/sailors", echo = True)

connect = engine.connect()

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime

Base = declarative_base()

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return "<Sailor(id = %s, name = '%s', rating = %s, age = %s)>" % (self.sid, self.sname, self.rating, self.age)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key = True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation',
                                backref = backref('Boat', cascade = 'delete'))

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color)

from sqlalchemy import PrimaryKeyConstraint

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailors = relationship('Sailor', 
                           backref = backref('Reservation', cascade = 'delete'))
    boats = relationship("Boat", 
                           backref = backref('Reservation', cascade = 'delete'))

    def __repr__(self):
        return "<Reservations(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day)

from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind = engine)
s = session()

def check_queries(sql_query, orm_table):
    sql_table = connect.execute(sql_query) #Executes the result from the sql query.

    sql_array = []
    orm_array = []

    for row_1 in sql_table:
        sql_array.append(row_1)
    for row_2 in orm_table:
        orm_array.append(row_2)

    return sql_array == orm_array #Checks if the list from the sql query matches the list from the orm one.

from sqlalchemy import desc, distinct, func
from sqlalchemy.orm import aliased

def test_1():
    sql = "select Boats.bid, Boats.bname, count(*) as Number_of_Reservations from Boats, Reserves where Boats.bid = Reserves.bid group by Boats.bid having Number_of_Reservations > 0;"
    orm = s.query(Reservation.bid, Boat.bname, func.count("Number_of_Reservations")).join(Reservation).group_by(Boat.bid).having(func.count("Number_of_Reservations") > 0)
    assert check_queries(sql, orm)

def test_2():
    sql = "select Sailors.sid, Sailors.sname from Sailors, Boats where not exists(select Boats.bid from Boats where not exists(select Reserves.bid from Reserves where Reserves.bid = Boats.bid and Boats.color = 'red'));"
    sub_query_1 = s.query(Boat.bid).filter(Boat.color == 'red')
    orm = s.query(Sailor.sid, Sailor.sname).filter(Boat.color == 'red').join(Reservation).group_by(Reservation.sid).having(func.count(distinct(Reservation.bid)) == sub_query_1.count())
    assert check_queries(sql, orm)

def test_3():
    sql = "select distinct Sailors.sid, Sailors.sname from Sailors, Reserves, Boats where Boats.color = 'red' and Sailors.sid = Reserves.sid and Reserves.bid = Boats.bid and Sailors.sid not in(select Sailors.sid from Sailors, Reserves, Boats where Boats.color != 'red' and Sailors.sid = Reserves.sid and Boats.bid = Reserves.bid);"
    sub_query_1 = s.query(Reservation.sid).join(Boat).filter(Boat.color == 'red')
    sub_query_2 = s.query(Reservation.sid).join(Boat).filter(Boat.color != 'red')
    orm = s.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.in_(sub_query_1)).filter(Sailor.sid.notin_(sub_query_2))
    assert check_queries(sql, orm)

def test_4():
    sql = "select Boats.bid, Boats.bname, count(*) as Number_of_Reservations from Boats, Reserves where Boats.bid = Reserves.bid group by Boats.bid order by Number_of_Reservations desc limit 1;"
    orm = s.query(Boat.bid, Boat.bname, func.count("Number_of_Reservations")).join(Reservation).group_by(Reservation.bid).order_by(desc(func.count("Number_of_Reservations"))).limit(1)
    assert check_queries(sql, orm)

def test_5():
    sql = "select Sailors.sid, Sailors.sname from Sailors where Sailors.sid not in (select Reserves.sid from Reserves inner join Boats on Boats.bid = Reserves.bid where Boats.color = 'red') order by Sailors.sid;"
    sub_query_1 = s.query(Reservation.sid).join(Boat).filter(Boat.color == 'red')
    orm = s.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.notin_(sub_query_1))
    assert check_queries(sql, orm)

def test_6():
    sql = "select avg(Sailors.age) as Average_Sailors_Age from Sailors where Sailors.rating = 10;"
    orm = s.query(func.avg(Sailor.age)).filter(Sailor.rating == 10)
    assert check_queries(sql, orm)

def test_7():
    sql = "select Sailors.sid, Sailors.sname, Sailors.rating, Sailors.age from Sailors having Sailors.age <= all(select Sailors_1.age from Sailors Sailors_1 where Sailors.rating = Sailors_1.rating) order by Sailors.rating;"
    Sailor_1 = aliased(Sailor)
    orm = s.query(Sailor.sid, Sailor.sname, Sailor.rating, Sailor.age).having(Sailor.age <= s.query(func.min(Sailor_1.age)).filter(Sailor.rating == Sailor_1.rating)).order_by(Sailor.rating)
    assert check_queries(sql, orm)

def test_8():
    sql = "select X.bid, X.bname, X.sid, X.sname, max(Number_of_Reservations) as Number_of_Reservations from(select Sailors.sname, Boats.bname, Reserves.sid, Reserves.bid, count(*) as Number_of_Reservations from Sailors, Boats, Reserves where Sailors.sid = Reserves.sid and Boats.bid = Reserves.bid group by Reserves.sid, Reserves.bid order by Number_of_Reservations) as X group by X.sid, X.bid order by X.bid;"
    orm = s.query(Boat.bid, Boat.bname, Sailor.sid, Sailor.sname, func.count("Number_of_Reservations")).filter(Sailor.sid == Reservation.sid).filter(Boat.bid == Reservation.bid).group_by(Sailor.sid).group_by(Boat.bid).order_by(Boat.bid)
    assert check_queries(sql, orm)

test_1()
test_2()
test_3()
test_4()
test_5()
test_6()
test_7()
test_8()