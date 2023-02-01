from django.urls import path
from .views import Index, RestartChat

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('chat/<int:chatid>', Index.as_view(), name='index_chatid'),
    path('chat/restart/<int:chatid>', RestartChat.as_view(), name='restart_chat'),
]