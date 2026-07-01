from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def admin_logout_get(request):
    auth_logout(request)
    return redirect('/admin/login/')

urlpatterns = [
    path('admin/do-logout/', admin_logout_get, name='admin_do_logout'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
