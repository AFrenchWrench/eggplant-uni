from django.urls import path
from .views import (
    UserLoginView,
    UserLogoutView,
    ChangePasswordRequestView,
    ChangePasswordActionView,
)

urlpatterns = [
    # Authentication
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('change-password-request/', ChangePasswordRequestView.as_view(), name='change-password-request'),
    path('change-password-action/', ChangePasswordActionView.as_view(), name='change-password-action'),


]
