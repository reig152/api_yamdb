from django.contrib.auth import get_user_model
from rest_framework import serializers

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
