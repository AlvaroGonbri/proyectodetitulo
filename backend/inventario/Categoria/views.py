from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria
from .serializers import CategoriaSerializer

class CategoriaListCreateAPIView(APIView):
    """
    Endpoint para listar y crear categorías
    GET: Lista todas las categorías ordenadas por ID descendente
    POST: Crea una nueva categoría
    """
    
    def get(self, request):
        """Obtiene todas las categorías ordenadas por ID descendente"""
        try:
            categorias = Categoria.objects.order_by('-id_categoria').all()
            serializer = CategoriaSerializer(categorias, many=True)
            return Response(
                {"data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": "error", "mensaje": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Crea una nueva categoría con validación de campos"""
        try:
            # Usar request.data para soportar JSON y form-data
            data = request.data
            
            # Validación manual del campo obligatorio
            if not data.get('nom_categoria'):
                return Response(
                    {"status": "error", "mensaje": "El campo 'nom_categoria' es obligatorio"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validación con serializer
            serializer = CategoriaSerializer(data=data)
            if serializer.is_valid():
                categoria = serializer.save()
                return Response(
                    {
                        "status": "success",
                        "mensaje": "Categoría creada exitosamente",
                        "categoria": CategoriaSerializer(categoria).data
                    },
                    status=status.HTTP_201_CREATED
                )
                
            return Response(
                {"status": "error", "mensaje": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"status": "error", "mensaje": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria
from .serializers import CategoriaSerializer

class CategoriaUpdateAPIView(APIView):
    def put(self, request, id):
        # Validar que el campo 'nom_categoria' esté presente y no vacío
        if request.data.get("nom_categoria") is None or not request.data.get("nom_categoria"):
            return Response(
                {"status": "error", "mensaje": "El campo nom_categoria es obligatorio"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Verificar que la categoría exista
            categoria = Categoria.objects.get(pk=id)
            # Actualizar el nombre
            categoria.nom_categoria = request.data.get("nom_categoria")
            categoria.save()
            return Response(
                {"status": "success", "mensaje": "Se modificó el registro exitosamente"},
                status=status.HTTP_200_OK
            )
        except Categoria.DoesNotExist:
            return Response(
                {"status": "error", "mensaje": "Categoría no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
