from django.urls import path
from . import views

app_name='analysis'

urlpatterns = [
    path('', views.analysis_select, name='select'),
    path('result/', views.analysis_result, name='result'),
    path('update-data/', views.update_data, name='update-data'),
    path('<str:gu_name>/', views.gu_search, name='gu_name'),

]
