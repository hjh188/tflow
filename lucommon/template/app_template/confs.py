"""
App setting for {{ app_name }}

We suggest you put all the app related settings here,
it's easy to maintain and good catch.

"""

from lucommon.confs import (
    LuConf,
    LuSQLConf,
)

{% for model_name in model_names %}
class {{ model_name }}Conf(LuConf):
    """
    It's a good practice to write {{ model_name }}
    related setting here.
    """
    # In a real world, you mostly need to change db here
    db = 'default'

{% endfor %}
