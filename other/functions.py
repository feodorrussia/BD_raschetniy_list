import datetime


def check_date(date):
    date = date.strip().split()
    if len(date) == 3:
        if 0 < date[0] <= 31 and 0 < date[1] <= 12 and 0 < date[2] <= datetime.date.today().year:
            if date[2] < datetime.date.today().year:
                return True
            elif date[2] == datetime.date.today().year:
                if date[1] < datetime.date.today().month:
                    return True
                elif date[1] == datetime.date.today().month:
                    if date[0] <= datetime.date.today().day:
                        return True
    return False


def generate_employee_list(employees):
    if len(employees) > 0:
        return "Список сотрудников:\n" + "\n".join([e.firstname + " " + e.lastname if e.middlename is None
                                                    else e.firstname + " " + e.lastname + " " + e.middlename for e in
                                                    employees])
    else:
        return "Пусто."


def generate_award_list(awards):
    if len(awards) > 0:
        return "Список поощрений/штрафов:\n" + "\n".join(
            [a.name + " - " + a.type + " = " + a.cost for a in awards])
    else:
        return "Пусто."


def date_rules():
    return "Формат даты ДД.ММ.ГГГГ. Также она не должна быть больше сегодняшней.\n"
