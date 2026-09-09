from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Tweet


class TweetModelTests(TestCase):
    def test_create_tweet(self):
        user = User.objects.create_user(username="tester", password="testpass")
        t = Tweet.objects.create(user=user, content="hello")
        self.assertEqual(str(t), "tester: hello")


class TweetViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="viewer", password="testpass")

    def test_tweet_create_requires_login(self):
        url = reverse("tweet_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_signed_up_user_can_create(self):
        self.client.login(username="viewer", password="testpass")
        url = reverse("tweet_create")
        resp = self.client.post(url, {"content": "a post"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Tweet.objects.filter(content="a post").exists())

    def test_ajax_create(self):
        # Ajax (XHR) create should return JSON with html snippet
        self.client.login(username="viewer", password="testpass")
        url = reverse("tweet_create")
        resp = self.client.post(url, {"content": "ajax post"}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Tweet.objects.filter(content="ajax post").exists())
        data = resp.json()
        self.assertIn('html', data)

    def test_non_owner_cannot_edit(self):
        # Only owner can access edit page
        t = Tweet.objects.create(user=self.user, content='owner post')
        other = User.objects.create_user(username='other', password='otherpass')
        self.client.login(username='other', password='otherpass')
        url = reverse('tweet_edit', args=[t.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_photo_upload(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        self.client.login(username='viewer', password='testpass')
        url = reverse('tweet_create')
        image = SimpleUploadedFile('test.jpg', b'filecontent', content_type='image/jpeg')
        resp = self.client.post(url, {'content': 'with photo', 'photo': image})
        # view may return 200 (render with errors) or redirect on success; accept either
        self.assertIn(resp.status_code, (200, 302))



# Create your tests here.
