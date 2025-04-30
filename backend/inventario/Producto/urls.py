from django.urls import path
from .views import *

urlpatterns = [
    path('producto', Clase1.as_view()),
    path('producto/', Clase2.as_view())
]