from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.

def signup(request):
    if request.method=="POST":  #HTTP 요청이 POST 방식일 때 실행
        if request.POST['password1']==request.POST['password2']:
            from django.contrib.auth.models import User
            user=User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'],
            )
            auth.login(request, user)
            return redirect('board:board') # 네임스페이스:URL 이름   #회원가입이 성공적으로 처리됨, '/'(홈)페이지로 이동
        return render(request,'accounts/signup.html')
    return render(request,'accounts/signup.html')
def signup2(request):
    if request.method=="POST":  #HTTP 요청이 POST 방식일 때 실행
        if request.POST['password1']==request.POST['password2']:
            from django.contrib.auth.models import User
            user=User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'],
            )
            auth.login(request, user)
            return redirect('board:board') # 네임스페이스:URL 이름   #회원가입이 성공적으로 처리됨, '/'(홈)페이지로 이동
        return render(request,'accounts/signup.html')
    else:
        form=UserCreationForm() # 장고가 기본적으로 제공하는 내장 폼
    return render(request,'accounts/signup.html',{'form':form})

# 각 함수에서 request 매개변수는 HTTP 요청(request) 객체를 의미
# auth는 장고에서 제공하는 인증 관련 기능을 담당하는 모듈. 각 함수의 동작을 제대로 수행하기 위해서는 auth 모듈이 미리 설정되어 있어야 함
def login(request): # POST 요청을 받았을 때 사용자가 제출한 로그인 정보를 검증하여 인증을 수행함
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('board:board')
        else:
            return render(request,'accounts/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('board:board')

# def home(request):
#     return render(request,'accounts/home.html')