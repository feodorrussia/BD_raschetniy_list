from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from DataBase_setup import *

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# WRITE
employee = Employee(firstname=input("firstname: "), lastname=input("lastname: "), middlename=input("middlename: "), gender=Gender.female, date_hired=datetime.date(2002, 2, 20))
session.add(employee)
session.commit()

print(employee)

# READ
print(session.query(Employee).all())

# UPDATE
for_edit = session.query(Employee).filter_by(id=1).all()
for edited in for_edit:
    gen = input(f"new gender for {edited.lastname}(now: {edited.gender}): ")
    edited.gender = Gender.male if gen.lower() == "male" or gen.lower() == "m" else Gender.female
    session.add(edited)
    session.commit()

# DELETE
# employeesToDelete = session.query(Employee).filter_by(gender=Gender.male).all()
# for employeeToDelete in employeesToDelete:
#     session.delete(employeeToDelete)
#     session.commit()

print(session.query(Employee).all())
