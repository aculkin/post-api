from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'), # Create new user
    path('token/', views.CreateTokenView.as_view(), name='token'), # Login with username and password, get 
    path('me/', views.ManageUserView.as_view(), name='me'),
]