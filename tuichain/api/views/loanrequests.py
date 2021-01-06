from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from tuichain.api.models import LoanRequest, Investment
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
import decimal


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_loan_request(request):
    """
    Create new LoanRequest
    """
    user = request.user

    school = request.data.get("school")
    course = request.data.get("course")
    amount = request.data.get("amount")
    destination = request.data.get("destination")
    description = request.data.get("description")

    if (
        school is None
        or course is None
        or amount is None
        or destination is None
        or description is None
    ):
        return Response(
            {"error": "Required fields: school, course and amount"},
            status=HTTP_400_BAD_REQUEST,
        )

    # TODO: verify if User has complete profile and validated identity

    q = LoanRequest.objects.filter(student=user)
    q = q.filter(status=0)
    q = q.filter(status=1)
    loanrequests = q.filter(status=2)

    if len(loanrequests) >= 1:
        return Response(
            {
                "error": "An user cannot create Loan Requests when it has one currently undergoing"
            },
            status=HTTP_400_BAD_REQUEST,
        )

    # ...

    loanrequest = LoanRequest.objects.create(
        student=user,
        school=school,
        course=course,
        amount=amount,
        destination=destination,
        description=description,
    )
    loanrequest.save()

    return Response(
        {"message": "Loan Request successfully created"},
        status=HTTP_201_CREATED,
    )


@api_view(["PUT"])
@permission_classes((IsAdminUser,))
def validate_loan_request(request, id):
    """
    Validate a Loan Request
    """

    loanrequest = LoanRequest.objects.filter(id=id).first()

    if loanrequest is None:
        return Response(
            {"error": "Unexistent Loan Request"}, status=HTTP_404_NOT_FOUND
        )

    if loanrequest.validated:
        return Response(
            {"error": "The given Loan Request as already been validated"},
            status=HTTP_403_FORBIDDEN,
        )

    loanrequest.status = 1
    loanrequest.save()

    return Response(
        {"message": "Loan Request has been validated"}, status=HTTP_201_CREATED
    )


@api_view(["PUT"])
@permission_classes((IsAdminUser,))
def close_loan_request(request, id):
    """
    Close a Loan Request
    """

    loanrequest = LoanRequest.objects.filter(id=id).first()

    if loanrequest is None:
        return Response(
            {"error": "Unexistent Loan Request"}, status=HTTP_404_NOT_FOUND
        )

    if not loanrequest.active:
        return Response(
            {"error": "The given Loan Request as already been closed"},
            status=HTTP_403_FORBIDDEN,
        )

    loanrequest.status = 5
    loanrequest.save()

    return Response(
        {"message": "Loan Request has been closed"}, status=HTTP_201_CREATED
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_loan_request(request, id):
    """
    Get Loan Request with given ID
    """

    loanrequest = LoanRequest.objects.filter(id=id).first()

    # TODO: should we pass it only if it is validated?

    if loanrequest is None:
        return Response(
            {"error": "Loan Request with given ID not found"},
            status=HTTP_404_NOT_FOUND,
        )

    return Response(
        {
            "message": "Loan Request found with success",
            "loan_request": loanrequest.to_dict(),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_personal_loan_requests(request):
    """
    Get Loan Requests made by the authenticated user
    """

    user = request.user

    loanrequest_list = LoanRequest.objects.filter(student=user)

    result = [obj.to_dict() for obj in loanrequest_list]

    return Response(
        {
            "message": "Loan Requests fetched with success",
            "loanrequests": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_all_loan_requests(request):
    """
    Get all active loan requests
    """

    q = LoanRequest.objects.filter(status=0)
    q = q.filter(status=1)
    loanrequest_list = q.filter(status=2)

    result = [obj.to_dict() for obj in loanrequest_list]

    return Response(
        {
            "message": "Loan Requests fetched with success",
            "loanrequests": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAdminUser,))
def get_non_validated_loan_requests(request):
    """
    Get all active and non_validated loan requests
    """

    loanrequest_list = LoanRequest.objects.filter(status=0)

    result = [obj.to_dict() for obj in loanrequest_list]

    return Response(
        {
            "message": "Loan Requests fetched with success",
            "loanrequests": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_specific_state_loan_requests(request, status):
    """
    Get all loan requests at a given state
    """
    user = request.user

    loanrequest_list = LoanRequest.objects.filter(student=user, status=status)

    result = [obj.to_dict() for obj in loanrequest_list]

    return Response(
        {
            'message': 'Loan Requests fetched with success',
            'loanrequests': result,
            'count': len(result)
        },
        status=HTTP_200_OK
    )

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_specific_state_loan_requests(request, status):
    """
    Get all loan requests at a given state
    """
    user = request.user

    loanrequest_list = LoanRequest.objects.filter(student=user, status=status)

    result = [obj.to_dict() for obj in loanrequest_list]

    return Response(
        {
            'message': 'Loan Requests fetched with success',
            'loanrequests': result,
            'count': len(result)
        },
        status=HTTP_200_OK
    )

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_loan_request_investments(request, id):
    """
    Get investments for a given loan request
    """

    loanrequest = LoanRequest.objects.filter(id=id).first()

    if loanrequest is None:
        return Response(
            {"error": "Loan Request with given ID not found"},
            status=HTTP_404_NOT_FOUND,
        )

    investments = Investment.objects.filter(request=loanrequest)

    result = [obj.to_dict() for obj in investments]

    return Response(
        {
            "message": "Investments fetched with success for the given Loan Request",
            "count": len(result),
            "investments": result,
        },
        status=HTTP_200_OK,
    )
