from django.test import TestCase, Client
from django.urls import reverse
from LegacySite.models import *
from LegacySite.views import *
from django.http import HttpRequest
import io


class TestResponse(TestCase):
	def test_password_salt(self):
		self.client.post(reverse('Register'), {'uname': 'testuser2', 'pword': 'password1', 'pword2': 'password1'})
		self.client.post(reverse('Register'), {'uname': 'admin1', 'pword': 'password1', 'pword2': 'password1'})
		self.client.post(reverse('Login'), {'uname': 'testuser2', 'pword': 'password1'})
		data = io.StringIO('{"merchant_id": "NYU Apparel Card", "customer_id": "test", "total_value": "1000", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": " \' union SELECT password from LegacySite_user where username = \'testuser2"}]}')
		filename="sqlInjection.gftcrd"
		response = self.client.post(reverse('Use a card'), {'card_data': data, 'filename' :filename, 'card_supplied': True, 'card_fname': 'test'},)
		saltedpassword1=response.context.get('card_found', None)
		print(saltedpassword1)
		self.client.post(reverse('Login'), {'uname': 'admin1', 'pword': 'password1'})
		data = io.StringIO('{"merchant_id": "NYU Apparel Card", "customer_id": "test", "total_value": "1000", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": " \' union SELECT password from LegacySite_user where username = \'admin1"}]}')
		filename="sqlInjection.gftcrd"
		response = self.client.post(reverse('Use a card'), {'card_data': data, 'filename' :filename, 'card_supplied': True, 'card_fname': 'test'},)
		saltedpassword2=response.context.get('card_found', None)
		print(saltedpassword2)
		assert(saltedpassword1 != saltedpassword2)
