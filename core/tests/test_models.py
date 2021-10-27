from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

def sample_post(user, title='Test title', content='Test content', group=None):
    """Create a sample post"""
    return models.Post.objects.create(user=user, title=title, content=content, group=group)

def sample_group(name='Test group'):
    """Create a sample group"""
    return models.Group.objects.create(name=name, description='Test description')


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_post_str(self):
        """Test the string representation of a post"""
        post = models.Post.objects.create(
            author=sample_user(),
            title='Test title',
            content='Test content'
        )

        self.assertEqual(str(post), post.title)

    def test_create_post_successful(self):
        """Test creating a post with required parameters is successful"""
        title = 'Test title'
        content = 'Test content'
        post = models.Post.objects.create(
            author=sample_user(),
            title=title,
            content=content
        )
        self.assertEqual(post.title, title)
        self.assertEqual(post.content, content)
    #test create post unsuccessful
    #test delete post
    #test update post successful
    #test update post unsuccessful

    def test_group_string(self):
        """Test the string representation of a group"""
        group = models.Group.objects.create(
            name='Test group name',
            slug='test_group-slug',
            description='Test group description',
        )

        self.assertEqual(str(group), group.name)
    #test create post successful
    #test create post unsuccessful
    #test delete post
    #test update post successful
    #test update post unsuccessful


    
        
