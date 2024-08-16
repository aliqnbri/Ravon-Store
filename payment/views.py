from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# Create your views here.
from order.models import Order
from django.conf import settings
from django.http.response import JsonResponse
import requests
import json
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required

class CallBackTemplateView(TemplateView):
    template_name = 'callback.html'

def send_request(request,order_id):
    callbackURL = 'http://localhost:80/zarinpal/callback/'
    order = Order.objects.get(id = order_id)
    phone = order.customer.phone
    amount = int(order.get_total_cost())
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "phone" : phone,
        "CallbackURL": callbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)
        print(response)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                order.payment_id = response['Authority']
                order.save()
                data = {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                res = JsonResponse(data)
                res.set_cookie(key='order',value=response['Authority'],max_age=300,)
                # res.data = json.dumps(data)
                return res
            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return response
    
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(request):
    if request.COOKIES.get('order') != None:
        order = Order.objects.get(payment_id = request.COOKIES.get('order'))
        amount = int(order.get_total_cost())
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Authority": request.COOKIES.get('order'),
        }
        
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            print(response)
            if response['Status'] == 100:

                order.status = 'PA'
                order.ref_id = response['RefID']
                order.save()
                return JsonResponse({'status': True, 'RefID': response['RefID']})
            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return response
    
    return JsonResponse(data = '' ,status= HTTP_403_FORBIDDEN,safe=False)