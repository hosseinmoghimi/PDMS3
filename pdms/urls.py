
from django.contrib import admin
from django.urls import path,include

from .settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('web/', include('web.urls')),
    path('core/', include('core.urls')),
    path('accounts/', include('authentication.urls')),
    path('', include('web2.urls')),
    path('utility/', include('utility.urls')),
    
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]
