from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import *
from django.core.files import File
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from Core.task import celeryusing
import boto3
from django.core.mail import EmailMessage
import uuid
from botocore.exceptions import ClientError
from djangoproject import settings
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class RouteList(APIView):
    def get(self, request):
        routes = [
            '/api/token',
            '/api/token/refresh'
        ]
        return Response(routes)
   

class RegisterView(APIView):
    """
    View to handle POST requests for registering a new user.
    """

    def post(self, request):

        email = request.data.get('email')
        username = request.data.get('first_name')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'email already exists..! Please Login'}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = UserSerializers(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            send_mail(email, username)
            return Response({'success': 'User created successfully!'}, status=status.HTTP_200_OK)




        
        
def send_mail(email,username):
    subject = "Email verification"
    myuuid = uuid.uuid4()
    # baseUrl = "http://localhost:3000/emailverification/"
    message = "https://master.d3emc9vq9tg0sv.amplifyapp.com/emailverification/"+str(myuuid)+"/"+username
    
    email_from = "dragunovhaunted@gmail.com"
    recipeint = [email]
    email = EmailMessage(subject=subject,body=message,to=recipeint)
    try:
        email.send() 
        return('sent') 
    except:
        return('failed')
        

# @api_view(['POST'])
# def login(request):
#     print('am login',request.data)
#     email = request.data['email']
#     password = request.data['password']
#     check = User.objects.filter(email=email,password=password).first()
#     if check:
#         user = 'True'
#         print('true')
#     else:
#         user = 'False'
#         print('false')
#     print("hj",check.id)
#     payload = {
#             'id':check.id,
#             'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
#             'iat':datetime.datetime.utcnow()
#         }
#     token = jwt.encode(payload,'secret',algorithm='HS256')

#     response = Response()
        
#     response.set_cookie(key='jwt',value=token,httponly=True)
    
#     response.data = {
#             'jwt':token,
            
#         }
#     print('lllloool')
#     tk = request.COOKIES.get('jwt')
#     print('mm',tk)
#     print('lll',response)
#     dec = jwt.decode(token,'secret',algorithms='HS256')
#     print ('ds',dec)
#     return response



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        
        token['name'] = user.first_name
        token['is_admin'] = user.is_admin
        token['is_bussiness'] = user.is_bussiness
        token['is_verified'] = user.is_verified
        if user.profile:
            token['profile'] = user.profile.url
        else:
            token['profile'] = "null"

        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
        
    

@api_view(['GET'])
def userhome(request):
    return Response(200)


class uploadPost(APIView):
    """
    View to handle POST requests for creating a new post.
    """

    def post(self, request):

        serializer = PostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response({'error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

    



class uploadStory(APIView):
    """
    View to handle POST requests for uploading a new story.
    """

    def post(self, request):
        """
        Handle POST requests to upload a new story.
        """
        serializer = StorySerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class FeedPostsAPIView(APIView):
    """
    View to handle GET requests for retrieving all posts in reverse chronological order.
    """

    def get(self, request):
        """
        Handle GET requests to retrieve all posts in reverse chronological order.
        """
        try:
            allpost = Posts.objects.all().order_by('-id')
            serializer = PostSerializer(allpost, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GetStoryAPIView(APIView):
    """
    View to handle GET requests for retrieving the latest story for each user created within the past 24 hours.
    """

    def get(self, request):
        """
        Handle GET requests to retrieve the latest story for each user created within the past 24 hours.
        """
        try:
            today = datetime.now() - timedelta(days=1)
            stories = Story.objects.filter(created_at__gte=today).order_by('userid', '-id').distinct('userid')
            serializer = StorySerializer(stories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class StoryWatch(APIView):
    """
    View to handle POST requests for adding a user's story watch.
    """

    def post(self, request):
        today = datetime.datetime.now() - datetime.timedelta(days=1)
        story_objs = Story.objects.filter(created_at__gte=today, userid_id=request.data['story'])

        for story in story_objs:
            user_obj = User.objects.get(id=request.data['user'])
            try:
                StoryWatches.objects.get(user=user_obj, story=story)
                print('already in list')
            except StoryWatches.DoesNotExist:
                new_watcher = StoryWatches()
                new_watcher.story = story
                new_watcher.user = user_obj
                new_watcher.save()

        return Response(status=status.HTTP_200_OK)


class CurrentStory(APIView):
    """
    API View to get the current story of a user.
    """

    def get(self, request, id):
        """
        Handle GET requests to get the current story of a user.
        """
        today = datetime.now() - timedelta(days=1)
        use = Story.objects.filter(userid=id, created_at__gte=today)
        serializer = StorySerializer(use, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubComment(APIView):
    """
    Create a new sub-comment for a post.

    Required POST parameters:
    - postid: ID of the post to which the sub-comment belongs
    - user: ID of the user creating the sub-comment
    - content: Text content of the sub-comment

    Returns the updated post object in serialized form.
    """
    def post(self, request):
        serializer = CommentSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = Posts.objects.get(id=request.data['postid'])
        res_serializer = PostSerializer(instance)
        return Response(res_serializer.data)



class LikePost(APIView):
    """
    Toggle a like for a post.

    Required POST parameters:
    - user: ID of the user liking the post
    - post: ID of the post being liked

    Returns the updated like count for the post.
    """
    def post(self, request):
        user = request.data['user']
        post = request.data['post']
        
        exist = Likes.objects.filter(user=user, post=post)
        if exist:
            exist.delete()
            likecount = Posts.objects.get(id=post)
            if int(likecount.likes) > 0:
                likecount.likes = likecount.likes - 1
                likecount.save()
            return Response(likecount.likes, status=status.HTTP_200_OK)
        else:
            serializer = LikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            likecount = Posts.objects.get(id=post)
            likecount.likes = int(likecount.likes) + 1
            likecount.save()
            return Response(likecount.likes, status=status.HTTP_200_OK)



class GetUserPosts(APIView):
    """
    Retrieve a user's posts based on a specified section.

    Required POST parameters:
    - section: the section from which to retrieve posts (all, files, primes, purchases)

    Returns a serialized list of posts.
    """
    def post(self, request, id):
        section = request.data.get('section')
        if section == 'all':
            posts = Posts.objects.filter(userid=id).order_by("-id")
        elif section == 'files':
            posts = Posts.objects.filter(userid=id, is_z=True).order_by("-id")
        elif section == 'primes':
            posts = Posts.objects.filter(userid=id, is_premium=True).order_by("-id")
        elif section == 'purchases':
            posts = PremiumPurchases.objects.filter(userid=id).order_by("-id")
            serializers = MyPurchases(posts, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid section specified.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializers = PostSerializer(posts, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class GetOwnStory(APIView):
    """
    Get own story for the last 24 hours.
    """
    def get(self, request, id):
        today = datetime.datetime.now() - datetime.timedelta(days=1)
        Use = Story.objects.filter(userid=id,created_at__gte=today,)
        serializers = StorySerializer(Use, many=True)
        return Response(serializers.data)


class GetProfileDatas(APIView):
    """
    Get user's profile data by user ID.
    """
    def get(self, request, userid):
        try:
            user = User.objects.get(id=userid)
            serializers = UserSerializers(user, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


class Follow(APIView):
    """
    Follow or unfollow a user.
    """
    def post(self, request):
        try:
            follower = request.data['follower']
            following = request.data['following']
            check = Follow.objects.filter(follower=follower, following=following)
            if check:
                check.delete()
                return Response('unfollowed', status=status.HTTP_200_OK)
            else:
                serializer = FollowSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response('followed', status=status.status.HTTP_200_OK)
        except KeyError:
            return Response({"error": "Missing required field"}, status=status.HTTP_400_BAD_REQUEST)
            

class FollowCheck(APIView):
    """
    Check if user is being followed
    """
    def post(self, request):
        check = Follow.objects.filter(follower=request.data['follower'], following=request.data['following'])
        if check:
            return Response('Following', status=status.HTTP_200_OK)
        else:
            return Response('Follow', status=status.HTTP_200_OK)


class ProfileCounts(APIView):
    """
    Retrieve user profile counts
    """
    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializers(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DummyPurchase(APIView):
    """
    Make a dummy purchase
    """
    def post(self, request):
        serializer = PrimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Success', status=status.status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

# @api_view(['GET'])
# def DownloadFile(self,filename):
#     # with open('reactapp/src/uploads/zpostfile/FACE_MASK_fG5rUZ1.rar') as f:
#     zip_file = open('reactapp/src/uploads/zpostfile/'+filename, 'rb')
#     response = HttpResponse(zip_file, content_type='application/force-download')
#     response['Content-Disposition'] = 'attachment; filename="%s"' % 'foo.zip'
#     return response

@api_view(['GET'])
def DownloadFile(request,pk):
    obj = Posts.objects.get(pk=pk)
    s3 = boto3.client (
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
    key = obj.zfile
    try:
        url = s3.generate_presigned_url('get_object',
                                                     Params={'Bucket':settings.AWS_STORAGE_BUCKET_NAME,
                                                             'Key': str(key)},
                                                     ExpiresIn=3600)
    except ClientError as e:
        logging.error(e)
        return Response(500)
    
    return Response(url)



class addDownloadsCount(APIView):
    def post (self,request):
        check = AllDownloads.objects.filter(postid=request.data['postid'],userid=request.data['userid'])
        if check:
            return Response('Already In DList')
        else:
            serializer = DownloadsCountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                countadd = Posts.objects.get(id=request.data['postid'])
                countadd.downloadsCount = countadd.downloadsCount + 1
                countadd.save()
                return Response("success")
        return Response('Something Went Wrong')


class GetExplorePosts(APIView):
    def get(self,request,section):
        try:
            if section == 'all':
                posts = Posts.objects.all()
                serializer = PostSerializer(posts,many=True)
                return Response(serializer.data)
            if section == 'files':
                posts = Posts.objects.filter(is_z=True)
                serializer = PostSerializer(posts,many=True)
                return Response(serializer.data)
            if section == 'primes':
                posts = Posts.objects.filter(is_premium=True)
                serializer = PostSerializer(posts,many=True)
                return Response(serializer.data)
            if section == 'trend':
                posts = Posts.objects.filter(lang='Python').order_by('-likes')
                serializer = PostSerializer(posts,many=True)
                return Response(serializer.data)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetLangPosts(APIView):
    def get(self,request,lang):
        posts = Posts.objects.filter(lang=lang)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
        

class GetUserNotFollowers(APIView):
    def get(self,request,id):
        notfollowers = Follow.objects.exclude(follower=id)
        serializer=FollowSerializerGet(notfollowers,many=True)
        return Response(serializer.data)


class GetAllSearch(APIView):
    def get(self,request,search):
        posts = Posts.objects.filter(caption__icontains=search)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)


@api_view(['GET'])
def searchUsers(request,search):
    users = User.objects.filter(first_name__icontains=search)|User.objects.filter(last_name__icontains=search)
    serializer = UserSerializers(users,many=True)
    return Response(serializer.data)
        # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTrendingDownloads(APIView):
    def get(self,request):
        data = Posts.objects.filter(is_z=True).order_by('-downloadsCount')
        serializer = PostSerializer(data,many=True)
        return Response(serializer.data)



        
@api_view(['POST']) 
def emailValidate(request):
    token = request.data['id']
    username = request.data['username']
    try :
        print('heeeeere')
        test = User.objects.get(first_name=username)
        test.is_verified = True
        test.save()
        return Response('verified succesfully')
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # print(test)
    # print(username)
    # if token is not None:
    #     ts = User.objects.get(first_name = username)
    #     ts.is_verfied = True
    #     ts.save()
    #     return Response(200) 
    # else:
    #     return Response(400)

@api_view(['GET']) 
def GetTestData(request):
    use = User.objects.get(id=1)
    print(use)
    use.is_bussiness = True
    use.save()
    return Response(200)


@api_view(['POST'])
def celeryverify(request):
    email = request.data.get('email')
    user = User.objects.get(email=email)
    username = user.first_name
    print(email,username)
    send_mail(email,username)
    return Response(200)


@api_view(['DELETE'])
def deletePost(request,id):
    instance = Posts.objects.get(id=id)
    s3 = boto3.resource('s3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
    file_path = str(instance.zfile)
    try:
        bucket.Object(file_path).delete()
    except:
        pass
    instance.delete()
    return Response(200)