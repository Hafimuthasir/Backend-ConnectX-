from rest_framework import serializers
from .models import BussinessRequest,PostReports,PostReportsCount
from Core.models import User
from Core.serializer import UserSerializers
from rest_framework.fields import SerializerMethodField



class BussinessSerializer(serializers.ModelSerializer):
    # usse = UserSerializers(many=True)
    class Meta:
        model = BussinessRequest
        depth = 1
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReports
        fields = "__all__"

class GetReportSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = PostReportsCount
        fields = "__all__"




        