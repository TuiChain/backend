from rest_framework import serializers
from tuichain.api.models import Investment, Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"
