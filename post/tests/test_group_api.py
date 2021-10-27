from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post, Group
from post.serializers import GroupSerializer

GROUPS_URL = reverse('post:group-list')
# GROUP_POSTS_URL = reverse('post:group-posts')

# def group_detail_url(group_id):
#     """Return recipe detail URL"""
#     return reverse('post:group-posts', args=[group_id])


def create_sample_user(email='user2@email.com', password='testpass', **params):
    """Create a sample user for test purposes"""
    return get_user_model().objects.create_user(email, password, **params)

def create_sample_post(user, **params):
    """Create a sample post for test purposes"""
    defaults = {
        'title': 'Sample post',
        'content': "Content for a sample post",
    }
    defaults.update(params)
    return Post.objects.create(author=user, **defaults)

def create_sample_group(**params):
    """Create a sample group for test purposes"""
    defaults = {
        'name': 'Sample group',
        'slug': 'sample-group',
        'description': 'Sample group description',
    }
    defaults.update(params)
    return Group.objects.create(**defaults)


class PublicGroupApiTests(TestCase):
    """Test the posts API (public)"""

    def setup(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(GROUPS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateGroupApiTests(TestCase):
    """Test authenticated recipe API access"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_list_all_groups(self):
        """Test retrieving a list of groups"""
        create_sample_group(slug='slug1')
        create_sample_group(slug='slug2')

        res = self.client.get(GROUPS_URL)

        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_group(self):
        """Test creating a group"""
        payload = {
            'name': 'Test group',
            'slug': 'test-group',
            'description': 'Test group description'
        }
        res = self.client.post(GROUPS_URL, payload)

        exists = Group.objects.filter(
            slug=payload['slug']
        ).exists()
        self.assertTrue(exists)

    def test_create_group_invalid(self):
        """Test creating a group with invalid payload"""
        payload = {
            'name': '',
            'slug': '',
            'description': ''
        }
        res = self.client.post(GROUPS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_delete_group(self):
    #     """Test deleting a group removes the group"""
    #     group1 = create_sample_group(slug='slug1')
    #     create_sample_group(slug='slug2')

    #     res = self.client.delete(group_detail_url(group1.id))
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     groups = Group.objects.all()
    #     serializer = GroupSerializer(groups, many=True)
    #     self.assertEqual(len(serializer.data), 1)

    # def test_retrieve_group_with_posts(self):
    #     """Test retrieving a group's posts"""
    #     print(group_detail_url(1))
    #     group = create_sample_group()
    #     create_sample_post(user=self.user, group=group)
    #     create_sample_post(user=self.user, group=group)

    #     res = self.client.get(group_detail_url(group.id))

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data.posts), 2)

    

