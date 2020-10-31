from django.contrib import admin
from .models import Student, Investor, LoanRequest, Investment

# Register your models here.
admin.site.register(Student)
admin.site.register(Investor)
admin.site.register(LoanRequest)
admin.site.register(Investment)
