from django.urls import path
from management.views import web

urlpatterns = [
    path('test/', web.test),
    path('isonline/', web.is_online),
    path('statictest/', web.static_test),
]
