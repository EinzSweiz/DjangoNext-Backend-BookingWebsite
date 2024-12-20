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
from useraccounts.api import google_login_callback, validate_google_token
from my_stripe import urls as stripe_urls
from drf_yasg.views import  get_schema_view
from drf_yasg import openapi
from reviews import urls as reviews_urls
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title='Diploma Road API',
        default_version='v1',
        description='API Documenation for Diploma Road',
        contact=openapi.Contact(email='riad.sultanov.1999@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(AllowAny,)
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(property_urls)),
    path('api/auth/', include(user_urls)),
    path('api/auth2/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('allauth.urls')),
    path('api/inquiries/', include(inquiries_urls)),
    path('api/chat/', include(chat_urls)),
    path('callback/', google_login_callback, name='callback'),
    path('api/review/', include(reviews_urls)),
    path('api/google/validate_token', validate_google_token, name='validate_token_google'),
    path('api/stripe/', include(stripe_urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
