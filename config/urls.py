from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('student/', include('student_dash.urls')),
    path('professor/', include('professor_dash.urls')),
    path('assistant/', include('assistant_dash.urls')),
    path('admin_dash/', include('admin_dash.urls')),
    path('', include('university.urls')),
]
