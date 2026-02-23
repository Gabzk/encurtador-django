from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ShortenedURL

class ShortenedURLModelTest(TestCase):
    def test_create_shortened_url(self):
        """Testa a criação de uma URL encurtada válida"""
        url = ShortenedURL.objects.create(original_url="https://www.example.com")
        self.assertEqual(url.original_url, "https://www.example.com")
        self.assertIsNotNone(url.short_code)
        self.assertGreaterEqual(len(url.short_code), 5) # assumindo código com 5+ caracteres

    def test_original_url_is_required(self):
        """Testa que original_url não pode ser vazio"""
        url = ShortenedURL(original_url="")
        with self.assertRaises(ValidationError):
            url.full_clean()

    def test_short_code_is_unique(self):
        """Testa que os códigos gerados são únicos"""
        url1 = ShortenedURL.objects.create(original_url="https://www.example1.com")
        url2 = ShortenedURL.objects.create(original_url="https://www.example2.com")
        self.assertNotEqual(url1.short_code, url2.short_code)

class ShortenerAPITest(APITestCase):
    def test_create_short_url(self):
        """Testa se a API encurta uma URL corretamente"""
        url = reverse('url-create')
        data = {'original_url': 'https://www.example.com/some/long/path'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_code', response.data)
        self.assertEqual(response.data['original_url'], data['original_url'])

    def test_invalid_url(self):
        """Testa se a API retorna erro quando a URL é inválida"""
        url = reverse('url-create')
        data = {'original_url': 'invalid-url'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RedirectTest(APITestCase):
    def setUp(self):
        self.shortened = ShortenedURL.objects.create(original_url="https://www.example.com")
        
    def test_redirect_to_original_url(self):
        """Testa se acessar o short_code redireciona (302) para a URL original"""
        response = self.client.get(f'/{self.shortened.short_code}')
        self.assertRedirects(response, self.shortened.original_url, status_code=302, fetch_redirect_response=False)

    def test_redirect_invalid_code(self):
        """Testa se acessar um código inexistente retorna 404"""
        response = self.client.get('/invalid123')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
