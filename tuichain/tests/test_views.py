from django.test import TestCase
from django.urls import reverse

from tuichain.api.models import Profile, IDVerifications, LoanRequest, Investmentor

class ProfileViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create 10 profiles for pagination tests
        number_of_profiles = 15

        for profile_id in range(number_of_profiles):
            Profile.objects.create(
                user=f'test {profile_id}',
                full_name='test user',
                birth_date='1998-01-01',
                address='test street',
                zip_code='1000-000',
                city='test city',
                country='test country',
                id_number=f'{profile_id}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('api/users/get/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_id(self):
        response = self.client.get('api/users/get/10/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_acessible_all(self):
        response = self.client.get('api/users/get_all/')
        self.assertEqual(response.status_code, 200)

# doubt nesta
    def test_view_url_acessible_update(self):
        response = self.client.get('api/users/update_profile/')
        self.assertEqual(response.status_code, 200)
    
# class LoanRequestsViewTest(TestCase):
# class ExternalViewTest(TestCase):
# class AuthViewTest(TestCase):

class InvestmentViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create 10 profiles for pagination tests
        number_of_investments = 15

        for investment_id in range(number_of_investments):
            Investment.objects.create(
                id=f'{investment_id}',
                investor=f'{investment_id}',
                request=f'{investment_id}',
                amount='500'
                active='True'
            )

    def test_view_url_accessible_me(self):
        response = self.client.get('api/investments/get_personal/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_id(self):
        response = self.client.get('api/investments/get/10/')
        self.assertEqual(response.status_code, 200)

# doubt nesta
    def test_view_url_acessible_new(self):
        response = self.client.get('api/investments/new/')
        self.assertEqual(response.status_code, 200)
