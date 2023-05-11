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
    exp[2] = (date2 - datetime.date(date2.year - (0 if 12 > date2.month - 1 > 0 else 1),
                                    (12 + date2.month - 2) % 12 + 1,
                                    date1.day)).days
    # print(exp)
    return exp


def generate_employee_list(employees):
    if len(employees) > 0:
        return "Список сотрудников:\n" + "\n".join([f"{e.firstname} {e.lastname} {'' if e.middlename is None else e.middlename}\n\t\t- Стаж - {e.getExperience_to_str()}\n\t\t- Статус - {'нанят' if e.date_fired is None else 'уволен'}" for e in employees])
    else:
        return "Пусто."


def generate_award_list(awards):
    if len(awards) > 0:
        text = "Список поощрений:\n" + "\n".join(
            [f"{a.name} - {a.cost} р." for a in sorted(list(filter(lambda x: x.type.name == 'award', awards)), key=lambda x: x.name)])
        text += "\n\nСписок штрафов:\n" + "\n".join(
            [f"{a.name} - {a.cost} р." for a in sorted(list(filter(lambda x: x.type.name == 'penalty', awards)), key=lambda x: x.name)])
        return text
    else:
        return "Пусто."


def generate_contract_list(contracts):
    if len(contracts) > 0:
        return "Список контрактов:\n" + "\n".join(
            [f"{c.name} - {'основной' if c.type.name == 'main' else 'дополнительный'}: с {date_to_str(c.start_date)} до {date_to_str(c.end_date)}" for c in
             list(filter(lambda x: x.get_status(), contracts))])
    else:
        return "Пусто."


def date_to_str(date):
    return str(date.year) + "." + str(date.month) + "." + str(date.day)

def date_rules():
    return "Формат даты ДД.ММ.ГГГГ. Также она не должна быть больше сегодняшней.\n"
