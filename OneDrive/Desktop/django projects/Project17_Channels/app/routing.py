from django.urls import path
from . import consumers

websocket_patterns = [
    path('ws/sc/', consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:group>', consumers.MyAsyncConsumer.as_asgi()),

]