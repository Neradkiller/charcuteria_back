from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from backend.models import (Direccion, Perfil, Producto,
                            User, UserManager)

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = ('name', 'name1', 'lastname','lastname1', 'doc_identidad')

class UserDirecctionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direccion
        fields = ('direccion',)

class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)
    direccion = UserDirecctionsSerializer(required=False)

    class Meta:
        model = User
        fields = ('email','password', 'profile', 'direccion')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        profile_data = validated_data.pop('profile')
        direccion_data = validated_data.pop('direccion')
        role = 'C'
        user = User.objects.create_user(validated_data['email'],validated_data['password'], role)

        Perfil.objects.create(
            user=user,
            name=profile_data['name'],
            name1=profile_data['name1'],
            lastname=profile_data['lastname'],
            lastname1=profile_data['lastname1'],
            doc_identidad=profile_data['doc_identidad']
        )

        Direccion.objects.create(
            user=user,
            direccion=direccion_data['direccion']
        )
        return user


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Usuario no encontrado.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Usuario con esa contraseña y email no fue encontrado.'
            )
        return {
            'email':user.role,
            'token': jwt_token,
        }


class productSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    codigo = serializers.CharField(max_length=5)
    nombre = serializers.CharField(max_length=50)
    descripcion = serializers.CharField(max_length=300)
    marca = serializers.CharField(max_length=50)
    tipo = serializers.CharField(max_length=50)
    fecha_vencimiento = serializers.DateField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    peso_kg = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)


    def create(self, validated_data):
        """
        Crear un objeto de tipo Producto y le asocia su precio
        """
        producto = Producto.objects.create(**validated_data)
        return producto
    
    def update(self, instance, validated_data):
        """
        Actualiza los datos basicos asociados a un producto
        """
        instance.codigo = validated_data.get('codigo', instance.codigo)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.marca = validated_data.get('marca', instance.marca)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.fecha_vencimiento = validated_data.get('fecha_vencimiento', instance.fecha_vencimiento)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.peso_kg = validated_data.get('peso_kg', instance.peso_kg)
        instance.save()
        return instance

