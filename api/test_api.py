from django.test import TestCase, Client
from django.urls import reverse
import json


class SummarizeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/summarize'
    
    def test_get_method_not_allowed(self):
        """Test that GET requests return 405 Method Not Allowed"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'POST method required.')
    
    def test_empty_file_content(self):
        """Test that empty fileContent returns 400 Bad Request"""
        response = self.client.post(
            self.url,
            json.dumps({'fileContent': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'fileContent cannot be empty.')
    
    def test_invalid_json(self):
        """Test that invalid JSON returns 400 Bad Request"""
        response = self.client.post(
            self.url,
            'invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Invalid JSON format in request body.')
    
    def test_url_pattern_exists(self):
        """Test that the URL pattern exists and is properly configured"""
        from django.urls import reverse, NoReverseMatch
        
        # Test that the URL exists
        try:
            url = reverse('summarize')
            self.assertTrue(url.endswith('/api/v1/summarize'))
        except NoReverseMatch:
            self.fail("URL pattern 'summarize' not found")