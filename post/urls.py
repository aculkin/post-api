from django.urls import path, include
from rest_framework.routers import DefaultRouter

from post import views

router = DefaultRouter()
router.register('posts', views.PostListViewset)
router.register('groups', views.GroupListViewset)

app_name = 'post'

urlpatterns = [
    path('groups/<int:group_id>/posts', views.GroupPostListViewset.as_view({'get': 'list'}), name='group-posts'),
    path('', include(router.urls)),
]

