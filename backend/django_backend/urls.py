"""
URL configuration for django_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from property import urls as property_urls
from django.conf import settings
from django.conf.urls.static import static
from useraccounts import urls as user_urls
from inquiries import urls as inquiries_urls
from chat import urls as chat_urls
from my_stripe import urls as stripe_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(property_urls)),
    path('api/auth/', include(user_urls)),
    path('accounts/', include('allauth.urls')),
    path('api/inquiries/', include(inquiries_urls)),
    path('oauth2callback/', include('allauth.urls')),  # This handles the Google OAuth2 callback
    path('api/chat/', include(chat_urls)),
    path('api/stripe/', include(stripe_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
