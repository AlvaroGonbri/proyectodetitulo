from django.urls import path
from .views import TecnicoListAPIView  # Asegúrate de tener esta vista en views.py

urlpatterns = [
    # Endpoint para listar técnicos
    # GET /rest/v1/tecnico/  - Lista todos los técnicos
    path('', TecnicoListAPIView.as_view(), name='tecnicos-list'),
]
