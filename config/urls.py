from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie


class CustomGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def format_error(error):
        return super(CustomGraphQLView, CustomGraphQLView).format_error(error)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return csrf_exempt(view)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('university_requests/', include('university_requests.urls')),
    path('university/', include('university.urls')),
    path('admin_dash/', include('admin_dash.urls')),
    path('', include('university.urls')),
    path("graphql/", jwt_cookie(csrf_exempt(CustomGraphQLView.as_view(graphiql=True))), name="graphql")

]
