from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.http.response import JsonResponse
from .models import *
from .serializers import *
from django.http import Http404
from http import HTTPStatus

# Create your views here.

#agregar cabezera a json

class Clase1(APIView):



    def get(self, request):
        # select * from productos order by id desc
        data = Producto.objects.order_by('-cod_material').all()
        datos_json = CategoriaSerializer(data, many=True)
        return JsonResponse({"data":datos_json.data}, status=HTTPStatus.OK)
        

    def post(self, request):
        if request.data.get("nom_producto")==None or not request.data['nom_producto']:
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"})
            status=HTTPStatus.BAD_REQUEST
        try:
            Producto.objects.create(nom_producto=request.data['nom_producto'])
            return JsonResponse({"estado":"ok", "mensaje":"Se crea el registro exitosamente"},
            status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404
        

class Clase2(APIView):
    def get(self, request):
        palabra_clave = request.GET.get('q', '')
        productos = Producto.objects.filter(nom_producto__icontains=palabra_clave)
        if not productos.exists():
            raise Http404("No se encontraron productos con esa palabra clave.")
        data = [
            {
                "cod_material": p.cod_material,
                "nom_producto": p.nom_producto,
                "cant_existencia": p.cant_existencia,
                "descripcion": p.descripcion,
                "stock_minimo": p.stock_minimo,
                "stock_maximo": p.stock_maximo,
                "categoria_id": p.categoria_id,
            }
            for p in productos
        ]
        return JsonResponse({"data": data}, status=200, safe=False)