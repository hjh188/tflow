from django.db import models
from lucommon.models import LuModel


class Project(LuModel):
    """
    Project model
    """
    name = models.CharField(max_length=255, null=False, unique=True)
    url = models.CharField(max_length=255, null=True)
    lead = models.CharField(max_length=255, null=True)
    key = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    status = models.CharField(max_length=255, null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    team_id = models.IntegerField(null=True)


class RequirementType(LuModel):
    """
    Requirement type model
    project <-> requirement type => 1-n
    """
    project_id = models.IntegerField(null=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)


class Component(LuModel):
    """
    Component model
    project <-> component => 1-n
    """
    project_id = models.IntegerField(null=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    url = models.CharField(max_length=255, null=True)
    lead = models.CharField(max_length=255, null=True)


