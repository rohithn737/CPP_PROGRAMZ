from django.contrib import admin
from django.urls import path,include

from django.conf import settings

from django.conf.urls.static import static #TO IMPORT THE STATIC FILES

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crm.urls')), #To connect app urls to main project , . --> to imply we are in the same directory
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
#This will help in uploading our own media files