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
from tuichain.api import controller


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_loan_request(request):
    """
    Create new LoanRequest

    Parameters
    ----------
    school : string

        User's desired school.

    course : string

        User's desired course.

    amount : float

        Amount of money pretended by the user.

    Returns
    -------
    201
        Loan request created successfully.

    400
        Required fields are missing or user already has an undergoing loan request.

    """

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
            {
                "error": "Required fields: school, course, amount, destination and description"
            },
            status=HTTP_400_BAD_REQUEST,
        )

    # TODO: verify if User has complete profile and validated identity

    q = LoanRequest.objects.filter(student=user)
    q = q.exclude(status=3)
    q = q.exclude(status=4)
    loanrequests = q.exclude(status=5)

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
@permission_classes((IsAuthenticated,))
def cancel_loan_request(request, id):
    """
    Cancel a pending Loan Request
    """

    user = request.user

    loanrequest = LoanRequest.objects.filter(id=id).first()

    if loanrequest is None:
        return Response(
            {"error": "Unexistent Loan Request"}, status=HTTP_404_NOT_FOUND
        )

    if loanrequest.student != user:
        return Response(
            {"error": "Loan Request does not belong to logged user"},
            status=HTTP_403_FORBIDDEN,
        )

    if loanrequest.status > 0:
        return Response(
            {"error": "That Loan Request cannot be cancelled"},
            status=HTTP_400_BAD_REQUEST,
        )

    # set status as cancelled
    loanrequest.status = 5
    loanrequest.save()

    return Response(
        {"message": "Loan Request has been canceled"}, status=HTTP_201_CREATED
    )


@api_view(["PUT"])
@permission_classes((IsAdminUser,))
def validate_loan_request(request, id):
    """
    Validate a Loan Request

    Parameters
    ----------
    id : integer

        Loan request's identifier.

    Returns
    -------
    201
        Loan request validated successfully.

    403
        Loan request has already been validated.

    404
        Unexistent loan request.

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

    Parameters
    ----------
    id : integer

        Loan request's identifier.

    Returns
    -------
    201
        Loan request closed successfully.

    403
        Loan request already closed.

    404
        Loan request not found.

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

    Parameters
    ----------
    id : integer

        Loan Request's identifier.

    Returns
    -------
    200
        Loan request found with success.

    404
        Loan request not found.

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

    Parameters
    ----------

    Returns
    -------
    200
        loan requests fetched with success.

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

    Parameters
    ----------

    Returns
    -------
    200
        Loan requests fetched with success.

    """

    q = LoanRequest.objects.exclude(status=3)
    q = q.exclude(status=4)
    loanrequest_list = q.exclude(status=5)

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

    Parameters
    ----------

    Returns
    -------
    200
        loan requests fetched with success.

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
            "message": "Loan Requests fetched with success",
            "loanrequests": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_loan_request_investments(request, id):
    """
    Get investments for a given loan request

    Parameters
    ----------
    id : integer

        Loan request's identifier.

    Returns
    -------
    200
        Investments from given loan requests fetched successfully.

    404
        Loan request not found.

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


@api_view(["GET"])
@permission_classes((IsAuthenticated))
def get_loan_request_investors(request, id):
    """
    Get loaners for a given loan request

    Parameters
    ----------
    id : integer

        Loan request's identifier.

    Returns
    -------
    200
        Loaners from given loan requests fetched successfully.

    404
        Loan request not found.

    """

    loanrequest = LoanRequest.objects.filter(id=id).first()

    if loanrequest is None:
        return Response(
            {"error": "Loan Request with given ID not found"},
            status=HTTP_404_NOT_FOUND,
        )

    investments = Investment.objects.filter(request=loanrequest)

    result = [obj.investor.to_dict() for obj in investments]

    return Response(
        {
            "message": "Loaners fetched with success for the given Loan Request",
            "count": len(result),
            "loaners": result,
        },
        status=HTTP_200_OK,
    )
