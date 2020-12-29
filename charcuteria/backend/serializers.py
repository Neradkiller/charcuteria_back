from rest_framework import serializers
from backend.models import User, Perfil, Direccion

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings


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
        user = User.objects.create_user(**validated_data)

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
