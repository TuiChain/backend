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
    
    user = request.user

    school = request.data.get('school')
    course = request.data.get('course')
    amount = request.data.get('amount')

    if school is None or course is None or amount is None:
        return Response({'error': 'Required fields: school, course and amount'},status=HTTP_400_BAD_REQUEST)

    # TODO: verify if User has complete profile and validated identity

    loanrequests = LoanRequest.objects.filter(student=user,active=True)

    if len(loanrequests) >= 1:
        return Response({'error': 'An user cannot create Loan Requests when it has one currently undergoing'}, status=HTTP_400_BAD_REQUEST)

    # ...

    loanrequest = LoanRequest.objects.create(student=user, school=school, course=course, amount=amount)
    loanrequest.save()

    return Response({'message': 'Loan Request successfully created'},status=HTTP_201_CREATED)

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
        return Response({'error': 'Unexistent Loan Request'},status=HTTP_404_NOT_FOUND)

    if loanrequest.validated:
        return Response({'error': 'The given Loan Request as already been validated'},status=HTTP_403_FORBIDDEN)

    loanrequest.validated = True
    loanrequest.save()

    return Response({'message': 'Loan Request has been validated'}, status=HTTP_201_CREATED)

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
        return Response({'error': 'Unexistent Loan Request'},status=HTTP_404_NOT_FOUND)

    if not loanrequest.active:
        return Response({'error': 'The given Loan Request as already been closed'},status=HTTP_403_FORBIDDEN)

    loanrequest.active = False
    loanrequest.save()

    return Response({'message': 'Loan Request has been closed'}, status=HTTP_201_CREATED)

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
        return Response({'error': 'Loan Request with given ID not found'}, status=HTTP_404_NOT_FOUND)

    return Response(
        {
            'message': 'Loan Request found with success',
            'loan_request': loanrequest.to_dict()
        },
        status=HTTP_200_OK
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
            'message': 'Loan Requests fetched with success',
            'loanrequests': result,
            'count': len(result)
        },
        status=HTTP_200_OK
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
    

    loanrequest_list = LoanRequest.objects.filter(active=True)

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
    

    loanrequest_list = LoanRequest.objects.filter(active=True, validated=False)

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
        return Response({'error': 'Loan Request with given ID not found'}, status=HTTP_404_NOT_FOUND)

    investments = Investment.objects.filter(request=loanrequest)

    result = [obj.to_dict() for obj in investments]

    return Response(
        {
            'message': 'Investments fetched with success for the given Loan Request',
            'count': len(result),
            'investments': result
        },
        status=HTTP_200_OK
    )



