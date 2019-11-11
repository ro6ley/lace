from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from .models import Template
from .permissions import IsOwner
from .serializers import TemplateSerializer


class TemplateCreateView(generics.ListCreateAPIView):
    """ View to handle the creation and listing of templates.
    """
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        """ Save the owner data when creating a new template
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """ View to handle the viewing and updating of individual templates.

    Public templates can be viewed by unauthenticated users.
    """
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]

    def retrieve(self, request, *args, **kwargs):
        template = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        serializer = TemplateSerializer(template)
        response = Response(serializer.data)

        user = None
        if self.request.user.is_authenticated:
            user = User.objects.get(username=self.request.user.username)
        
        if template.is_private and template.owner == user:
            return response
        elif not template.is_private:
            return response
        else:
            self.check_object_permissions(self.request, template)
            return response
