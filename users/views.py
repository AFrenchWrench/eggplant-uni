from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql import GraphQLError

from .schema import schema


class CustomGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def format_error(error):
        formatted_error = super(CustomGraphQLView, CustomGraphQLView).format_error(error)
        if isinstance(error, GraphQLError):
            formatted_error = {'message': str(error)}
        return formatted_error

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return csrf_exempt(view)


# POST
class UserLoginView(View):
    pass


# POST
class UserLogoutView(View):
    pass


# POST
class ChangePasswordRequestView(View):
    pass


# POST
class ChangePasswordActionView(View):
    pass
