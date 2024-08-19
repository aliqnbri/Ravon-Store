from django.shortcuts import render
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


def user_context_processor(request):
    jwt_token = request.COOKIES.get('access_token')
    if jwt_token:
        try:
            payload = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            return {'user': user}
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return {}
        except jwt.InvalidTokenError:
            # Handle invalid token
            return {}
    return {}

# Create your views here.


def home(request):
    context = user_context_processor(request)
    return render(request, 'index.html', context=context)
