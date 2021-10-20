from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post
from post.serializers import PostSerializer

POSTS_URL = reverse('post:post-list')

def create_sample_user(email='user2@email.com', password='testpass', **params):
    """Create a sample user for test purposes"""
    return get_user_model().objects.create_user(email, password, **params)

def create_sample_post(**params):
    """Create a sample post for test purposes"""
    defaults = {
        'title': 'Sample post',
        'content': "Content for a sample post",
    }
    defaults.update(params)
    return Post.objects.create(**defaults)




class PublicPostApiTests(TestCase):
    """Test the posts API (public)"""

    def setup(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatePostApiTests(TestCase):
    """Test authenticated recipe API access"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_all_posts(self):
        """Test retrieving a list of posts"""

        user2 = create_sample_user()
        post1 = create_sample_post(author=self.user)
        post2 = create_sample_post(author=user2)

        res = self.client.get(POSTS_URL)

        posts = Post.objects.all().order_by('-id')
        listSerializer = PostSerializer(posts, many=True)
        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), len(listSerializer.data))
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_create_post(self):
        """Test that a user can create a post and it is associated with the authenticated user"""
        res = self.client.post(POSTS_URL, {
            'title': 'my post',
            'content': 'my post content'
        })

        createdPost = Post.objects.get(id=res.data['id'])
        self.assertEqual(createdPost.author.id, self.user.id)