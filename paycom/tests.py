from django.test import TestCase
from django.test.client import Client
from .exceptions import PaycomException
import requests
import json
# Create your tests here.
class PaycomTest(TestCase):
    base_url = "http://localhost:8000/api/payments/paycom"


    def test_unauthenticated(self):
        headers = {}
        client = Client()
        res = client.post(self.base_url,
                          headers=headers,
                          content_type="raw",
                          data='{"id": 1}')
        response = json.loads(res.content)

        self.assertEqual(response["error"]["code"],  PaycomException.ERRORS_CODES["UNAUTHENTICATED"])

    # def test_check_perform_transaction(self):
    #
    #     expected = {
    #         "result": {
    #             "allow": True,
    #         }
    #     }
    #
    #     headers = {"Authentication": "Basic UGF5Y29tOlF3SFpWMjJFaHBIeHNVOXo2anpFdzdwMjNrP2h6QUJTdFY5Tg=="}
    #
    #     client = Client()
    #
    #     res = client.post(self.base_url, headers = headers, content_type="raw")