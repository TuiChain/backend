from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.response import Response
from django.contrib.auth.models import User

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
    Fetch the authentication token for the user with the given username and password
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Required fields: username and password'},status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials or unexistent user'},status=HTTP_404_NOT_FOUND)

    token = Token.objects.get(user=user)
    return Response({'message': 'User logged in with success', 'token': token.key}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    """
    Create a new User
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    if username is None or password is None or email is None or first_name is None or last_name is None:
        return Response({'error': 'Required Fields: username, email, password, first_name and last_name'}, status=HTTP_400_BAD_REQUEST)

    user = User.objects.filter(username=username).first()
    if user is not None:
        return Response({'error': 'That username is already taken'}, status=HTTP_403_FORBIDDEN)

    user = User.objects.filter(email=email).first()
    if user is not None:
        return Response({'error': 'That email is already taken'}, status=HTTP_403_FORBIDDEN)

    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    user.save()

    token = Token.objects.get(user=user)
    return Response({'message': 'User created with success', 'token': token.key}, status=HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes((AllowAny,))
def verify_email(request):
    """
    Verify if email can be used for account creation (signup)
    """
    email = request.data.get("email")

    if email is None:
        return Response({'error': 'Required fields: email'},status=HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()

    if user is None:
        return Response({'message': 'The given email is valid for signup'}, status=HTTP_200_OK)
    
    return Response({'error': 'Email already taken, please try another one'},status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def verify_username(request):
    """
    Verify if username can be used for account creation (signup)
    """
    username = request.data.get("username")

    if username is None:
        return Response({'error': 'Required fields: username'},status=HTTP_400_BAD_REQUEST)

    user = User.objects.filter(username=username).first()

    if user is None:
        return Response({'message': 'The given username is valid for signup'}, status=HTTP_200_OK)
    
    return Response({'error': 'Username already taken, please try another one'},status=HTTP_400_BAD_REQUEST)
