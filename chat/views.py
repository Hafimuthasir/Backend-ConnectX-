from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from django.db.models import Q
from Core.models import Posts
from rest_framework.views import APIView


class GetChats(APIView):
    """
    POST request to retrieve all the chats between two users.
    """
    def post(self, request):
        owner = request.data.get('primary_user')
        selectedUser = request.data.get('secondary_user')

        if owner == selectedUser:
            return Response('Primary and secondary user cannot be same.', status=status.HTTP_400_BAD_REQUEST)

        try:
            try:
                rm = Room.objects.get(primary_user=owner, secondary_user=selectedUser)
            except Room.DoesNotExist:
                rm = Room.objects.get(primary_user=selectedUser, secondary_user=owner)   
            
            cht = Chat.objects.filter(room=rm.id)
            serializer = MessageSerializer(cht, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except (Room.DoesNotExist, Chat.DoesNotExist):
            serializer = RoomSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)





class GetChatList(APIView):
    """
    GET request to retrieve a list of all chats for a specific user.
    """
    def get(self, request, id):
        try:
            chatlist = Room.objects.filter(primary_user=id) | Room.objects.filter(secondary_user=id)
            serializer = RoomSerializer(chatlist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response('User has no chats.', status=status.HTTP_404_NOT_FOUND)

    

class PostMessages(APIView):
    """
    POST request to create a new chat message.
    """
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class GetChatsByRoom(APIView):
    """
    GET request to retrieve all the chats for a specific room.
    """
    def get(self, request, id):
        try:
            chats = Chat.objects.filter(room=id)
            serializer = MessageSerializer(chats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Chat.DoesNotExist:
            return Response('No chats for the room.', status=status.HTTP_404_NOT_FOUND)
