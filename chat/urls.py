from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('getchats',getChats,name='getchats'),
    path('getchatlist/<int:id>',getChatList,name='getchatlist'),
    path('post_messages',post_messages,name='post_messages'),
    path('getchatsbyroom/<int:id>',getChatsByRoom,name='getchatsbyroom'),
]
