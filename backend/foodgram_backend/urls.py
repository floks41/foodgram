"""foodgram_backend URL Configuration."""

from django.contrib import admin
from django.urls import include, path
from djoser.views import UserViewSet

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/users/<int:id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('api/users/me/', UserViewSet.as_view({'get': 'me'})),
    path(
        'api/users/set_password/',
        UserViewSet.as_view({'post': 'set_password'}),
    ),
]
