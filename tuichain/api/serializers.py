from rest_framework import serializers
from tuichain.api.models import Student, Investor, Investment, LoanRequest

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name',
                'last_name',
                'full_name',
                'birth_date',
                'email',
                'country',
                'address',
                'id_number')

    def create(self, validated_data):
        return Student.objects.create(**validated_data)


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ('first_name',
                'last_name',
                'full_name',
                'birth_date',
                'email',
                'country',
                'address')

    def create(self, validated_data):
        return Investor.objects.create(**validated_data)

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ('school',
                'course',
                'amount',
                'student')

    def create(self, validated_data):
        return LoanRequest.objects.create(**validated_data)

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ('investor',
                'request',
                'amount')
    
    def create(self, validated_data):
        return Investment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.investor = validated_data.get('investor', instance.investor)
        instance.request = validated_data.get('request', instance.request)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.investment_date = validated_data.get('investment_date', instance.investment_date)

        instance.save()
        return instance