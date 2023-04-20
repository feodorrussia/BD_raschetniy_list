
def daysToDate_str(timedelta):
    date = [timedelta/365, timedelta%365/30, timedelta%365%30/7]
    return f""