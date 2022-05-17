from django.urls import path
from . import views

app_name='analysis'

urlpatterns = [
    path('', views.analysis_select, name='select'),
    path('result/', views.analysis_result, name='result'),

]
