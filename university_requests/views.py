from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from graphene_django.views import GraphQLView


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
