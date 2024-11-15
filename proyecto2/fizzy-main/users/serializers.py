from rest_framework import serializers
from .models import CustomUser      

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role' , 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_role(self, value):
        if not value:
            raise serializers.ValidationError("El rol es obligatorio.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')  # Saca la contraseña del diccionario
        user = CustomUser(**validated_data)  # Crea el usuario sin la contraseña primero
        user.set_password(password)  # Establece la contraseña usando el método correcto
        user.save()  # Guarda el usuario con la contraseña encriptada
        return user