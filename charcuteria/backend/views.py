from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from backend.serializers import UserRegistrationSerializer, UserLoginSerializer, productSerializer
from rest_framework.decorators import api_view, permission_classes
from backend.models import User, Producto


class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'Usuario loggeado exitosamente',
            'token' : serializer.data['token'],
            'role': serializer.data['email']
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)



class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        cedula = request.data["profile"]["doc_identidad"]
        if(cedula.isdigit()):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'msg': 'Usuario registrado exitosamente',
                'status': status_code
            }
        else:
            status_code = status.HTTP_200_OK
            response = {
                'success': False,
                'msg': 'La cedula no puede contener ni letras ni caracteres especiales',
                'status': status_code
                }

        return Response(response, status=status_code)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def product_list(request):

    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = productSerializer(productos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if(request.data["codigo"].isdigit()):
            serializer = productSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            status_code = status.HTTP_200_OK
            response = {
                'success': False,
                'msg': 'El codigo solo puede contener numeros',
                'status': status_code
                }
            return Response(response, status=status_code)




@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def product_details(request, id):

    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = productSerializer(producto)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = productSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Producto.objects.filter(id = id).delete()

        status_code = status.HTTP_204_NO_CONTENT

        response = {
            'success': True,
            'msg': 'producto eliminado con exito',
            'status': status_code
        }

        return Response(response, status=status_code)





