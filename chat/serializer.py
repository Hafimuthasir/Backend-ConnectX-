from rest_framework import serializers
from .models import *
from djapp.serializer import UserSerializers


class RoomSerializer(serializers.ModelSerializer):
    primary_username = serializers.SerializerMethodField()
    primary_profile = serializers.SerializerMethodField()
    secondary_username =serializers.SerializerMethodField()
    secondary_profile = serializers.SerializerMethodField()
    # primary_user = UserSerializers(many=True)
    class Meta:
        model = Room
        fields = '__all__'
    
    def get_primary_username(self,user):
        return user.primary_user.first_name

    def get_primary_profile(self, user):
        if user.primary_user.get_profile():
            photo = user.primary_user.get_profile()
            return photo.url

    def get_secondary_username(self,user):
        return user.secondary_user.first_name

    def get_secondary_profile(self, user):
        if user.secondary_user.get_profile():
            photo = user.secondary_user.get_profile()
            return photo.url


class MessageSerializer(serializers.ModelSerializer):
    # ownername = serializers.SerializerMethodField()
    class Meta:
        model=Chat
        fields = '__all__'


    # def get_ownername(self,user):
    #     return user.owner.first_name