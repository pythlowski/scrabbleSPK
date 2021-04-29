from django.urls import re_path

from .consumers import WSConsumer

ws_urlpatterns = [
    re_path('ws/game/(?P<room_name>\w+)/$', WSConsumer.as_asgi())
]