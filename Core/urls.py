from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', RouteList.as_view(), name='routes'),

    # User authentication related URLs
    path('register', RegisterView.as_view(), name='register'),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('emailvalidate', emailValidate, name='emailvalidate'),

    # User profile related URLs
    path('userhome', userhome, name='userhome'),
    path('getProfileDatas/<int:userid>', GetProfileDatas.as_view(), name='getProfileDatas'),
    path('ProfileCounts/<id>', ProfileCounts.as_view(), name='ProfileCounts'),

    # User post related URLs
    path('uploadPost', uploadPost.as_view(), name='uploadPost'),
    path('feedPost', FeedPostsAPIView.as_view(), name='feedPost'),
    path('getUserPosts/<int:id>', GetUserPosts.as_view(), name='getUserPosts'),
    path('LikePost', LikePost.as_view(), name='LikePost'),
    path('deletepost/<id>', deletePost, name='deletepost'),
    path('GetExplorePosts/<str:section>', GetExplorePosts.as_view(), name='GetExplorePosts'),
    path('GetLangPosts/<str:lang>', GetLangPosts.as_view(), name='GetLangPosts'),
    path('subComment',SubComment.as_view(),name='subComment'),

    # User story related URLs
    path('uploadStory', uploadStory.as_view(), name='uploadStory'),
    path('getStory', GetStoryAPIView.as_view(), name='getStory'),
    path('getOwnStory/<int:id>', GetOwnStory.as_view(), name='getOwnStory'),
    path('storywatch', StoryWatch.as_view(), name='storywatch'),
    path('getCurStory/<int:id>', CurrentStory.as_view(), name='getCurStory'),

    # User follow related URLs
    path('follow', Follow.as_view(), name='follow'),
    path('followCheck', FollowCheck.as_view(), name='followCheck'),
    path('getUserNotFollowers/<int:id>', GetUserNotFollowers.as_view(), name='GetUserNotFollowers'),

    #Downloads related URLs
    path('DownloadFile/<pk>', DownloadFile, name='DownloadFile'),
    path('addDownloadsCount', addDownloadsCount.as_view(), name='addDownloadsCount'),
    path('GetTrendingDownloads', GetTrendingDownloads.as_view(), name='GetTrendingDownloads'),

    # Miscellaneous URLs
    path('dummyPurchase', DummyPurchase.as_view(), name='dummyPurchase'),
    path('searchusers/<str:search>', searchUsers, name='searchUsers'),
    path('GetAllSearch/<str:search>', GetAllSearch.as_view(), name='GetAllSearch'),
    path('GetTestData', GetTestData, name='GetTestData'),
    path('celeryverify', celeryverify, name='celeryverify'),

]
