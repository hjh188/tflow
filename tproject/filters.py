import django_filters

from tproject.models import (
    Component,
    Project,
    RequirementType,
)

"""
Query filter

On how to set filter class, you can refer to
Django filter for detail management.
"""

class ComponentFilter(django_filters.FilterSet):
    """
    Component filter
    """
    min_project_id = django_filters.NumberFilter(name='project_id', lookup_type='gte')
    max_project_id = django_filters.NumberFilter(name='project_id', lookup_type='lte')

    class Meta:
        model = Component
        fields = ['id', 'project_id', 'max_project_id', 'min_project_id', 'name', 'description', 'url', 'lead']


class ProjectFilter(django_filters.FilterSet):
    """
    Project filter
    """
    min_update_at = django_filters.DateTimeFilter(name='update_at', lookup_type='gte')
    min_team_id = django_filters.NumberFilter(name='team_id', lookup_type='gte')
    max_team_id = django_filters.NumberFilter(name='team_id', lookup_type='lte')
    min_create_at = django_filters.DateTimeFilter(name='create_at', lookup_type='gte')
    max_create_at = django_filters.DateTimeFilter(name='create_at', lookup_type='lte')
    max_update_at = django_filters.DateTimeFilter(name='update_at', lookup_type='lte')

    class Meta:
        model = Project
        fields = ['id', 'name', 'url', 'lead', 'description', 'status', 'create_at', 'max_create_at', 'min_create_at', 'update_at', 'max_update_at', 'min_update_at', 'team_id', 'max_team_id', 'min_team_id']


class RequirementTypeFilter(django_filters.FilterSet):
    """
    RequirementType filter
    """
    min_project_id = django_filters.NumberFilter(name='project_id', lookup_type='gte')
    max_project_id = django_filters.NumberFilter(name='project_id', lookup_type='lte')

    class Meta:
        model = RequirementType
        fields = ['id', 'project_id', 'max_project_id', 'min_project_id', 'name', 'description']


