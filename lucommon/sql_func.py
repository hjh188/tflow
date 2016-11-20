import datetime


"""
SQL Func will define small utils function used for the LuSQLConf
This part of function usually will get the value runtime
"""

def get_today():
    """
    Get date by today
    """
    return str(datetime.date.today())

def get_current_user(view):
    """
    Get current login user's username
    """
    return view.request.user.username

def get_day_before(day):
    """
    Get specified day before today
    """
    return str(datetime.date.today() + datetime.timedelta(days = int(-day)))

def get_day_after(day):
    """
    Get specified day after today
    """
    return str(datetime.date.today() + datetime.timedelta(days = int(day)))


