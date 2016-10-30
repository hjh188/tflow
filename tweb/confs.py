"""
App setting for tweb

We suggest you put all the app related settings here,
it's easy to maintain and good catch.

"""

from lucommon.confs import LuConf


class WebSourceConf(LuConf):
    """
    It's a good practice to write WebSource
    related setting here.
    """
    # In a real world, you mostly need to change db here
    db = 'default'

    # Static File Prefix
    static_file_endpoint = 'http://127.0.0.1:8080/web/'

