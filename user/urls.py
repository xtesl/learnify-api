from .views import CreateUser, Login, ConfirmUser
from django.urls import path

urlpatterns = [
    path('auth/register/',CreateUser.as_view(), name='register'),
    path('auth/login/', Login.as_view(), name='login'),
    path('auth/confirm-user/', ConfirmUser.as_view(), name='confirm-user'),
 ]