from django.urls import path
from graphql_jwt.decorators import jwt_cookie
from .views import (
    UserLoginView,
    UserLogoutView,
    ChangePasswordRequestView,
    ChangePasswordActionView,
    CustomGraphQLView,
)
from django.views.decorators.csrf import csrf_exempt
from .schema import schema

app_name = 'users'
urlpatterns = [
    # Authentication
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('change-password-request/', ChangePasswordRequestView.as_view(), name='change-password-request'),
    path('change-password-action/', ChangePasswordActionView.as_view(), name='change-password-action'),
    path("graphql/", jwt_cookie(csrf_exempt(CustomGraphQLView.as_view(graphiql=True, schema=schema))), name="graphql")

]
