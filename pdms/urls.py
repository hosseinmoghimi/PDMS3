
from django.contrib import admin
from django.urls import path,include,re_path

from .settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('web/', include('web.urls')),
    path('core/', include('core.urls')),
    path('accounts/', include('authentication.urls')),
    path('', include('web2.urls')),
    path('utility/', include('utility.urls')),
    
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]
