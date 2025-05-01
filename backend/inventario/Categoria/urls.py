from django.urls import path
from .views import CategoriaListCreateAPIView, CategoriaUpdateAPIView

urlpatterns = [
    path('', CategoriaListCreateAPIView.as_view(), name='categoria-list-create'),
    path('', CategoriaListCreateAPIView.as_view(), name='categoria-list-create'),
    path('<int:id>/', CategoriaUpdateAPIView.as_view(), name='categoria-update')
]
