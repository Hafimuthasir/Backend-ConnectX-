from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('logadmin',AdminLogin.as_view(),name='logadmin'),
    path('userlist',UserListView.as_view(),name='userlist'),
    path('edituser/<int:id>',EditUser.as_view(),name='edituser'),
    path('deleteuser/<int:id>',BlockUser.as_view(),name='deleteuser'),
     path('emailVerifyAdmin/<int:id>',EmailVerifyAdmin.as_view(),name='emailVerifyAdmin'),
    path('bussinessReq/<int:id>',BussinessReq.as_view(),name='bussinessReq'),
    path('getbussinessReqs',BussinessReqListView.as_view(),name='bussinessReq'),
    path('removebussreq/<int:id>',RemoveBussinessReq.as_view(),name='removebussreq'),
    path('acceptbussreq/<int:id>',AcceptBussinessReq.as_view(),name='acceptbussreq'),
    path('reportpost',ReportPost.as_view(),name='reportpost'),
    path('getpostreports',getPostReports,name='postreports'),
    path('removepost/<int:id>',removePost,name='removepost'),
    path('ignorepost/<int:id>',ignorePost,name='ignorepost'),
]
