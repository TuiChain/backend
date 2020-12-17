from django.test import TestCase
from tuichain.api.models import Profile, IDVerifications, LoanRequest, Investment
from datetime import datetime


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Profile.objects.create(
            user='test',
            full_name='test user',
            birth_date='1998-01-01',
            address='test street',
            zip_code='1000-000',
            city='test city',
            country='test country',
            id_number='10'
        )
    
    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'test')
    
    def test_full_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'test user')
    
    def test_birth_date_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('birth_date').verbose_name
        self.assertEqual(field_label, 'test')
    
    def test_address_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('address').verbose_name
        self.assertEqual(field_label, '1998-01-01')
    
    def test_zip_code_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('zip_code').verbose_name
        self.assertEqual(field_label, '1000-000')
    
    def test_city_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('city').verbose_name
        self.assertEqual(field_label, 'test city')

    def test_country_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('country').verbose_name
        self.assertEqual(field_label, 'test country')

    def test_id_number_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('id_number').verbose_name
        self.assertEqual(field_label, '10')


class IDVerificationsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        IDVerifications.objects.create(
            user='test',
            verification_id='1'
            person_id='1'
            validated='False'
        )
    
    def test_user_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'test')
    
    def test_verification_id_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('verification_id').verbose_name
        self.assertEqual(field_label, '1')
    
    def test_person_id_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('person_id').verbose_name
        self.assertEqual(field_label, '1')
    
    def test_validated_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('validated').verbose_name
        self.assertEqual(field_label, 'False')


class LoanRequestModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        LoanRequest.objects.create(
            id='1',
            student='1',
            request_date=datetime.now(),
            school='test school'
            course='test course'
            amount='1000'
            validated='False'
            active='True'
        )
    
    def test_id_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('id').verbose_name
        self.assertEqual(field_label, '1')
    
    def test_student_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('student').verbose_name
        self.assertEqual(field_label, '1')
    
    def test_request_date_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('request_date').verbose_name
        self.assertEqual(field_label, datetime.now())

    def test_school_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('school').verbose_name
        self.assertEqual(field_label, 'test school')
    
    def test_course_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('course').verbose_name
        self.assertEqual(field_label, 'test course')

    def test_amount_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('amount').verbose_name
        self.assertEqual(field_label, '1000')

    def test_validated_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('validated').verbose_name
        self.assertEqual(field_label, 'False')

    def test_active_label(self):
        idverifications = Profile.objects.get(id=1)
        field_label = idverifications._meta.get_field('active').verbose_name
        self.assertEqual(field_label, 'True')