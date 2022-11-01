from django.test import TestCase, Client
from django.urls import reverse
from LegacySite.models import *
from LegacySite.views import *
from django.http import HttpRequest
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