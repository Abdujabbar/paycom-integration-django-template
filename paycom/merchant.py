from django.conf import settings
from .exceptions import PaycomException
import base64
class Merchant(object):
    key = ""
    login = ""
    request = False
    def __init__(self, request):
        self.key = settings.PAYCOM_API_KEY
        self.login  = settings.PAYCOM_API_LOGIN
        self.request = request

    def authorize(self):

        if not 'HTTP_AUTHORIZATION' in self.request.META:
            raise PaycomException()

        basic = self.request.META['HTTP_AUTHORIZATION']
        password = str(basic.replace("Basic", "")).strip()
        decoded = base64.b64decode(password)

        if self.generate_pair_login_pass().encode() != decoded:
            raise PaycomException()

        return True

    def generate_pair_login_pass(self):
        return self.login + ":" + self.key