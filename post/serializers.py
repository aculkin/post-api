from rest_framework import serializers

from user.serializers import UserSerializer
from core.models import Post, Group

class PostSerializer(serializers.ModelSerializer):
    """Serializer for post objects"""
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'date_posted', 'date_updated', 'author', 'group')
        read_only_fields = ('id', 'date_posted', 'date_updated', 'author')


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for listing group objects"""
    class Meta:
        model = Group
        fields = ('id', 'name', 'slug', 'description', 'listed', 'date_created')
        read_only_fields = ('id', 'date_created')
