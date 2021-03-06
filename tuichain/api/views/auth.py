from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_408_REQUEST_TIMEOUT,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from tuichain.api.services.email import send_email, send_email_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
    Fetch the authentication token for the user with the given username and password

    Parameters
    ----------
    username : string

        User's username.

    password : string

        User's password.

    Returns
    -------
    200
        User Logged in with success.

    400
        Username and password required.

    404
        Invalid credentials or user not found.

    """
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response(
            {"error": "Required fields: username and password"},
            status=HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"error": "Invalid credentials or unexistent user"},
            status=HTTP_404_NOT_FOUND,
        )

    token = Token.objects.get(user=user)
    return Response(
        {
            "message": "User logged in with success",
            "token": token.key,
            "is_admin": user.is_superuser,
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    """
    Create a new user

    Parameters
    ----------
    username : string

        User's username.

    email : string

        User's email.

    password : string

        User's password.

    first_name : string

        User's first name

    last_name : string

        User's last name.

    Returns
    -------
    201
        User created with success.

    400
        Username, email, password, first name and last name are required

    403
        Username or email are already taken.


    """

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    if (
        username is None
        or password is None
        or email is None
        or first_name is None
        or last_name is None
    ):
        return Response(
            {
                "error": "Required Fields: username, email, password, first_name and last_name"
            },
            status=HTTP_400_BAD_REQUEST,
        )

    user = User.objects.filter(username=username).first()
    if user is not None:
        return Response(
            {"error": "That username is already taken"},
            status=HTTP_403_FORBIDDEN,
        )

    user = User.objects.filter(email=email).first()
    if user is not None:
        return Response(
            {"error": "That email is already taken"}, status=HTTP_403_FORBIDDEN
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    user.save()

    send_email(
        subject="Welcome to Tuichain!",
        message="Your Tuichain's account is now created! \n\n Thank you! \n\n Please, complete your Profile with your personal info so you can enjoy the app as a whole.",
        to_email=email,
        html_file="email.html",
    )

    token = Token.objects.get(user=user)
    return Response(
        {"message": "User created with success", "token": token.key},
        status=HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes((AllowAny,))
def verify_email(request):
    """
    Verify if email can be used for account creation (signup)

    Parameters
    ----------
    email : string

        User's email.

    Returns
    -------
    200
        Email is valid for signup.

    400
        Email is missing or is already taken.

    """

    email = request.data.get("email")

    if email is None:
        return Response(
            {"error": "Required fields: email"}, status=HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(email=email).first()

    if user is None:
        return Response(
            {"message": "The given email is valid for signup"},
            status=HTTP_200_OK,
        )

    return Response(
        {"error": "Email already taken, please try another one"},
        status=HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes((AllowAny,))
def verify_username(request):
    """
    Verify if username can be used for account creation (signup)

    Parameters
    ----------
    username : string

        User's username.

    Returns
    -------
    200
        Username is valid for signup.

    400
        Username is missing or is already taken.

    """

    username = request.data.get("username")

    if username is None:
        return Response(
            {"error": "Required fields: username"}, status=HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(username=username).first()

    if user is None:
        return Response(
            {"message": "The given username is valid for signup"},
            status=HTTP_200_OK,
        )

    return Response(
        {"error": "Username already taken, please try another one"},
        status=HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes((AllowAny,))
def email_reset_password(request):
    """
    Send email to user's email to change his password

    Parameters
    ----------
    email : string

        User's email.

    Returns
    -------
    200
        Email sent to redefine password.

    400
        Email is required.

    404
        Email not registered.

    """

    email = request.data.get("email")

    if email is None:
        return Response(
            {"error": "Required fields: email"}, status=HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(email=email).first()

    if user is None:
        return Response(
            {"error": "The given email is not registered in our platform"},
            status=HTTP_404_NOT_FOUND,
        )

    id_number = str(user.pk)
    token = str(PasswordResetTokenGenerator().make_token(user))
    send_email_password(
        subject="Redefine TuiChain Password",
        message="You have requested a password change for the account associated with this email \n\n If this email is not intended for you, please ignore it. \n\n Use the following link to redefine your password: http://127.0.0.1:8000/api/auth/reset_password/"
        + id_number
        + "/"
        + token
        + "/ \n\n Thank you for using TuiChain!",
        to_email=email,
        token=token,
        id=id_number,
        html_file="redefine_password.html",
    )

    return Response(
        {"message": "Email has been sent to redefine password"},
        status=HTTP_200_OK,
    )


@api_view(["PUT"])
@permission_classes((AllowAny,))
def reset_password(request, id, token):
    """
    Resets User's password

    Parameters
    ----------
    password : string

        User's new password.

    Returns
    -------
    200
        Password has been reset.

    400
        Password is missing.

    408
        Password reset link has expired.


    """

    pwd = request.data.get("password")
    if pwd is None:
        return Response(
            {"error": "Required fields: password"}, status=HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(pk=id).first()
    # This should never happen
    # if user is None:
    #    return Response({'error': 'The given user is not registered in our platform'}, status=HTTP_404_NOT_FOUND)

    if PasswordResetTokenGenerator().check_token(user, token) is True:
        user.set_password(pwd)
        user.save()

        return Response(
            {"message": "Password has been reset"}, status=HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Password reset link has expired"},
            status=HTTP_408_REQUEST_TIMEOUT,
        )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def is_admin_user(request):
    """
    Checks if the user is an admin (superuser) through the authentication token

    Parameters
    ----------

    Returns
    -------
    200
        Verification was done successfully

    """

    user = request.user

    return Response(
        {
            "message": "Verification was done successfully",
            "is_admin": user.is_superuser,
        },
        status=HTTP_200_OK,
    )
