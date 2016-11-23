from django.contrib import admin
from lucommon.reversion_compare_admin import CompareVersionAdmin
from reversion import revisions
from lucommon import admin as luadmin

from tproject.models import (
    Component,
    Project,
    RequirementType,
)

from tproject.confs import (
    ComponentConf,
    ProjectConf,
    RequirementTypeConf,
)

"""
Register models for django admin
"""


class ComponentAdmin(luadmin.MultiDBModelAdmin, CompareVersionAdmin):
    """
    Component admin part
    """
    using = ComponentConf.db
    # Update `search_fields` for the which field took for search
    search_fields = ['id', 'project_id', 'name', 'description', 'url', 'lead']
    # Update `list_display` to show which field display in the admin page
    list_display = ['id', 'project_id', 'name', 'description', 'url', 'lead']


class ProjectAdmin(luadmin.MultiDBModelAdmin, CompareVersionAdmin):
    """
    Project admin part
    """
    using = ProjectConf.db
    # Update `search_fields` for the which field took for search
    search_fields = ['id', 'name', 'url', 'lead', 'description', 'status', 'create_at', 'update_at', 'team_id']
    # Update `list_display` to show which field display in the admin page
    list_display = ['id', 'name', 'url', 'lead', 'description', 'status', 'create_at', 'update_at', 'team_id']


class RequirementTypeAdmin(luadmin.MultiDBModelAdmin, CompareVersionAdmin):
    """
    RequirementType admin part
    """
    using = RequirementTypeConf.db
    # Update `search_fields` for the which field took for search
    search_fields = ['id', 'project_id', 'name', 'description']
    # Update `list_display` to show which field display in the admin page
    list_display = ['id', 'project_id', 'name', 'description']



Component._meta.using = ComponentConf.db

revisions.register(Component)

admin.site.register(Component, ComponentAdmin)
Project._meta.using = ProjectConf.db

revisions.register(Project)

admin.site.register(Project, ProjectAdmin)
RequirementType._meta.using = RequirementTypeConf.db

revisions.register(RequirementType)

admin.site.register(RequirementType, RequirementTypeAdmin)


