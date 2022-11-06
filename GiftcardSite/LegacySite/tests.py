from django.test import TestCase, Client
from django.urls import reverse
from LegacySite.models import *
from LegacySite.views import *
from django.http import HttpRequest
import io


# Create your tests here.

class TestResponse(TestCase):
	def setup(self):
		self.client= Client()

	def test_xss_gift(self):
		prouct1 = Product.objects.create(product_name = 'test', product_image_path= 'test', recommended_price = 1, description = 'test')
		response = self.client.get('/gift' , {'director' : '<script>alert(''XSS Vulnerability Found'')</script>'})
		#print(response.content)
		#self.assertnotContains(response, "XSS Vulnerability Found")
		#self.assertTrue("XSS Vulnerability Found" in response.content)
		#self.assertIn("XSS Vulnerability Found",response.content)
		self.assertContains(response, "&lt;script&gt;alert(XSS Vulnerability Found)&lt;/script&gt;", status_code=200)

	def test_xss_buy(self):
		prouct1 = Product.objects.create(product_name = 'test', product_image_path= 'test', recommended_price = 1, description = 'test')
		response = self.client.get('/buy' , {'director' : '<script>alert(''XSS Vulnerability Found'')</script>'})
		#print(response.content)
		#self.assertnotContains(response, "XSS Vulnerability Found")
		#self.assertTrue("XSS Vulnerability Found" in response.content)
		self.assertContains(response, "&lt;script&gt;alert(XSS Vulnerability Found)&lt;/script&gt;", status_code=200)
	
	def test_csrf_attack(self):
		#Registered user sending his card to another user
		test = Client(enforce_csrf_checks=True)
		test.post(reverse('Register'), {'uname': 'admin', 'pword': 'password1', 'pword2': 'password1'})
		test.post(reverse('Login'), {'uname': 'testuser1', 'pword': 'password1'})
		Product.objects.create(product_name="Columbia_Apparel Card 2", product_image_path="/images/product_8.jpg",recommended_price="80", description="Stocks")
		data = {'amount': '80', 'username': 'fare'}
		response = test.post("/gift.html", data)
		assert(response.status_code != 200)
		#Non-registered user sending a card to another user 
		test1 = Client(enforce_csrf_checks=True)
		Product.objects.create(product_name="Columbia_Apparel Card 3", product_image_path="/images/product_9.jpg",recommended_price="70", description="Stocks")
		data = {'amount': '70', 'username': 'test'}
		response2 = test1.post("/gift.html", data)
		assert(response2.status_code != 200)

	def test_SQL_Injection(self):
		self.client.post(reverse('Register'), {'uname': 'testuser1', 'pword': 'password1', 'pword2': 'password1'})
		self.client.post(reverse('Register'), {'uname': 'admin', 'pword': 'password1', 'pword2': 'password1'})
		self.client.post(reverse('Login'), {'uname': 'testuser1', 'pword': 'password1'})
        	#User1 = User.objects.create(username='testuser1', password='password1')
        	#self.client.login(username = 'admin', password = password)
		data = io.StringIO('{"merchant_id": "NYU Apparel Card", "customer_id": "test", "total_value": "1000", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": " \' union SELECT password from LegacySite_user where username = \'admin"}]}')
		filename="sqlInjection.gftcrd"
		response = self.client.post(reverse('Use a card'), {'card_data': data, 'filename' :filename, 'card_supplied': True, 'card_fname': 'test'},)
		#print(response.content)
		self.assertEqual(response.context.get('card_found', None), None)


