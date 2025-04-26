from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.http.response import JsonResponse
from .models import *
from .serializers import *
from django.http import Http404
from http import HTTPStatus

# Create your views here.


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

    def get(self, request, id):
        try:
            data = Producto.objects.get(cod_material=id)
            return JsonResponse({
                "data": {
                    "cod_material": data.cod_material,
                    "nom_producto": data.nom_producto,
                    "cant_existencia": data.cant_existencia,
                    "descripcion": data.descripcion,
                    "stock_minimo": data.stock_minimo,
                    "stock_maximo": data.stock_maximo,
                    "categoria_id": data.categoria_id,
                }
            }, status=HTTPStatus.OK)
        except Producto.DoesNotExist:
            raise Http404()
