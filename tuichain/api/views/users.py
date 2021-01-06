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
        return Response(
            {"error": "User with given ID not found"}, status=HTTP_404_NOT_FOUND
        )

    return Response(
        {
            "message": "User found with success",
            "user": result.profile.to_dict(private=user.id == result.id),
        },
        status=HTTP_200_OK,
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
            "message": "User gotten with success",
            "user": user.profile.to_dict(private=True),
        },
        status=HTTP_200_OK,
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
            "message": "Users fetched with success",
            "users": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def update_profile(request):
    """
    Update profile of authenticated user
    """

    user = request.user

    full_name = request.data.get('full_name')
    birth_date = request.data.get('birth_date')
    address = request.data.get('address')
    zip_code = request.data.get('zip_code')
    country = request.data.get('country')
    city = request.data.get('city')
    id_number = request.data.get('id_number')
    short_bio = request.data.get('short_bio')
    profile_image = request.data.get('profile_image')

    profile = user.profile

    try:
        if full_name is not None:
            profile.full_name = full_name
        if birth_date is not None:
            profile.birth_date = birth_date
        if address is not None:
            profile.address = address
        if zip_code is not None:
            profile.zip_code = zip_code
        if country is not None:
            profile.country = country
        if city is not None:
            profile.city = city
        if id_number is not None:
            profile.id_number = id_number
        if short_bio is not None:
            profile.short_bio = short_bio
        if profile_image is not None:
            profile.profile_image = profile_image

        profile.save()

    except Exception as e:
        return Response(
            {"error": "Could not update the profile", "details": e.args},
            status=HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "message": "User profile updated with success",
            "user": profile.to_dict(private=True),
        },
        status=HTTP_200_OK,
    )
