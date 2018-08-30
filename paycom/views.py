from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .paycom import Paycom
from .exceptions import PaycomException
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# Create your views here.
@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def index(request):
    paycom = Paycom(request)

    try:
        paycom.authorize()

        # available_methods = {
        #     "CheckPerformTransaction":  paycom.check_perform_transaction,
        #     "CreateTransaction":        paycom.create_transaction,
        #     "PerformTransaction":       paycom.perform_transaction,
        #     "CancelTransaction":        paycom.cancel_transaction,
        #     "CheckTransaction":         paycom.check_transaction,
        #     "GetStatement":             paycom.get_statement,
        #     "ChangePassword":           paycom.change_password,
        # }
        #
        # if paycom.params['method'] in available_methods:
        #     available_methods[paycom.params['method']]()
        # else:
        #     raise PaycomException("METHOD_NOT_EXIST")


        if paycom.params['method'] == "CheckPerformTransaction" and paycom.check_perform_transaction():
            return Response({
                "result": {
                    "allow": True
                }
            })
        if paycom.params['method'] == "CreateTransaction":
            transaction = paycom.create_transaction()
            return Response({
                "result": {
                    "created_time": transaction.create_time,
                    "transaction": transaction.transaction,
                    "state": transaction.state,
                }
            })




    except PaycomException as e:
        return Response({
            "id": paycom.params['id'],
            "result": "",
            "error": {
                "code": e.ERRORS_CODES[e.code],
                "message": e.message,
                "data": ""
            }
        })

    return Response({
        "success": True,
    })
