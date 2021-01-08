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
from tuichain.api import controller


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_blockchain_info(request):
    """
    Get Blockchain information
    """
    if controller is None:
        return Response(
            {"error": "Something went wrong with the Tuichain's connection..."},
            status=HTTP_404_NOT_FOUND,
        )

    return Response(
        {
            "chain_id": controller.chain_id,
            "dai_contract_address": controller.dai_contract_address,
        },
        status=HTTP_200_OK,
    )
