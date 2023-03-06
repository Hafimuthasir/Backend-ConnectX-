from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('logadmin',logadmin,name='logadmin'),
    path('userlist',userlist,name='userlist'),
    path('edituser/<int:id>',edituser,name='edituser'),
    path('deleteuser/<int:id>',deleteuser,name='deleteuser'),
     path('emailVerifyAdmin/<int:id>',emailVerifyAdmin,name='emailVerifyAdmin'),
    path('bussinessReq/<int:id>',BussinessReq,name='bussinessReq'),
    path('getbussinessReqs',getBussinessReqs,name='bussinessReq'),
    path('removebussreq/<int:id>',removeBussinessReq,name='removebussreq'),
    path('acceptbussreq/<int:id>',acceptBussinessReq,name='acceptbussreq'),
    path('reportpost',ReportPost,name='reportpost'),
    path('getpostreports',getPostReports,name='postreports'),
    path('removepost/<int:id>',removePost,name='removepost'),
    path('ignorepost/<int:id>',ignorePost,name='ignorepost'),
]
