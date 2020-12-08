from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    id_number = models.IntegerField(null=True, blank=True)

    def to_dict(self, private=False):
        result = {
            'full_name': self.full_name,
            'country': self.country
        }

        if private:
            setattr(result, 'birth_date', self.birth_date)
            setattr(result, 'address', self.address)
            setattr(result, 'zip_code', self.zip_code)
            setattr(result, 'city', self.city)
            setattr(result, 'id_number', self.id_number)

        return result

    def __str__(self): 
         return self.full_name

class LoanRequest(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    school = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    current_amount = models.DecimalField(max_digits=8, decimal_places=2, default='0.00')
    validated = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'student': self.student.id,
            'request_date': self.request_date,
            'school': self.school,
            'course': self.course,
            'amount': self.amount,
            'current_amount': self.current_amount,
            'validated': self.validated,
            'active': self.active
        }

    def __str__(self): 
         return self.course + " by " + self.school + " from " + self.student.full_name

class Investment(models.Model):
    id = models.AutoField(primary_key=True)
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    investment_date = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'investor': self.investor.id,
            'request': self.request.id,
            'amount': self.amount,
            'investment_date': self.investment_date
        }


# SIGNALS

# Create Auth token automatically when a User is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    print('SIGNAL: create auth token')
    if created:
        Token.objects.create(user=instance)

# Create and Save User Profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print('SIGNAL: create user profile')
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('SIGNAL: save user profile')
    instance.profile.save()

    
