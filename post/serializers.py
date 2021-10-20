from django.contrib.auth.models import User
from rest_framework import serializers

from user.serializers import UserSerializer
from core.models import Post

class PostSerializer(serializers.ModelSerializer):
    """Serializer for post objects"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'date_posted', 'date_updated', 'author')
        read_only_fields = ('id', 'date_posted', 'date_updated')


class PostDetailSerializer(PostSerializer):
    """Serializer for a post details"""
    author = UserSerializer(read_only=True)