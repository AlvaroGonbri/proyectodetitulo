from django.urls import path, include
from .views import ProductoListCreateAPIView, ProductoSearchAPIView, ProductoUpdateAPIView

urlpatterns = [
    # Endpoint para listar y crear productos
    # GET /rest/v1/producto/  - Lista todos los productos
    # POST /rest/v1/producto/ - Crea un nuevo producto
    path('', ProductoListCreateAPIView.as_view(), name='productos-list-create'),

    # Endpoint para buscar productos por palabra clave
    # GET /rest/v1/producto/buscar/?q=palabra
    path('buscar/', ProductoSearchAPIView.as_view(), name='productos-search'),
    path('<int:id>/', ProductoUpdateAPIView.as_view(), name='producto-update'),
    
]
