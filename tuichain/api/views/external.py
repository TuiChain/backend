from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import *
from django.contrib.auth import authenticate
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from tuichain.api.models import Profile, IDVerifications
from tuichain.api.services.id_verification import (
    create_verification_intent,
    get_verification_intent,
)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def request_id_verification(request):
    """
    Request ID Verification to Stripe

    Parameters
    ----------

    Returns
    -------
    201
        Verification intent created successfully.

    400
        Verification intent not possible or return and refresh links missing.


    """

    user = request.user

    try:
        verification_intent = create_verification_intent(user.profile.id_number)
    except Exception as e:
        return Response(
            {
                "error": "Could not create verification intent",
                "details": e.args,
            },
            status=HTTP_400_BAD_REQUEST,
        )

    id_verification = user.id_verification

    id_verification.verification_id = verification_intent.id
    id_verification.person_id = verification_intent.person
    id_verification.validated = False
    id_verification.save()

    return Response(
        {
            "message": "Verication intent successfully created",
            "redirect_to_url": verification_intent.next_action.redirect_to_url,
            "intent_id": verification_intent.id,
            "person": verification_intent.person,
        },
        status=HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_id_verification_result(request, verification_intent_id):
    """
    Request ID Verification results to Stripe

    Parameters
    ----------
    verification_intent_id : integer

        verification identifier.

    Returns
    -------
    200
        Verification intent created successfully.

    400
        Verification intent not possible or return and refresh links missing.


    """

    user = request.user
    try:
        verification_intent = get_verification_intent(verification_intent_id)
    except Exception as e:
        return Response(
            {
                "error": "Could not create verification intent",
                "details": e.args,
            },
            status=HTTP_400_BAD_REQUEST,
        )
    id_verification = user.id_verification

    if verification_intent.status == "succeeded":
        id_verification.validated = True
        id_verification.save()

    return Response(
        {
            "message": "Verication results",
            "data": verification_intent,
        },
        status=HTTP_200_OK,
    )
