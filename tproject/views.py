from tproject.serializers import (
    ComponentSerializer,
    ProjectSerializer,
    RequirementTypeSerializer,
)

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

from tproject.filters import (
    ComponentFilter,
    ProjectFilter,
    RequirementTypeFilter,
)

from lucommon import (
    viewsets,
)

from lucommon.response import LuResponse
from lucommon.logger import lu_logger

"""
Write less, do more

* By viewsets.ModelViewSet, we can write restful API easily.
Usually, it's necessary to write CRUD operation in the viewset,
it's enough for common scenario. However, we can override
these functions(`list`, `create`, `retrieve`, `update`,
`partial_update`, `destroy`) for more detail control.

Example for HTTP GET:

def retrieve(self, request, *args, **kwargs):
    #`args` indicate the path without ?P(item) in urls route
    #`kwargs` indicate the param in ?P(item) in urls route
    do_something_before()
    response = super(viewsets.ModelViewSet, self).retrieve(request, *args, **kwargs)
    do_something_after()
    return response

* API docs(http://django-rest-swagger.readthedocs.org/en/latest/yaml.html)
Use the YAML Docstring for API docs

"""


class ComponentViewSet(viewsets.LuModelViewSet):
    """
    ViewSet for Component operation
    """
    # Query set
    queryset = Component.objects.using(ComponentConf.db).all()

    # Serializer class
    serializer_class = ComponentSerializer

    # Filter class
    filter_class = ComponentFilter

    # Conf class
    conf = ComponentConf

    # APP name
    app = "tproject"

    # Model name
    model = "Component"

    def perform_create(self, serializer):
        """
        Keep this function for POST db select
        """
        serializer.save(using=ComponentConf.db)

    def get_queryset(self):
        # Add whatever to filter the response if you want
        return Component.objects.using(ComponentConf.db).all()


    def list(self, request, *args, **kwargs):
        """
        HTTP GET list entry
        """
        return super(ComponentViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        HTTP GET item entry
        """
        return super(ComponentViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        HTTP POST item entry
        """
        return super(ComponentViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        HTTP PUT item entry
        """
        return super(ComponentViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        HTTP PATCH item entry
        """
        return super(ComponentViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        HTTP DELETE item entry
        """
        return super(ComponentViewSet, self).destroy(request, *args, **kwargs)

    def history(self, request, *args, **kwargs):
        """
        Object History
        """
        return super(ComponentViewSet, self).history(request, *args, **kwargs)


class ProjectViewSet(viewsets.LuModelViewSet):
    """
    ViewSet for Project operation
    """
    # Query set
    queryset = Project.objects.using(ProjectConf.db).all()

    # Serializer class
    serializer_class = ProjectSerializer

    # Filter class
    filter_class = ProjectFilter

    # Conf class
    conf = ProjectConf

    # APP name
    app = "tproject"

    # Model name
    model = "Project"

    def perform_create(self, serializer):
        """
        Keep this function for POST db select
        """
        serializer.save(using=ProjectConf.db)

    def get_queryset(self):
        # Add whatever to filter the response if you want
        return Project.objects.using(ProjectConf.db).all()


    def list(self, request, *args, **kwargs):
        """
        HTTP GET list entry
        """
        return super(ProjectViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        HTTP GET item entry
        """
        return super(ProjectViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        HTTP POST item entry
        """
        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        HTTP PUT item entry
        """
        return super(ProjectViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        HTTP PATCH item entry
        """
        return super(ProjectViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        HTTP DELETE item entry
        """
        return super(ProjectViewSet, self).destroy(request, *args, **kwargs)

    def history(self, request, *args, **kwargs):
        """
        Object History
        """
        return super(ProjectViewSet, self).history(request, *args, **kwargs)


class RequirementTypeViewSet(viewsets.LuModelViewSet):
    """
    ViewSet for RequirementType operation
    """
    # Query set
    queryset = RequirementType.objects.using(RequirementTypeConf.db).all()

    # Serializer class
    serializer_class = RequirementTypeSerializer

    # Filter class
    filter_class = RequirementTypeFilter

    # Conf class
    conf = RequirementTypeConf

    # APP name
    app = "tproject"

    # Model name
    model = "RequirementType"

    def perform_create(self, serializer):
        """
        Keep this function for POST db select
        """
        serializer.save(using=RequirementTypeConf.db)

    def get_queryset(self):
        # Add whatever to filter the response if you want
        return RequirementType.objects.using(RequirementTypeConf.db).all()


    def list(self, request, *args, **kwargs):
        """
        HTTP GET list entry
        """
        return super(RequirementTypeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        HTTP GET item entry
        """
        return super(RequirementTypeViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        HTTP POST item entry
        """
        return super(RequirementTypeViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        HTTP PUT item entry
        """
        return super(RequirementTypeViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        HTTP PATCH item entry
        """
        return super(RequirementTypeViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        HTTP DELETE item entry
        """
        return super(RequirementTypeViewSet, self).destroy(request, *args, **kwargs)

    def history(self, request, *args, **kwargs):
        """
        Object History
        """
        return super(RequirementTypeViewSet, self).history(request, *args, **kwargs)


