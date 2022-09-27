from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.upload, name="upload")
              ] + static(settings.MEDIA_URL_OUTPUT, document_root=settings.MEDIA_ROOT_OUTPUT)
