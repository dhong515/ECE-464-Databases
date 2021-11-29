#Danny Hong ECE-464 Databases Problem Set 1 Part 3

import pytest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

engine = create_engine(
      "mysql+pymysql://root:danny0515@127.0.0.1:3306/part3", echo = True)

connect = engine.connect()

session = sessionmaker(bind = engine)
s = session()

metadata = MetaData(engine)

from sqlalchemy import Table, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

reserves = Table('reserves', metadata,
             Column('sid', Integer, primary_key = True),
             Column('bid', Integer, primary_key = True),
             Column('reserved_date', Date, primary_key = True), #Editing the reserves table to include a date of reservation attribute
             Column('returned_date', Date, primary_key = True)) #Editing the reserves table to include a date of return attribute

boats = Table('boats', metadata,
             Column('bid', Integer, primary_key = True),
             Column('bname', String(20)),
             Column('color', String(15)),
             Column('length', Integer),
             Column('cost_per_day', Integer)) #Editing the boats table to include a cost per day attribute

sailors = Table('sailors', metadata,
             Column('sid', Integer, primary_key = True),
             Column('sname', String(15)),
             Column('rating', Integer),
             Column('age', Integer))

#Adding in an employees table consisting of an employee's id, name, wage, and weekly hours worked (which is assumed to be fixed)
employees = Table('employees', metadata, 
             Column('eid', Integer, primary_key = True),
             Column('ename', String(20)),
             Column('wage', Integer),
             Column('weekly_hours_worked', Integer))

metadata.drop_all()
metadata.create_all()

#Reading in each line from the sailors_part3.sql file and getting rid of trailing new lines when reading the file
with open("sailors_part3.sql", "r") as lines:
      for line in lines:
            line = line.strip("\n")
            connect.execute(line)

#Calculating each employee's weekly pay and then adding them together to find the total amount the company has to pay to its employees
def get_total_weekly_employee_pay():
      sql_query = "select employees.eid, employees.ename, employees.wage, employees.weekly_hours_worked from employees order by employees.eid;"
      output = connect.execute(sql_query)
      total_weekly_employee_pay = 0
      for employee in output:
            total_weekly_employee_pay = total_weekly_employee_pay + (employee[2] * employee[3])
      return total_weekly_employee_pay

#Testing to see if the get_total_weekly_employee_pay function is working as intended
def test_1():
      assert get_total_weekly_employee_pay() == 3800

#Calculating the earnings from each boat and then adding them together to find the total amount that the company has earned for its boat renting service
def get_total_boat_earnings():
      sql_query = "select boats.bid, boats.bname, boats.cost_per_day, (reserves.returned_date - reserves.reserved_date + 1) as days_used from boats, reserves where boats.bid = reserves.bid order by boats.bid;"
      output = connect.execute(sql_query)
      total_boat_earnings = 0
      for boat in output:
            total_boat_earnings = total_boat_earnings + (boat[2] * boat[3])
      return total_boat_earnings

#Testing to see if the get_total_boat_earnings function is working as intended
def test_2():
      assert get_total_boat_earnings() == 21520

get_total_weekly_employee_pay()
test_1()

get_total_boat_earnings()
test_2()