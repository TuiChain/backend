from rest_framework import viewsets
from rest_framework import permissions
from tuichain.api.serializers import StudentSerializer, InvestorSerializer, InvestmentSerializer, LoanRequestSerializer
from tuichain.api.models import Student, Investor, Investment, LoanRequest

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

class InvestmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows investments to be viewed or edited.
    """
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoanRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows loan requests to be viewed or edited.
    """
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [permissions.IsAuthenticated]