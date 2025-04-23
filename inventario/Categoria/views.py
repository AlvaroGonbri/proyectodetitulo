from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.http.response import JsonResponse
from .models import *
from .serializers import *

# Create your views here.


class Clase1(APIView):

    def get(self, request):
        # select * from caterorias order by id desc
        data = Categoria.objects.order_by('-id_categoria').all()
        datos_json = CategoriaSerializer(data, many=True)
        return Response(datos_json.data)
        pass


