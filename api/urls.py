from django.urls import path
from . import views

urlpatterns = [
    path('room-list/', views.roomList, name='room-list'),
    path('room-details/<str:pk>', views.roomDetails, name='room-details'),
    path('room-create/', views.createRoom, name='room-create'),
    path('room-update/<str:pk>/', views.updateRoom, name='room-update'),
    path('room-delete/<str:pk>/', views.deleteRoom, name='room-delete')
]