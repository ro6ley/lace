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

    def perform_create(self, serializer):
        """
        Save the POST data when creating a new template
        """
        # TODO: automatically create slug in case it is not provided
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Template.objects.all()
        username = self.request.user
        if username is None:
            queryset = queryset.filter(is_private=False)
        return queryset        


class TemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """ View to handle the viewing and updating of individual templates.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()

    def get_object(self):
        queryset = self.get_queryset()

        try:
            template = Template.objects.get(pk=self.kwargs['pk'])

            username = None
            user = None
            if self.request.user.is_authenticated:
                username = self.request.user.username
                user = User.objects.get(username=username)
            
            if template.is_private and template.owner == user:
                return template
            elif not template.is_private:
                return template
            else:
                raise PermissionDenied(detail="You're probably not allowed to see this", code=403)
        except Template.DoesNotExist:
            raise NotFound(detail="I really don't know what you're looking for, but I don't have it", code=404)
