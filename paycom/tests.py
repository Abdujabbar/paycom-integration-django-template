from django.test import TestCase
from django.test.client import Client
import requests
# Create your tests here.
class PaycomTest(TestCase):

    def test_authentication(self):
        headers = {"Authorization": "Basic UGF5Y29tOlF3SFpWMjJFaHBIeHNVOXo2anpFdzdwMjNrP2h6QUJTdFY5Tg=="}
        pass