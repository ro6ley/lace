from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Template
from .permissions import IsOwner
from .serializers import TemplateSerializer


class TemplateCreateView(generics.ListCreateAPIView):
    """ View to handle the creation and listing of templates.
    """
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """ Save the owner data when creating a new template
        """
        serializer.save(owner=self.request.user)


class TemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """ View to handle the viewing and updating of individual templates.

    Public templates can be viewed by unauthenticated users.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()

    def get_object(self):
        queryset = self.get_queryset()

        try:
            template = Template.objects.get(pk=self.kwargs['pk'])

            user = None
            if self.request.user.is_authenticated:
                user = User.objects.get(username=self.request.user.username)
            
            if template.is_private and template.owner == user:
                return template
            elif not template.is_private:
                return template
            else:
                raise PermissionDenied(detail="You're probably not allowed to see this", code=403)
        except Template.DoesNotExist:
            raise NotFound(detail="I really don't know what you're looking for, but I don't have it", code=404)
