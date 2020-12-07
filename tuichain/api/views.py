from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.decorators import action
from tuichain.api.serializers import StudentSerializer, InvestorSerializer, InvestmentSerializer, LoanRequestSerializer
from tuichain.api.models import Student, Investor, Investment, LoanRequest
import decimal
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class InvestorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows investors to be viewed or edited.
    """
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
    permission_classes = [permissions.IsAuthenticated]

class InvestmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows investments to be viewed or edited.
    """
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail =False, methods=['post'], name='Create Investment')
    def invest(self, request, **kwargs):
            # request.data is from the POST object. We want to take these
            # values and supplement it with the user.id that's defined
            # in our URL parameter
            data = {
                'investor': request.data['investor'],
                'request': request.data['request'],
                'amount': request.data['amount']
            }

            loanrequest = LoanRequest.objects.filter(id=data['request']).first()

            d = decimal.Decimal(data['amount'])

            if d + loanrequest.current_amount <= loanrequest.amount :

                serializer = InvestmentSerializer(data=data)

                if serializer.is_valid():

                    novovalor = loanrequest.current_amount + d
                    setattr(loanrequest, 'current_amount', novovalor)
                    loanrequest.save()

                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else: return Response({"Quantidade inválida"}, status=status.HTTP_400_BAD_REQUEST)
            
            


class LoanRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows loan requests to be viewed or edited.
    """
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [permissions.IsAuthenticated]