from django.test import TestCase
from django.test.client import Client
from .exceptions import PaycomException
import json
from orders.models import Order


# Create your tests here.
class PaycomTest(TestCase):
    base_url = "http://localhost:8000/api/payments/paycom"

    def setUp(self):
        credentials = "Basic UGF5Y29tOlF3SFpWMjJFaHBIeHNVOXo2anpFdzdwMjNrP2h6QUJTdFY5Tg=="
        self.client.defaults["HTTP_AUTHORIZATION"] = credentials

    @classmethod
    def create_default_order(cls, state=Order.ORDER_ON_WAIT):
        order = Order()
        order.state = state
        order.amount = 50000
        order.product_ids = '1,2,3'
        order.user_id = 1
        order.phone = '935820828'
        order.save()
        return order

    def test_unauthenticated(self):
        self.client.defaults["HTTP_AUTHORIZATION"] = ""
        res = self.client.post(self.base_url,
                               content_type="raw",
                               data='{"id": 1}')
        received = json.loads(res.content)
        self.assertEqual(received["error"]["code"], PaycomException.ERRORS_CODES["UNAUTHENTICATED"])

    def test_check_perform_transaction(self):
        expected = {
            "result": {
                "allow": True,
            }
        }

        order = self.create_default_order()

        body = {
            "method": "CheckPerformTransaction",
            "params": {
                "amount": order.amount,
                "account": {
                    "phone": order.phone,
                    "order_id": order.pk,
                }
            }
        }
        res = self.client.post(self.base_url,
                               content_type="raw",
                               data=json.dumps(body))

        received = json.loads(res.content)

        self.assertEqual(expected, received)

    def test_order_not_exists_exception(self):
        exception = PaycomException("ORDER_NOT_FOUND")
        expected = {
            "result": "",
            "error": {
                "code": exception.ERRORS_CODES[exception.code],
                "message": exception.message,
                "data": "",
            },
        }
        body = {
            "method": "CheckPerformTransaction",
            "params": {
                "amount": 50000,
                "account": {
                    "phone": '935820828',
                    "order_id": -1,
                }
            }
        }

        res = self.client.post(self.base_url, content_type="raw", data=json.dumps(body))

        received = json.loads(res.content)
        self.assertEqual(expected, received)

    def test_order_already_payed_exception(self):
        exception = PaycomException("ORDER_ALREADY_PAYED")
        expected = {
            "result": "",
            "error": {
                "code": exception.ERRORS_CODES[exception.code],
                "message": exception.message,
                "data": "",
            },
        }

        order = self.create_default_order(Order.ORDER_IS_PAYED)

        body = {
            "method": "CheckPerformTransaction",
            "params": {
                "amount": 50000,
                "account": {
                    "phone": "935820828",
                    "order_id": order.pk,
                }
            }
        }

        res = self.client.post(self.base_url, content_type="raw", data=json.dumps(body))
        received = json.loads(res.content)
        self.assertEqual(expected, received)

    def test_order_cancelled_exception(self):
        exception = PaycomException("ORDER_CANCELLED")
        expected = {
            "result": "",
            "error": {
                "code": exception.ERRORS_CODES[exception.code],
                "message": exception.message,
                "data": "",
            },
        }

        order = self.create_default_order(Order.ORDER_CANCELLED)

        body = {
            "method": "CheckPerformTransaction",
            "params": {
                "amount": 50000,
                "account": {
                    "phone": "935820828",
                    "order_id": order.pk,
                }
            }
        }

        res = self.client.post(self.base_url, content_type="raw", data=json.dumps(body))

        received = json.loads(res.content)

        self.assertEqual(expected, received)


