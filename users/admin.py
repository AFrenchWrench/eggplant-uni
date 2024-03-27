from django.apps import apps
from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    if model_name == 'Group':
        pass
    admin.site.register(model)
