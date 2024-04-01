from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import CustomGraphQLView
# from .schema import schema

urlpatterns = [
    # path("graphql/", csrf_exempt(CustomGraphQLView.as_view(graphiql=True, schema=schema)), name="graphql")
]
