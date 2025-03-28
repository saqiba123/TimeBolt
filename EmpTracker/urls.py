from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
# api schema
schema_view = get_schema_view(openapi.Info(title="Task",default_version="v1",description="Api documentation",
                                           terms_of_service="https:/www.example.com/terms", contact=openapi.Contact(email="support@example.com"),license=openapi.License(name="MIT License")),
                              public=True,
                              permission_classes=(permissions.AllowAny,))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    # path("accounts/", include("django.contrib.auth.urls")),
     # Allauth for social login and registration
  
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    # Django's built-in auth for basic login/logout
    # path('api/', include('tracker.urls')),
    path("swagger/",schema_view.with_ui("swagger",cache_timeout=0), name="swagger-api-doc"),
]
