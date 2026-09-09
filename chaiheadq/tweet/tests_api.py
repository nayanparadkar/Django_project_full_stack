from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from .models import Tweet


class TweetAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='apipass')
        self.client = APIClient()

    def test_list_public(self):
        Tweet.objects.create(user=self.user, content='public')
        resp = self.client.get('/api/tweets/')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list)

    def test_create_requires_auth(self):
        resp = self.client.post('/api/tweets/', {'content': 'no auth'})
        self.assertEqual(resp.status_code, 403)

    def test_create_authenticated(self):
        self.client.login(username='apiuser', password='apipass')
        resp = self.client.post('/api/tweets/', {'content': 'with auth'})
        self.assertIn(resp.status_code, (201, 302, 200))
        # ensure created
        self.assertTrue(Tweet.objects.filter(content='with auth').exists())
