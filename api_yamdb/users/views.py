from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from random import randint
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import UserConfirmationCode
from .serializers import SignUpSerializer, TokenSerializer

User = get_user_model()

SIGNUP_PATH = '/api/v1/auth/signup/'
MY_EMAIL = 'myemail@fake.com'


def confirmation_code_generate():
    confirmation_code = ''
    for i in range(6):
        num = str(randint(1, 9))
        confirmation_code += num
    return confirmation_code


def create_confirmation_code(user):
    confirmation_code = confirmation_code_generate()
    attrs = {
        'user': user,
        'confirmation_code': confirmation_code
    }
    code = UserConfirmationCode.objects.create(**attrs)
    return code


def send_confirmation_code(code):
    """
    Эта функция формирует и отправляет письмо с кодом подтверждения.
    """
    confirmation_code = code.confirmation_code
    email = code.user.email
    username = code.user.username
    text = (
        f'Данные для получения токена: confirmation_code - {confirmation_code}'
        f', username - {username}.'
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
        if not UserConfirmationCode.objects.filter(user=user).exists():
            create_confirmation_code(user)
        code = get_object_or_404(UserConfirmationCode, user=user)
        send_confirmation_code(code)
        return Response(
            (f'Код подтверждения для пользоватедля {username} '
             f'отправлен на {email}'),
            status=status.HTTP_200_OK
        )
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        code = create_confirmation_code(user)
        send_confirmation_code(code)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    """ Эта функция генерирует JWT токен."""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        user = get_object_or_404(User,
                                 username=username)
        token = AccessToken.for_user(user)
        response = {'token': str(token)}
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
