from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.conf import settings
import jwt
import random
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import verify,User,Token
from .forms import UserSignupForm,UserLoginForm,UserVerifyForm,UserPasswordForm
# Create your views here.

@api_view(['POST'])
def signup(request):
    template=loader.get_template('signup.html')
    if request.method =='POST':
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        userExist=User.objects.filter(email=email)
        if not (username and email and phone):
          return JsonResponse({'error': 'Missing userdata.'},status=400)
        if(userExist):
          return JsonResponse({'error': 'User already Existed.'},status=400)
        data = User(
            username=username,
            email=email,
            password='',
            phone=phone,
            # Set other fields as needed
        )
        data.save()
        new_verify=verify(
            email=email,
            verification_code=code,
            expire_at=timezone.now() + timedelta(minutes=5)
        )
        new_verify.save()
        send_mail(
            "Your Verification Code",
            f'Hi {username}, Your verification code is: {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        return JsonResponse({'message': 'UserData saved successfully'},status=200)
    return HttpResponse(template.render())

@api_view(['POST'])
def verifyemail(request):
    template=loader.get_template('verifyemail.html')
    if request.method == 'POST':
       email = request.data.get('email', None)
       verification_code = request.data.get('verification_code', None)
       if verify.objects.filter(email=email).exists():
           existing_verification_code= verify.objects.get(email=email)
           if(existing_verification_code.verification_code == verification_code and timezone.now() < existing_verification_code.expire_at):
              existing_verification_code.delete()
              return JsonResponse({"message":"success verified"})
           return JsonResponse({"message":"invaild verification code"})
       return JsonResponse({"message":"user does not exist"})
    return HttpResponse(template.render())

@api_view(['POST'])
def setpassword(request):
    template=loader.get_template('setpassword.html')
    if request.method == 'POST':
       username = request.data.get('username', None)
       password = request.data.get('password', None)
       if User.objects.filter(username=username).exists():
         current_user=User.objects.get(username=username)
         hashed_password = make_password(password)
         current_user.password=hashed_password
         current_user.save()
         return JsonResponse({"message":"success set password"})
       return JsonResponse({"message":"user does not exist"})
    return HttpResponse(template.render())

@api_view(['POST'])
def login(request):
    template=loader.get_template('login.html')
    if request.method == 'POST':
        email=request.data.get('email',None)
        password=request.data.get('password',None)
        credentials={
            'email':email,
            'password':password
        }
        userExist=User.objects.get(email=email)
        if not (email and password):
          return JsonResponse({'error': 'Missing userdata.'},status=400)
        if check_password(password,userExist.password):
            accesstoken=jwt.encode(credentials,settings.ASECRET_KEY,algorithm="HS256")
            refreshtoken=jwt.encode(credentials,settings.RSECRET_KEY,algorithm="HS256")
            data=Token(
              accesstoken=accesstoken,
              refreshtoken=refreshtoken
            )
            data.save()
            return JsonResponse({'success': 'Login Successfully!!!', 'tokencreate':'token created successfully','accesstoken':accesstoken,'refreshtoken':refreshtoken},status=200)
        else:
          return JsonResponse({'error': 'password invalid.'},status=400)
    return HttpResponse(template.render())

def dashboard(request):
    template=loader.get_template('dashboard.html')
    return HttpResponse(template.render())