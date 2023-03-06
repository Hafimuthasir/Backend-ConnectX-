from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from django.db.models import Q
from djapp.models import Posts

# Create your views here.
@api_view(['POST'])
def getChats(request):
    print('in get chat',request.data)
    owner = request.data['primary_user']
    selectedUser = request.data['secondary_user']
    if owner == selectedUser:
        return Response(200)
    try:
        try:
            rm = Room.objects.get(primary_user=owner,secondary_user=selectedUser)
            print('in this')
        except:
            rm = Room.objects.get(primary_user=selectedUser,secondary_user=owner)
        
        cht = Chat.objects.filter(room=rm.id)
        print('jj',cht)
        serializer = MessageSerializer(cht,many=True)
        print('sss',serializer.data)
        return Response(serializer.data)
    except:
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(200)





@api_view(['GET'])
def getChatList(request,id):
    chatlist  = Room.objects.filter(primary_user=id) | Room.objects.filter(secondary_user = id)
    serializer = RoomSerializer(chatlist,many=True)
    return Response(serializer.data)

    

@api_view(['POST'])
def post_messages(request):
    serializer = MessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(200)


@api_view(['GET'])
def getChatsByRoom(request,id):
    chats=Chat.objects.filter(room=id)
    serializer = MessageSerializer(chats,many=True)
    return Response(serializer.data)
