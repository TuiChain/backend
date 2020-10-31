from rest_framework import serializers
from .models import Student, Investor, LoanRequest, Investment

# Serializers allow complex data such as querysets and model instances to be converted to native
# Python datatypes that can then be easily rendered into JSON, XML or other content types.
# Serializers also provide deserialization, allowing parsed data to be converted back into complex types,
# after first validating the incoming data.


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor


class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
