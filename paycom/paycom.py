from .factory import MerchantFactory
import json
class Paycom(object):

    def __init__(self, request):
        self.merchant = MerchantFactory.create_merchant(request)
        self.params = json.loads(request.body.decode('utf-8'))


    def authorize(self):
        self.merchant.authorize()


    def check_perform_transaction(self):
        pass

    def create_transaction(self):
        pass

    def perform_transaction(self):
        pass

    def cancel_transaction(self):
        pass

    def check_transaction(self):
        pass

    def get_statement(self):
        pass

    def change_password(self):
        pass