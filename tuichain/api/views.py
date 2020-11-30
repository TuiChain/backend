from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from tuichain.api.serializers import StudentSerializer, InvestorSerializer, InvestmentSerializer, LoanRequestSerializer
from tuichain.api.models import Student, Investor, Investment, LoanRequest


# Create your views here.

class StudentView(APIView):
    
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response({"students": serializer.data})

    def post(self, request):
        student = request.data.get('student')

        serializer = StudentSerializer(data=student)
        if serializer.is_valid(raise_exception=True):
            student_saved = serializer.save()
        return Response({"sucess": "Student '{}' created sucessfully".format(student_saved.full_name)})

    def put(self, request, pk):
        saved_student = get_object_or_404(Student.objects.all(), pk=pk)
        data = request.data.get('student')

        serializer = StudentSerializer(instance=saved_student, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_student = serializer.save()
        return Response({"success": "Student '{}' updated successfully".format(saved_student.full_name)})

    def delete(self, request, pk):
        student=get_object_or_404(Student.objects.all(), pk=pk)
        student.delete()
        return Response({"message": "Student with id `{}` has been deleted.".format(pk)}, status=204)


class InvestorView(APIView):
    
    def get(self, request):
        investors = Investor.objects.all()
        serializer = InvestorSerializer(investors, many=True)
        return Response({"investors": serializer.data})

    def post(self, request):
        investor = request.data.get('investor')

        serializer = InvestorSerializer(data=investor)
        if serializer.is_valid(raise_exception=True):
            investor_saved = serializer.save()
        return Response({"sucess": "Investor '{}' created sucessfully".format(investor_saved.full_name)})

    def put(self, request, pk):
        saved_investor = get_object_or_404(Investor.objects.all(), pk=pk)
        data = request.data.get('investor')

        serializer = InvestorSerializer(instance=saved_investor, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_investor = serializer.save()
        return Response({"success": "Investor '{}' updated successfully".format(saved_investor.full_name)})

    def delete(self, request, pk):
        investor=get_object_or_404(Investor.objects.all(), pk=pk)
        investor.delete()
        return Response({"message": "Investor with id `{}` has been deleted.".format(pk)}, status=204)

class InvestmentView(APIView):

    def get(self, request):
        investments = Investment.objects.all()
        serializer = InvestmentSerializer(investments, many=True)
        return Response({"investments": serializer.data})

    def post(self, request):
        investment = request.data.get('investment')

        serializer = InvestmentSerializer(data=investment)
        if serializer.is_valid(raise_exception=True):
            investment_saved = serializer.save()
        return Response({"sucess": "Investment '{}' created sucessfully".format(investment_saved.investor)})

    def put(self, request, pk):
        saved_investment = get_object_or_404(Investment.objects.all(), pk=pk)
        data = request.data.get('investment')

        serializer = InvestmentSerializer(instance=saved_investment, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_investment = serializer.save()
        return Response({"success": "Investment '{}' updated successfully".format(saved_investment.title)})

    def delete(self, request, pk):
        investment=get_object_or_404(Investment.objects.all(), pk=pk)
        investment.delete()
        return Response({"message": "Investment with id `{}` has been deleted.".format(pk)}, status=204)

class LoanRequestView(APIView):
    
    def get(self, request):
        loanrequests = LoanRequest.objects.all()
        serializer = LoanRequestSerializer(loanrequests, many=True)
        return Response({"loanrequests": serializer.data})

    def post(self, request):
        loanrequest = request.data.get('loanrequest')

        serializer = LoanRequestSerializer(data=loanrequest)
        if serializer.is_valid(raise_exception=True):
            loanrequest_saved = serializer.save()
        return Response({"sucess": "Loan Request '{}' created sucessfully".format(loanrequest_saved.course)})

    def put(self, request, pk):
        saved_loanrequest = get_object_or_404(LoanRequest.objects.all(), pk=pk)
        data = request.data.get('loanrequests')

        serializer = LoanRequestSerializer(instance=saved_loanrequest, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_loanrequest = serializer.save()
        return Response({"success": "Loan Request '{}' updated successfully".format(saved_loanrequest.course)})

    def delete(self, request, pk):
        loanrequest=get_object_or_404(LoanRequest.objects.all(), pk=pk)
        loanrequest.delete()
        return Response({"message": "Loan Request with id `{}` has been deleted.".format(pk)}, status=204)
