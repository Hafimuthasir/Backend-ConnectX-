from django.db import models
from djapp.models import User
# Create your models here.

class Room(models.Model):
    primary_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='primary_user',unique=False)
    secondary_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='secondary_user',unique=False)

class Chat(models.Model):
    messages = models.TextField(blank=True)
    room  = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='specific_room',unique=False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='chat_owner',unique=False)