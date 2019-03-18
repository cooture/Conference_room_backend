from django.urls import path, include

from .api_transfer import api

urlpatterns = [
    path('', include(api))
]