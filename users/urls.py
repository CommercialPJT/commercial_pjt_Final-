from django.urls import path
from . import views


app_name='users'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('login/kakao/', views.kakao_login, name="kakao-login"),
    path('login/kakao/callback/', views.kakao_login_callback, name="kakao-callback"),
    path('logout/', views.logout, name="logout"),
    path('logout/kakao/', views.kakao_logout, name="kakao-logout"),
    path('profile/', views.profile, name="profile"),

]
