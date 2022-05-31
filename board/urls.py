from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.board_list, name=''),
    path('write/', views.board_write, name='write'),
    path('content/<int:board_id>/', views.board_content, name='content'),
    path('content/<int:board_id>/remove/', views.board_remove, name='remove'),
    path('content/<int:board_id>/edit/', views.board_edit, name='edit'),
    path('mapboard/',views.map_board, name='mapboard'),
]
