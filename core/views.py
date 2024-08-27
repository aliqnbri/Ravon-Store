from django.shortcuts import render
import jwt
from django.conf import settings
from account.utils import user_context_processor


# Create your views here.


def home(request):
    context = user_context_processor(request)
    return render(request, 'index.html', context=context)
