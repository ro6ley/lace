from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer


class SnippetViewSet(ModelViewSet):
    """ View to handle the viewing and updating of individual templates.

    Public templates can be viewed by unauthenticated users.
    """
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        if user.id:
            return Snippet.objects.filter(Q(is_private=False) | Q(owner=user))
        else:
            return Snippet.objects.filter(is_private=False)

    # Set user as owner of a Snippet
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
