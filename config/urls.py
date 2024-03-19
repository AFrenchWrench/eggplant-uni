from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from config import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('users/', include('users.urls')),
                  path('admin_dash/', include('admin_dash.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
