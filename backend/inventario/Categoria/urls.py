from django.urls import path
from .views import *

urlpatterns = [
    path('categoria', Clase1.as_view())
]