from .merchant import Merchant

class MerchantFactory(object):
    @staticmethod
    def create_merchant(request):
        return Merchant(request)