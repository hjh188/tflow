"""
App setting for tuser

We suggest you put all the app related settings here,
it's easy to maintain and good catch.

"""

from lucommon.confs import LuConf


class UserConf(LuConf):
    """
    It's a good practice to write User
    related setting here.
    """
    # In a real world, you mostly need to change db here
    db = 'default'

    sql_injection_allow = ['SELECT','UPDATE']
    sql_injection_map = {'get_menu':'select sidebar_menu_top, sidebar_menu_bottom from tuser_user where username = %s',
                         'set_menu':"""update tuser_user set sidebar_menu_top = %s, sidebar_menu_bottom = %s where username = %s"""}

