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


