from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from djapp.models import *
from djapp.serializer import *
from .serializers import *

# Create your views here.


@api_view(['POST'])
def logadmin(request):
    print('in logadmin')
    username = request.data['username']
    password = request.data['password']
    print(username, password)
    check = admins.objects.filter(
        user_name=username, password=password).first()
    if check:
        admincheck = 'True'
    else:
        admincheck = 'False'
    return Response(admincheck)


@api_view(['GET', 'POST'])
def userlist(request):
    if request.data:
        # if request.data['auth']:
        #     print("yes")
            allusers = User.objects.all()
            serializer = UserSerializers(allusers, many=True)
            print(allusers)
            print(serializer.data)
            return Response(serializer.data)
    else:
        # print("no")
        return Response(500)


@api_view(['PUT'])
def edituser(request, id):
    print('in edit', id)
    print('ddata', request.data)
    data = request.data

    try:
        user = User.objects.get(id=id)
        data['password'] = user.password
        print('ko', data)
    except:
        return Response('User not found in the data')
    editserializer = UserSerializers(user, data)
    if editserializer.is_valid():
        editserializer.save()
        check = User.objects.get(id=id)
        print('io', check)

        return Response(200)
    return Response(editserializer.errors)


@api_view(['POST'])
def deleteuser(request, id):
    try:
        user = User.objects.get(id=id)
        if user.is_blocked == True:
            user.is_blocked = False
        else:
            user.is_blocked = True
        user.save()
        return Response(200)
    except:
        return Response('User not found in the data')
    
@api_view(['POST'])
def emailVerifyAdmin(request, id):
    try:
        user = User.objects.get(id=id)
        if user.is_verified == True:
            user.is_verified = False
        else:
            user.is_verified = True
        user.save()
        return Response(200)
    except:
        return Response('User not found in the data')


@api_view(['GET', 'PUT'])
def BussinessReq(request, id):
    try:
        check = BussinessRequest.objects.get(user=id)
        return Response('User already in request list')
    except:
        add = BussinessRequest()
        use = User.objects.get(id=id)
        add.user = use
        add.save()
        return Response('added into bussiness requests')


@api_view(['GET'])
def getBussinessReqs(request):
    alldat = BussinessRequest.objects.all()
    serializer = BussinessSerializer(alldat, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def removeBussinessReq(request, id):
    try:
        bussreqdata = BussinessRequest.objects.get(id=id)
        bussreqdata.delete()
        return Response('removed successfully')
    except:
        return Response('Request not found')


@api_view(['GET'])
def acceptBussinessReq(request, id):
        print('kkkkkkk',id)
        busreq = BussinessRequest.objects.get(id = id)
        print('pppp',busreq.user)
        use = User.objects.get(email = busreq.user)
        use.is_bussiness = True
        use.save()
        busreq.delete()
        return Response(200)
   

@api_view(['GET'])
def allPost(request):
        busreq = BussinessRequest.objects.get(id = id)
        use = User.objects.get(email = busreq.user)
        use.is_bussiness = True
        use.save()
        busreq.delete()
        return Response(200)


@api_view(['POST'])
def ReportPost(request):

    propt0 = PostReports.objects.filter(post_id=request.data['post'],opt=1).count()
    propt1 = PostReports.objects.filter(post_id=request.data['post'],opt=2).count()
    propt2 = PostReports.objects.filter(post_id=request.data['post'],opt=3).count()
    propt3 = PostReports.objects.filter(post_id=request.data['post'],opt=4).count()
    reasons = [propt0,propt1,propt2,propt3]


    max_val = reasons[0]
    for i in range(1, len(reasons)):
        if reasons[i] >= max_val:
            max_val = reasons[i]

    if max_val == reasons[0]   : 
        option = 1

    elif max_val == reasons[1]:
        option = 2
 
    elif max_val == reasons[2] : 
        option = 3

    else :
        option = 4

    try:
        check = PostReports.objects.get(user_id=request.data['user'],post_id=request.data['post'])
        return Response('already in report list')
    except:
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            countadd = PostReportsCount.objects.get(post_id=request.data['post'])
            countadd.total_reports=countadd.total_reports+1
            countadd.most_reason = option
            countadd.save()
        except:
            postobj = Posts.objects.get(id=request.data['post'])
            countadd = PostReportsCount()
            countadd.post = postobj
            countadd.total_reports = 1
            countadd.most_reason = option
            countadd.save()

        return Response('report done')

@api_view(['GET'])
def getPostReports(request):
    dat = PostReportsCount.objects.all()
    serializer = GetReportSerializer(dat,many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def removePost(request,id):
    postobj = Posts.objects.get(id=id)
    postobj.delete()
    posreportcount = PostReportsCount.objects.get(post_id=id)
    posreportcount.delete()
    postreport = PostReports.objects.get(post_id=id)
    postreport.delete()
    return Response('success')

@api_view(['DELETE'])
def ignorePost(request,id):
    pos = PostReportsCount.objects.get(post_id = id)
    postreport=PostReports.objects.filter(post_id = id)
    postreport.delete()
    pos.delete()
    return Response('success')

