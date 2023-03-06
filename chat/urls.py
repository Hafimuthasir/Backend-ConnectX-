from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('getchats',GetChats.as_view(),name='getchats'),
    path('getchatlist/<int:id>',GetChatList.as_view(),name='getchatlist'),
    path('post_messages',PostMessages.as_view(),name='post_messages'),
    path('getchatsbyroom/<int:id>',GetChatsByRoom.as_view(),name='getchatsbyroom'),
]
