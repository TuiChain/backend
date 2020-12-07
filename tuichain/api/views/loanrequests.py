from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from tuichain.api.models import LoanRequest
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

    school = request.data.get('school')
    course = request.data.get('course')
    amount = request.data.get('amount')

    if school is None or course is None or amount is None:
        return Response({'error': 'Required fields: school, course and amount'},status=HTTP_400_BAD_REQUEST)

    # TODO: verify if User has complete profile and validated identity
    # TODO: add validations to prevent users from creating/having more than one active LoanRequest at a time
    # ...

    loanrequest = LoanRequest.objects.create(student=user, school=school, course=course, amount=amount)
    loanrequest.save()

    return Response({'message': 'Loan Request successfully created'},status=HTTP_201_CREATED)
