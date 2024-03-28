from django.contrib import admin
from django.urls import include
from django.urls import path

from users import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('requests/', include('requests.urls')),
    path('admin_dash/', include('admin_dash.urls')),
    path('', include('university.urls')),
]
