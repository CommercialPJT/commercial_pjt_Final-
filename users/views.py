from re import L
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.views.decorators.http import require_http_methods
from django.contrib.auth import (
    get_user_model,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
import requests
from .forms import (
    CustomUserCreationForm,
    CustomLoginForm,
)


# 나중에 key는 가릴 것
key = '07fb27a0628c6bde6abb9e4bd5ea463e'


# Create your views here.
@require_http_methods(['GET','POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('main:main')
    else:        
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'users/signup.html', context)


@require_http_methods(['GET','POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('main:main')
    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('main:main')
        else:
            print(form.errors)
            
    else:
        form = CustomLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('main:main')
    

def kakao_login(request):
    REST_API_KEY = key
    REDIRECT_URI = 'http://127.0.0.1:8000/users/login/kakao/callback/'
    # GET 형식의 url
    # 카카오 인증 서버가 사용자에게 동의 화면을 출력하여 인가를 위한 사용자 동의를 요청
    # 인가 코드 요청의 응답은 redirect_uri로 HTTP 302 Redirect
    # 보안 위해서는 state, nonce parameter 추가
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    return redirect(url)
    
    
def kakao_login_callback(request):
    # code --> 인가 코드 받기 요청을 통해 받은 인가 코드
    code = request.GET.get('code')
    REST_API_KEY = key
    REDIRECT_URI = 'http://127.0.0.1:8000/users/login/kakao/callback/'
    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
    )
    token_json = token_request.json()
    error = token_json.get("error", None)

    return redirect('main:main')


def kakao_logout(request):
    REST_API_KEY = key
    LOGOUT_REDIRECT_URI = "http://127.0.0.1:8000/users/login/"
    url = f"https://kauth.kakao.com/oauth/logout?client_id={REST_API_KEY}&logout_redirect_uri={LOGOUT_REDIRECT_URI}"
    return redirect(url)


@login_required
def profile(request) :
    return render(request,'users/profile.html')