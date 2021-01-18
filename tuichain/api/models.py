from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from tuichain.api.enums import LoanState


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    full_name = models.CharField(max_length=200, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    short_bio = models.CharField(max_length=500, null=True, blank=True)
    profile_image = models.FileField(
        upload_to="media/photos", null=True, blank=True
    )
    id_number = models.IntegerField(null=True, blank=True)

    def to_dict(self, private=False):
        img_url = ""

        # if self.profile_image is not None:
        #     img_url = self.profile_image.url

        result = {
            "id": self.user.id,
            "username": self.user.username,
            "full_name": self.full_name,
            "created_at": self.user.date_joined,
            "is_active": self.user.is_active,
            "country": self.country,
            "short_bio": self.short_bio,
            "profile_image": img_url,
        }

        if private:
            result["birth_date"] = self.birth_date
            result["address"] = self.address
            result["zip_code"] = self.zip_code
            result["city"] = self.city
            result["id_number"] = self.id_number

        return result


class IDVerifications(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="id_verification"
    )
    verification_id = models.CharField(max_length=100, null=True, blank=True)
    person_id = models.CharField(max_length=100, null=True, blank=True)
    validated = models.BooleanField(default=False)


class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    school = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    requested_value_atto_dai = models.CharField(max_length=40)
    description = models.CharField(max_length=5000)
    state = models.IntegerField(default=LoanState.PENDING.value)
    recipient_address = models.CharField(max_length=42)
    identifier = models.CharField(max_length=42, null=True, blank=True)

    def to_dict(self):
        return {
            "id": self.id,
            "student": self.student.id,
            "request_date": self.request_date,
            "school": self.school,
            "course": self.course,
            "destination": self.destination,
            "requested_value_atto_dai": self.requested_value_atto_dai,
            "description": self.description,
            "state": str(LoanState(self.state)),
            "recipient_address": self.recipient_address,
            "identifier": self.identifier,
        }


# SIGNALS

# Create Auth token automatically when a User is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    print("SIGNAL: create auth token")
    if created:
        Token.objects.create(user=instance)


# Create and Save User Profile and ID Verification when a User is created
@receiver(post_save, sender=User)
def create_user_profile_idverification(sender, instance, created, **kwargs):
    # print('SIGNAL: create user profile')
    if created:
        Profile.objects.create(user=instance)
        IDVerifications.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile_idverification(sender, instance, **kwargs):
    # print('SIGNAL: save user profile')
    instance.profile.save()
    instance.id_verification.save()
