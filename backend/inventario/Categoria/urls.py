from django.urls import path
from .views import CategoriaListCreateAPIView

urlpatterns = [
    path('', CategoriaListCreateAPIView.as_view(), name='categoria-list-create'),
]
