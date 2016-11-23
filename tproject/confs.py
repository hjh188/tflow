"""
App setting for tproject

We suggest you put all the app related settings here,
it's easy to maintain and good catch.

"""

from lucommon.confs import (
    LuConf,
    LuSQLConf,
)


class ComponentConf(LuConf):
    """
    It's a good practice to write Component
    related setting here.
    """
    # In a real world, you mostly need to change db here
    db = 'default'

    # Generate the default SEARCH for the model by lu SQL injection
    sql_injection_map = {'get_component':'SELECT * FROM tproject_component WHERE LU_SEARCH_CONDITION'}


class ProjectConf(LuConf):
    """
    It's a good practice to write Project
    related setting here.
    """
    # In a real world, you mostly need to change db here
    db = 'default'

    # Generate the default SEARCH for the model by lu SQL injection
    sql_injection_map = {'get_project':'SELECT * FROM tproject_project WHERE LU_SEARCH_CONDITION'}


class RequirementTypeConf(LuConf):
    """
    It's a good practice to write RequirementType
    related setting here.
    """
    # In a real world, you mostly need to change db here
    db = 'default'

    # Generate the default SEARCH for the model by lu SQL injection
    sql_injection_map = {'get_requirementtype':'SELECT * FROM tproject_requirementtype WHERE LU_SEARCH_CONDITION'}


