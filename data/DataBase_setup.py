import datetime
import enum

from sqlalchemy import Column, Integer, String, Date, Float, Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Basic(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    def info(self):
        return ""

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id!r}){': ' + self.info() if self.info() != '' else ''}>"


class Gender(enum.Enum):
    male = 1
    female = 0


class Employee(Basic):
    __tablename__ = 'employees'

    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    middlename = Column(String(250), default=None)
    date_hired = Column(Date, default=datetime.datetime.today().date())
    date_fired = Column(Date, default=None)
    gender = Column(Enum(Gender), default=Gender.male)

    def getExperience_inDays(self):
        return (
            self.date_fired if self.date_fired is not None else datetime.datetime.today().date() - self.date_hired).days

    def getExperience_to_str(self):
        date = self.date_fired if self.date_fired is not None else datetime.datetime.today().date()
        exp = [date.year - self.date_hired.year, date.month - self.date_hired.month, date.day - self.date_hired.day]

        exp[1] += - 1 if exp[2] < 0 else 0
        exp[0] += -1 if exp[1] < 0 else 0
        exp[1] = (12 + exp[1]) % 12
        exp[2] = (date - datetime.date(date.year - (0 if 12 > date.month - 1 > 0 else 1), (12 + date.month - 1) % 12,
                                       self.date_hired.day)).days

        return f"{'years: ' + str(exp[0]) + ' ' if exp[0] > 0 else ''}{'months: ' + str(exp[1]) + ' ' if exp[1] > 0 or exp[0] > 0 else ''}{'days: ' + str(exp[2]) if exp[2] > 0 or exp[1] > 0 or exp[0] > 0 else 'None'}"

    def info(self):
        return f"Name: {self.firstname} {self.lastname}{' ' + self.middlename if self.middlename is not None and self.middlename != '' else ''}, {self.gender}, hired - {self.date_hired}{' - fired' + str(self.date_fired) if self.date_fired is not None else ''}, experience: {self.getExperience_to_str()}"


# если будет два родителя работать в одной компании, то просто делаем ещё одну запись (небольшое дублирование, но в пределах допустимого, на мой взгляд)
class Child(Basic):
    __tablename__ = 'children'

    id_employee = Column(Integer, nullable=False)
    birthday = Column(Date, default=datetime.datetime.today().date())

    def info(self):
        return f"parent id: {self.id_employee} - child age: {self.getAge()}"

    def getAge(self):
        now = datetime.datetime.today().date()
        age = [now.year - self.birthday.year, now.month - self.birthday.month, now.day - self.birthday.day]

        age[1] += - 1 if age[2] < 0 else 0
        age[0] += -1 if age[1] < 0 else 0

        return age[0]


class Rate(Basic):
    __tablename__ = 'rates of employees'

    id_employee = Column(Integer, nullable=False)
    rate = Column(Float, default=1.0)
    id_position = Column(Integer, nullable=False)

    def info(self):
        return f"employee id: {self.id_contract} - position id: {self.id_position} rate: {self.rate * 100}%"


class Position(Basic):
    __tablename__ = 'positions'

    descr = Column(String(250), default=None)
    staff_num = Column(Integer, default=1)
    wage = Column(Float, nullable=False)  # - стандартная ЗП

    def info(self):
        return f"staff_num: {self.type} -- standard wage: {self.wage}{'; description: ' + self.descr if self.descr is not None else ''}"


class PosContr(Basic):
    __tablename__ = 'positions to contracts'

    id_contract = Column(Integer, nullable=False)
    id_position = Column(Integer, nullable=False)

    def info(self):
        return f"contract id: {self.id_contract} -- position id: {self.id_position} "


class ContractTypes(enum.Enum):
    main = -1
    addition = 1


class Contract(Basic):
    __tablename__ = 'contracts'

    start_date = Column(Date, default=datetime.datetime.today().date())
    end_date = Column(Date, nullable=False)
    type = Column(Enum(ContractTypes), nullable=False, default=ContractTypes.addition)
    descr = Column(String(250), default=None)

    def info(self):
        return f"starts {self.start_date} - ends {self.end_date}{'; description: ' + self.descr if self.descr is not None else ''}"


class AwardEvent(Basic):
    __tablename__ = 'event of awarding'

    id_employee = Column(Integer, nullable=False)
    id_award = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    def info(self):
        return f"{self.date}: employee id {self.id_employee} -- award id {self.id_award}"


class AwardTypes(enum.Enum):
    penalty = -1
    award = 1


class Award(Basic):
    __tablename__ = 'awards & penalties'

    type = Column(Enum(AwardTypes), nullable=False, default=AwardTypes.award)
    descr = Column(String(250), default=None)
    cost = Column(Float, nullable=False)

    def info(self):
        return f"{self.type} sum:{self.sum}{'; description: ' + self.descr if self.descr is not None or self.descr != '' else ''}"


# if I'll get a free time in the future
# class Transaction(Basic):
#     __tablename__ = 'operations of transactions'
#
#     # id_transaction
#     # data_old
#     # data_new
#     # status
#     # last - bool


engine = create_engine('sqlite:///data/database.db')

Base.metadata.create_all(engine)
