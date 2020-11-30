from django.db import models

# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    email = models.EmailField()
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    id_number = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
         return self.full_name


class LoanRequest(models.Model):
    request_date = models.DateTimeField(auto_now_add=True)
    school = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    current_amount = models.DecimalField(editable=False, max_digits=8, decimal_places=2, default='0.00')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    validated = models.BooleanField(editable=False,default=False)

    def __str__(self): 
         return self.course + " na " + self.school + " do " + self.student.full_name


class Investor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    email = models.EmailField()
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
         return self.full_name

class Investment(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    investment_date = models.DateTimeField(auto_now_add=True)

    
