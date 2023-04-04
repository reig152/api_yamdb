from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import SignUpSerializer, TokenSerializer

User = get_user_model()

SIGNUP_PATH = '/api/v1/auth/signup/'
MY_EMAIL = 'myemail@fake.com'


def send_confirmation_code(user):
    """
    Эта функция формирует и отправляет письмо с кодом подтверждения.
    """
    confirmation_code = user.confirmation_code
    email = user.email
    text = (
        f'Данные для получения токена: confirmation_code - {confirmation_code}'
        f', username - {user.username}.'
    )
    theme = 'Код подтверждения.'
    send_mail(
        theme,
        text,
        MY_EMAIL,
        [email],
        fail_silently=False
    )
    return


@api_view(['POST'])
def sign_up_and_confirmation_code(request):
    """
    Эта функция создаёт пользователя и отправляет код подтверждения на email,
    если пользователь существует, то просто отправляет письмо с кодом.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    if User.objects.filter(username=username, email=email).exists():
        user = get_object_or_404(User, username=username, email=email)
        send_confirmation_code(user=user)
        return Response(
            (f'Код подтверждения для пользоватедля {username} '
             f'отправлен на {email}'),
            status=status.HTTP_200_OK
        )
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation_code(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    """ Эта функция генерирует JWT токен."""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User,
                                 username=username,
                                 confirmation_code=code)
        token = AccessToken.for_user(user)
        response = {'token': str(token)}
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
