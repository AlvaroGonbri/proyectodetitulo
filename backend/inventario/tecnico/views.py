from django.http import JsonResponse
from rest_framework.views import APIView # type: ignore
from http import HTTPStatus
from .models import Tecnico
from .serializers import TecnicoSerializer

class TecnicoListAPIView(APIView):
    """
    Endpoint para listar todos los técnicos.
    GET: Lista todos los técnicos ordenados por rut_trab ascendente.
    """
    def get(self, request):
        tecnicos = Tecnico.objects.order_by('rut_trab').all()
        serializer = TecnicoSerializer(tecnicos, many=True)
        return JsonResponse({"data": serializer.data}, status=HTTPStatus.OK, safe=False)
