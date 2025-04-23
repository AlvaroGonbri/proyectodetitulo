from rest_framework import serializers
from .models import *


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ("cod_material", "nom_producto", "cant_existencia", "descripcion", "stock_minimo", "stock_maximo", "categoria_id")