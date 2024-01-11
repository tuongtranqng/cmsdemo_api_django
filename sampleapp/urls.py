from django.urls import path, include

from rest_framework.authtoken import views


urlpatterns = [
    path('token-auth/', views.obtain_auth_token),
    path('', include('sampleapp.api.v1.urls')),
]
