from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from backend.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.decorators import api_view, permission_classes
from backend.models import User


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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED

        response = {
            'success': True,
            'msg': 'Usuario registrado exitosamente',
            'status': status_code
        }

        return Response(response, status=status_code)