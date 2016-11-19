"""
Lu Base Conf for view

By leverage this class, we can add more feature in lucommon
framework base, user no need to care and regenerate code by
lucommon

More flexible to control and enhance lucommon
"""

class LuSQLConf(object):
    """
    value: the replacement value
    type: replacement type, control replace the key or value.
          eg: a = b, a is the key, b is the value, if type is 'value'
          will replace the b.
    mode: mode use to extend LuSQLConf, default is runtime, there are other
          value: fixed, changed.
          - runtime: execute in the backend, without change according to client input, eg: currentUser: self.request.user.username
          - fixed: never change, eg: version = 1
          - changed: execute in the runtime, also eval the value according to client input, like -1d, -2d, 3d
    """
    def __init__(self, value, type = 'value', mode = 'fixed'):
        self.value = value
        self.type = type
        self.mode = mode
        # key used for the mode = 'changed'
        self.key = None

class LuConf(object):
    # db for model to connect
    db = 'default'

    # for reversion
    enable_reversion_post = False
    enable_reversion_update = False
    enable_reversion_partial_update = False
    enable_reversion_delete = False

    # sql_injection_allow <list>: only allow 'select' sql injection
    # Actually, user can replace with more, lucommon will match
    # condition here and to see if allow or not
    sql_injection_allow = ['SELECT']

    # sql_injection_map <dict>: it will treat something like sql process
    # User call interface by post and add "{'lu_sql':'sql_func', 'lu_sql_param':'param1,param2'}",
    # lucommon will look up this map to find the SQL for 'sql_func', lucommon support
    # in this way, for better security
    #
    # Example like this:
    # sql_injection_map = {'sql_func':"select * from a"}
    sql_injection_map = {}

    # sql_param_delimiter <string>: default, ','
    sql_param_delimiter = ','

    # sql_injection_conf <dict>, will define configuration for search replacement,
    # coming soon, we will define useful global variable here
    sql_injection_conf = {'today': LuSQLConf('str(datetime.date.today())', mode='runtime'),
                          'currentUser': LuSQLConf('self.request.user.username', mode='runtime'),
                          '-(\d+)d': LuSQLConf('str(datetime.date.today() + datetime.timedelta(days = int(-%s)))', mode='changed'),
                          '\+(\d+)d': LuSQLConf('str(datetime.date.today() + datetime.timedelta(days = int(%s)))', mode='changed'),
                         }


    # For POST and UPDATE operation with multiple key/value pairs in body
    # Default, lucommon will join the value with the specified delimiter
    # and save the join value into database. User could disable this behavior
    # by the settings `enable_join_multiple_key_value_pair` and `join_multipe_key_value_pair_delimiter`
    #
    # Example: Post body like "student_name=Bob&student_name=Jane&student_name=Chris"
    # Lucommon save to db by set student_name=Bob,Jane,Chris
    enable_join_multiple_key_value_pair = True
    join_multiple_key_value_pair_delimiter = ','

    # Permission based on model level
    # for get and list, set the switch for it, it can be changed on the view conf
    # for update, create and delete, let the permission based on django permission,
    # so just need to set the conf if need to do the permission check or not
    enable_perm_get_check = False
    enable_perm_list_check = False
    enable_perm_update_check = False
    enable_perm_delete_check = True
    enable_perm_create_check = False


class DummyLuConf(object):pass


