import datetime


def check_date(date):
    try:
        date = list(map(int, date.strip().split(".")))
    except Exception as e:
        return False
    date_now = datetime.date.today()
    if len(date) == 3:
        if 0 < date[0] <= 31 and 0 < date[1] <= 12 and 0 < date[2] <= date_now.year:
            if date[2] < date_now.year:
                return True
            elif date[2] == date_now.year:
                if date[1] < date_now.month:
                    return True
                elif date[1] == date_now.month:
                    if date[0] <= date_now.day:
                        return True
    return False

def dif_date(date1, date2):
    exp = [date2.year - date1.year, date2.month - date1.month, date2.day - date1.day]

    exp[1] += - 1 if exp[2] < 0 else 0
    exp[0] += -1 if exp[1] < 0 else 0
    exp[1] = (12 + exp[1]) % 12
    exp[2] = (date2 - datetime.date(date2.year - (0 if 12 > date2.month - 1 > 0 else 1), (12 + date2.month - 2) % 12 + 1,
                                   date1.day)).days
    # print(exp)
    return exp


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
