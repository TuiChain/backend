from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from tuichain.api.models import Profile
from django.contrib.auth.models import User
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
from django.core import serializers

# Add here routes related to the Users
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_user(request, id):
    """
    Get User with given ID
    """

    user = request.user

    result = User.objects.filter(id=id).first()

    if result is None:
        return Response({'error': 'User with given ID not found'}, status=HTTP_404_NOT_FOUND)
    
    return Response(
        {
            'message': 'User found with success', 
            'user': result.profile.to_dict(private=user.id==result.id)
        }, 
        status=HTTP_200_OK
    )

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_me(request):
    """
    Get personal profile
    """
    user = request.user

    return Response(
        {
            'message': 'User gotten with success', 
            'user': user.profile.to_dict(private=True)
        }, 
        status=HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_all(request):
    """
    Get all users (public profile)
    """

    user_list = User.objects.all()

    result = [user.profile.to_dict() for user in user_list]

    return Response(
        {
            'message': 'Users fetched with success', 
            'users': result, 
            'count': len(result)
        }, 
        status=HTTP_200_OK
    )

