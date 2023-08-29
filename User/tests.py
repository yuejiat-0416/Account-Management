from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template import RequestContext
from django.utils import timezone
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from allauth.account.adapter import get_adapter

class TestUserLogin(TestCase):
    # register user
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testusername1', password='wocaonima', email='testusername1@example.com')

        # Create a fake request
        request = self.client.get('/').wsgi_request

        # Associate it with the user
        request.user = self.user

        email_address = EmailAddress.objects.create(user=self.user, email='testusername1@example.com', primary=True, verified=True)

        
        get_adapter().stash_verified_email(request, email_address.email)
        email_confirmation = EmailConfirmation.create(email_address)
        email_confirmation.sent = timezone.now()
        email_confirmation.save()

        self.confirmation_key = EmailConfirmationHMAC(email_confirmation).key

    def test_dashboard_access_without_login(self):
        print('Test1: Dashboard access without login')
        response = self.client.get(reverse('homepage'), follow=True)
        print(f"Status code: {response.status_code}")
        if hasattr(response, 'url'):  # Check if response object has url attribute
            print(f"Redirected to: {response.url}")
        self.assertRedirects(response, '/accounts/login/?next=%2Fdashboard')

        
    def test_login_success(self):
        print('')
        print('Test 2: login success')
        # Confirm the email
        confirmation_response = self.client.post('/accounts/confirm-email/' + self.confirmation_key, follow=True)
        print("Confirmation response:", confirmation_response)

        login_data = {
            'login': 'testusername1',
            'password': 'wocaonima',
        }

        response = self.client.post(reverse('account_login'), data=login_data, follow=True)
        print(f"User is authenticated: {self.user.is_authenticated}")
        print(f"Status code: {response.status_code}")
        if hasattr(response, 'url'):  # Check if response object has url attribute
            print(f"Redirected to: {response.url}")
        self.assertRedirects(response, reverse('homepage'))



