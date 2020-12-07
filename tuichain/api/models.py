from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    id_number = models.IntegerField(blank=True)

    def __str__(self): 
         return self.full_name

class LoanRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    school = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    current_amount = models.DecimalField(editable=False, max_digits=8, decimal_places=2, default='0.00')
    validated = models.BooleanField(editable=False,default=False)

    def __str__(self): 
         return self.course + " by " + self.school + " from " + self.student.full_name

class Investment(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    investment_date = models.DateTimeField(auto_now_add=True)

    
