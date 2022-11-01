from django.test import TestCase,Client

# Create your tests here.
class MyTestCase(TestCase):
    def test_xss(self):
        payload = "<script>alert('XSS Vulnerability Found')</script>"
        params = {'director': payload}
        response = self.client.get('/buy.html', params)
        #self.assertEqual(response.context.get('director', None), payload)
        print(response)
        print(response.context)
        self.assertEqual(response, payload)
