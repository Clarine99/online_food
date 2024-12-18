from django.test import TestCase, SimpleTestCase

from django.urls import reverse

class HomepageTest(SimpleTestCase):

    def test_url_exist_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

# Create your tests here.

