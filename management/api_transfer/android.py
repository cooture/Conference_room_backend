from django.urls import path
from management.views import android


urlpatterns = [
    path('test/', android.test)
]