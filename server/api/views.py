from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import Template
from .permissions import IsOwner
from .serializers import TemplateSerializer


class TemplateCreateView(generics.ListCreateAPIView):
    """ View to handle the creation and listing of templates.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()

    def perform_create(self, serializer):
        """
        Save the POST data when creating a new template
        """
        # TODO: automatically create slug in case it is not provided
        serializer.save(owner=self.request.user)


class TemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()

