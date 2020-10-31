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
    creation_date = models.DateTimeField()


class LoanRequest(models.Model):
    request_date = models.DateTimeField()
    school = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    amount = models.DecimalField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    validated = models.BooleanField()


class Investor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    email = models.EmailField()
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    creation_date = models.DateTimeField()


class Investment(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    amount = models.DecimalField()
    investment_date = models.DateTimeField()
