from django.test import TestCase
from api.models import Profile, IDVerifications, LoanRequest, Investment


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
       Profile.objects.create(
            user='test',
            full_name='test user',
            birth_date='1998-01-01',
            address='test street',
            zip_code='1000-000'
            city='test city',
            country='test country'
            id_number='10'
        )
    
    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = author._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'test')
    
    def test_full_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = author._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'test user')
    
    def test_birth_date_label(self):
        profile = Profile.objects.get(id=1)
        field_label = author._meta.get_field('birth_date').verbose_name
        self.assertEqual(field_label, 'test')
    
    def test_address_label(self):
        profile = Profile.objects.get(id=1)
        field_label = author._meta.get_field('address').verbose_name
        self.assertEqual(field_label, '1998-01-01')
    
    def test_zip_code_label(self):
        profile = Profile.objects.get(id=1)
        field_label = author._meta.get_field('zip_code').verbose_name
        self.assertEqual(field_label, '1000-000')
    
    def test_city_label(self):
        profile = Profile.objects.get(id=1)
        field_label = author._meta.get_field('city').verbose_name
        self.assertEqual(field_label, 'test city')

    def test_country_label(self):
        profile = Profile.objects.get(id=1)
        field_label = author._meta.get_field('country').verbose_name
        self.assertEqual(field_label, 'test country')

    def test_id_number_label(self):
        profile = Profile.objects.get(id=1)
        field_label = author._meta.get_field('id_number').verbose_name
        self.assertEqual(field_label, '10')