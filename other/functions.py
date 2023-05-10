def check_date(date):
    return True


def generate_employee_list(employees):
    print(employees)
    if len(employees) > 0:
        return "Список сотрудников:\n" + "\n".join([e.firstname + " " + e.lastname if e.middlename is None
                                                else e.firstname + " " + e.lastname + " " + e.middlename for e in
                                                employees])
    else:
        return "Пусто."
def generate_award_list(awards):
    print(awards)
    if len(awards) > 0:
        return "Список поощрений/штрафов:\n" + "\n".join([a.descr + " - " + a.type + " = " + a.cost for a in awards])
    else:
        return "Пусто."
