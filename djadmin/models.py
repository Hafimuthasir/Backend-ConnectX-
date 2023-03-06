from django.db import models
from djapp.models import Posts,User

# Create your models here.
class admins(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
class PostReports(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    opt =  models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)

class PostReportsCount(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    total_reports = models.IntegerField()
    most_reason = models.IntegerField(null=True)


class BussinessRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usse')
