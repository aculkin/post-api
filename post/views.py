from post.serializers import PostSerializer, GroupSerializer

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post, Group

class PostListViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin):
    """Manage the posts"""
    authentication_classes = (TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """create a new post"""
        serializer.save(author=self.request.user)

class GroupListViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """Manage the groups"""
    authentication_classes = (TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupPostListViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Get all the posts in a specific group"""
    authentication_classes = (TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    serializer_class=PostSerializer

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(group_id=self.kwargs['group_id'])