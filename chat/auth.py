from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from .models import  Customer




@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginUser(request):
    phonenumber = request.data.get("username")
    password = request.data.get("password")

    buyer = Customer.objects.filter(phone_number= phonenumber).first()
    username = buyer.username
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)

    if not user:
        context = {
            'error': 'Invalid Username or Password',
        }
        return Response(context, status=status.HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    context = {
        'token': token.key,
        'id': user.id,
        'username': username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number' : phonenumber,
    }
    return Response(context,
                    status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def registerUser(request):

    phonenumber = request.data.get("number")
    password = request.data.get("password")
    email = request.data.get("email")
    id_number = request.data.get("id_number")
    name = request.data.get("name")

    if name is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = Customer.objects.filter(username = name).first()

    if user:
        return Response({'error': 'Username already exists'}, status=status.HTTP_403_FORBIDDEN)

    user = Customer()
    user.username = name
    user.phone_number = phonenumber
    user.email = email
    user.id_number = id_number
    user.set_password(password)
    user.is_staff = False
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    context = {
        'token': token.key,
        'id': user.id,
        'username': name,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number' : phonenumber,
        'address' : user.address
    }

    return Response(context,
                    status=status.HTTP_200_OK)


def getToken(request):
    r_token = request.META['HTTP_AUTHORIZATION']

    return r_token.split(' ', 1)[1] 