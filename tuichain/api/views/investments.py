from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from tuichain.api.models import Investment, LoanRequest
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
import decimal

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_investment(request):
    """
    Create new Investment
    """
    user = request.user

    loanrequest_id = request.data.get('request')
    amount = request.data.get('amount')

    if loanrequest_id is None or amount is None:
        return Response({'error': 'Required fields: request and amount'},status=HTTP_400_BAD_REQUEST)


    loanrequest = LoanRequest.objects.filter(id=loanrequest_id).first()

    if loanrequest is None:
        return Response({'error': 'Unexistent Loan Request'},status=HTTP_404_NOT_FOUND)

    if loanrequest.student == user.id:
        return Response({'error': 'Cannot invest in your own Loan Request'},status=HTTP_403_FORBIDDEN)

    if not loanrequest.validated:
        return Response({'error': 'The given Loan Request is not validated yet'},status=HTTP_403_FORBIDDEN)

    if not loanrequest.active:
        return Response({'error': 'The given Loan Request is not active anymore'},status=HTTP_403_FORBIDDEN)

    if loanrequest.student == user:
        return Response({'error': 'A user cannot invest in its own Loan Requests'},status=HTTP_403_FORBIDDEN)

    decimal_amount = decimal.Decimal(amount)

    new_amount = decimal_amount + loanrequest.current_amount

    if new_amount <= loanrequest.amount :
        investment = Investment.objects.create(amount=decimal_amount, investor=user, request=loanrequest)
        investment.save()

        loanrequest.current_amount = new_amount
        loanrequest.save()

        return Response({'message': 'Investment created with success'}, status=HTTP_201_CREATED)
            
    else: 
        return Response({'error': 'An Investment with that amount is not possible at the moment'}, status=HTTP_400_BAD_REQUEST)