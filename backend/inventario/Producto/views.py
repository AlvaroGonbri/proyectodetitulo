import json
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from http import HTTPStatus
from .models import Producto
from .serializers import ProductoSerializer  # Cambiado a ProductoSerializer


class ProductoListCreateAPIView(APIView):
    """
    Endpoint para listar y crear productos
    GET: Lista todos los productos ordenados por código descendente
    POST: Crea un nuevo producto
    """
    
    def get(self, request):
        """Obtiene todos los productos ordenados por código descendente"""
        productos = Producto.objects.order_by('-cod_material').all()
        serializer = ProductoSerializer(productos, many=True)
        return JsonResponse({"data": serializer.data}, status=HTTPStatus.OK, safe=False)

    def post(self, request):
        """Crea un nuevo producto con validación de campos"""
        try:
            # Usar request.data de DRF para soportar JSON y form-data
            data = request.data if request.content_type == 'application/json' else request.POST
            
            # Validación de campos obligatorios
            required_fields = ['nom_producto', 'cant_existencia', 'descripcion', 'categoria_id']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse(
                        {"status": "error", "mensaje": f"Campo requerido: {field}"},
                        status=HTTPStatus.BAD_REQUEST
                    )

            # Creación usando el serializer para mejor control
            serializer = ProductoSerializer(data=data)
            if serializer.is_valid():
                producto = serializer.save()
                return JsonResponse(
                    {
                        "status": "success",
                        "mensaje": "Producto creado exitosamente",
                        "producto": ProductoSerializer(producto).data
                    },
                    status=HTTPStatus.CREATED
                )
            return JsonResponse(
                {"status": "error", "mensaje": serializer.errors},
                status=HTTPStatus.BAD_REQUEST
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "mensaje": str(e)},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

class ProductoSearchAPIView(APIView):
    """
    Endpoint para búsqueda de productos
    GET: Busca productos por palabra clave en el nombre (parámetro 'q')
    """
    
    def get(self, request):
        """Busca productos por término en el nombre"""
        search_term = request.GET.get('q', '').strip()
        
        if not search_term:
            return JsonResponse(
                {"data": [], "mensaje": "Ingrese un término de búsqueda"},
                status=HTTPStatus.OK
            )

        productos = Producto.objects.filter(nom_producto__icontains=search_term)
        
        if not productos.exists():
            raise Http404("No se encontraron productos con ese criterio")

        serializer = ProductoSerializer(productos, many=True)
        return JsonResponse({"data": serializer.data}, status=HTTPStatus.OK, safe=False)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from .serializers import ProductoSerializer

class ProductoUpdateAPIView(APIView):
    """
    Endpoint para actualizar un producto por su ID
    PUT: Actualiza los datos de un producto existente
    """
    def put(self, request, id):
        try:
            producto = Producto.objects.get(pk=id)
        except Producto.DoesNotExist:
            return Response(
                {"status": "error", "mensaje": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validación básica de campos obligatorios
        required_fields = ['nom_producto', 'cant_existencia', 'descripcion', 'stock_minimo', 'stock_maximo', 'categoria_id']
        for field in required_fields:
            if request.data.get(field) is None or request.data.get(field) == "":
                return Response(
                    {"status": "error", "mensaje": f"El campo '{field}' es obligatorio"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Actualiza los campos
        producto.nom_producto = request.data.get('nom_producto')
        producto.cant_existencia = request.data.get('cant_existencia')
        producto.descripcion = request.data.get('descripcion')
        producto.stock_minimo = request.data.get('stock_minimo')
        producto.stock_maximo = request.data.get('stock_maximo')
        producto.categoria_id = request.data.get('categoria_id')
        producto.save()

        return Response(
            {
                "status": "success",
                "mensaje": "Producto actualizado exitosamente",
                "producto": ProductoSerializer(producto).data
            },
            status=status.HTTP_200_OK
        )
