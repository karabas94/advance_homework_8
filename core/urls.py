"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from blog.views import RegisterFormView, login_request, logout_request, UpdateProfile, UserProfile, PublicProfile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='/blog/post/', permanent=True)),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/register/', RegisterFormView.as_view(), name='register'),
    path('accounts/login/', login_request, name='login'),
    path('accounts/update_profile/', UpdateProfile.as_view(), name='update_profile'),

    path('accounts/', UserProfile.as_view(), name='profile'),
    path('accounts/<int:pk>/', PublicProfile.as_view(), name='user_profile'),

    path('logout', logout_request, name="logout"),


]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
