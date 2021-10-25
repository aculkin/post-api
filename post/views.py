from post.serializers import PostSerializer

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post

class PostListViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin):
    """Manage the posts"""
    authentication_classes = (TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """create a new post"""
        serializer.save(author=self.request.user)
