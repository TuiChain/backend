from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tuichain.api.serializers import InvestmentSerializer, LoanRequestSerializer
from tuichain.api.models import Investment, LoanRequest
import decimal

class LoanRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows loan requests to be viewed or edited.
    """
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
