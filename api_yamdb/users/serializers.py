from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import UserConfirmationCode

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Запрещено использовать me '
                                              'в качестве username!')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        super().validate(attrs)
        user = get_object_or_404(User, username=attrs['username'])
        if not UserConfirmationCode.objects.filter(user=user).exists():
            raise serializers.ValidationError('Код подтверждения '
                                              'ранее не запрашивался.')
        if (user.confirmation_code.confirmation_code
                != attrs['confirmation_code']):
            raise serializers.ValidationError('Невалидный код!')
        return attrs
