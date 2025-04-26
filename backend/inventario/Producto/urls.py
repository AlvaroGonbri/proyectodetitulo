from django.urls import path
from .views import *

urlpatterns = [
    path('producto', Clase1.as_view()),
    path('producto/<int:id>', Clase2.as_view())
]