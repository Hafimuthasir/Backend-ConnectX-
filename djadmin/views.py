from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Core.models import *
from Core.serializer import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics

# Create your views here.


class AdminLogin(APIView):

    """
    Log in an admin user.

    """


    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        check = admins.objects.filter(user_name=username, password=password).first()
        if check:
            admincheck = True
            status_code = status.HTTP_200_OK
        else:
            admincheck = False
            status_code = status.HTTP_401_UNAUTHORIZED
        return Response(admincheck, status=status_code)


class UserListView(APIView):
    """
    Retrieve a list of all users.

    """

    def get(self, request):
        allusers = User.objects.all()
        serializer = UserSerializers(allusers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditUser(APIView):
    """
    Update a user's information.
    """

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response('User not found in the data', status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['password'] = user.password

        editserializer = UserSerializers(user, data)

        if editserializer.is_valid():
            editserializer.save()
            check = User.objects.get(id=id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(editserializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockUser(APIView):
    """
    Toggle a user's blocked status.
    """

    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response('User not found in the data', status=status.HTTP_404_NOT_FOUND)

        user.is_blocked = not user.is_blocked
        user.save()

        return Response(status=status.HTTP_200_OK)
    

class EmailVerifyAdmin(APIView):
    """
    Toggle a user's email verification status.
    """

    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response('User not found in the data', status=status.HTTP_404_NOT_FOUND)

        user.is_verified = not user.is_verified
        user.save()

        return Response(status=status.HTTP_200_OK)



class BussinessReq(APIView):
    """
    Retrieve or create a business request for a user.
    """

    def get(self, request, id):
        try:
            check = BussinessRequest.objects.get(user=id)
            return Response('User already in request list', status=status.HTTP_400_BAD_REQUEST)
        except BussinessRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            check = BussinessRequest.objects.get(user=id)
            return Response('User already in request list', status=status.HTTP_400_BAD_REQUEST)
        except BussinessRequest.DoesNotExist:
            add = BussinessRequest(user_id=id)
            add.save()
            return Response('Added into business requests', status=status.HTTP_200_OK)


class BussinessReqListView(generics.ListAPIView):
    """
    API endpoint to retrieve all business requests
    """
    serializer_class = BussinessSerializer
    queryset = BussinessRequest.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RemoveBussinessReq(APIView):
    """
    DELETE request to remove a specific Business Request.
    """
    def delete(self, request, id):
        try:
            bussreqdata = BussinessRequest.objects.get(id=id)
            bussreqdata.delete()
            return Response('Removed successfully', status=status.HTTP_204_NO_CONTENT)
        except BussinessRequest.DoesNotExist:
            return Response('Request not found', status=status.HTTP_404_NOT_FOUND)


class AcceptBussinessReq(APIView):
    """
    GET request to accept a Business Request and mark the user as a business.
    """
    def get(self, request, id):
        try:
            busreq = get_object_or_404(BussinessRequest, id=id)
            use = User.objects.get(email=busreq.user)
            use.is_bussiness = True
            use.save()
            busreq.delete()
            return Response(status=status.HTTP_200_OK)
        except (BussinessRequest.DoesNotExist, User.DoesNotExist):
            return Response('Request not found', status=status.HTTP_404_NOT_FOUND)


class AllPost(APIView):
    """
    GET request to retrieve all Business Requests.
    """
    def get(self, request):
        busreq = BussinessRequest.objects.all()
        return Response(busreq, status=status.HTTP_200_OK)


class ReportPost(APIView):
    """
    API view for reporting a post.

    HTTP Methods: POST
    """

    def post(self, request):
        """
        Report a post.

        Parameters:
        request (HttpRequest): The HTTP request object.

        Returns:
        Response: The HTTP response object containing a message indicating whether the report was successful.
        """
        # Get the counts of each report option for the post.
        propt0 = PostReports.objects.filter(post_id=request.data['post'], opt=1).count()
        propt1 = PostReports.objects.filter(post_id=request.data['post'], opt=2).count()
        propt2 = PostReports.objects.filter(post_id=request.data['post'], opt=3).count()
        propt3 = PostReports.objects.filter(post_id=request.data['post'], opt=4).count()
        reasons = [propt0, propt1, propt2, propt3]

        # Determine the option with the most reports.
        max_val = reasons[0]
        for i in range(1, len(reasons)):
            if reasons[i] >= max_val:
                max_val = reasons[i]

        if max_val == reasons[0]:
            option = 1
        elif max_val == reasons[1]:
            option = 2
        elif max_val == reasons[2]:
            option = 3
        else:
            option = 4

        try:
            # Check if the user has already reported the post.
            check = PostReports.objects.get(user_id=request.data['user'], post_id=request.data['post'])
            return Response('Already reported.')
        except:
            # Save the report and update the post report count.
            serializer = ReportSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            try:
                countadd = PostReportsCount.objects.get(post_id=request.data['post'])
                countadd.total_reports = countadd.total_reports + 1
                countadd.most_reason = option
                countadd.save()
            except:
                postobj = Posts.objects.get(id=request.data['post'])
                countadd = PostReportsCount()
                countadd.post = postobj
                countadd.total_reports = 1
                countadd.most_reason = option
                countadd.save()

            return Response('Report submitted successfully.', status=status.HTTP_200_OK)

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

