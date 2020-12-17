from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from tuichain.api.serializers import StudentSerializer, InvestorSerializer, InvestmentSerializer, LoanRequestSerializer
from tuichain.api.models import Student, Investor, Investment, LoanRequest

# Create your tests here.
