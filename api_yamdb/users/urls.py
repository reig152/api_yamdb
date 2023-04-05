from django.urls import path

from .views import get_jwt_token, sign_up_and_confirmation_code

app_name = 'users'

urlpatterns = [
    path('signup/', sign_up_and_confirmation_code),
    path('token/', get_jwt_token)
]
