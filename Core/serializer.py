from rest_framework import serializers
from .models import *


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'profile')


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_firstname')
    profile = serializers.SerializerMethodField('get_profile')

    class Meta:
        model = Comment
        fields = '__all__'

    def get_firstname(self, comment):
        return comment.userid.get_first_name()

    def get_profile(self, comment):
        if comment.userid.get_profile():
            photo = comment.userid.get_profile()
            return photo.url


# class PostSerializer(serializers.ModelSerializer):
#     like = LikeSerializer(many=True)
#     comment = CommentSerializer(many=True)
#     class Meta:
#         model=Posts
#         fields = ('id','file','caption','created_at','likes','userid','like','comment')
class PrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPurchases
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    like = LikeSerializer(many=True)
    comment = CommentSerializer(many=True)
    prime = PrimeSerializer(many=True)
    username = serializers.SerializerMethodField('get_username')
    profile = serializers.SerializerMethodField('get_profile')
    bio = serializers.SerializerMethodField('get_bio')

    class Meta:
        model = Posts
        fields = ('id', 'file','file2','file3','mediatype','mediatype2','mediatype3', 'caption', 'created_at', 'likes', 'userid', 'like', 'comment', 'username', 'profile', 'bio',
                  'lang', 'repo', 'is_z', 'zfile', 'zdescription', 'is_premium', 'price', 'prime',
                  )

    def get_username(self, user):
        if user.userid.get_first_name():
            return user.userid.get_first_name()

    def get_profile(self, user):
        if user.userid.get_profile():
            photo = user.userid.get_profile()
            return photo.url

    def get_bio(self, user):
        if user.userid.bio:
            userbio = user.userid.bio
            return userbio


class MyPurchases(serializers.ModelSerializer):
    postid = PostSerializer()

    class Meta:
        model = PremiumPurchases
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following')


class FollowSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following')
        depth = 1


class UserSerializers(serializers.ModelSerializer):
    owner = PostSerializer(many=True)
    follower = FollowSerializer(many=True)
    following = FollowSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'password', 'owner', 'profile', 'follower', 'following', 'is_blocked','is_verified']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # return User.objects.create(**validated_data)

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class StoryWatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryWatches
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')
    profile = serializers.SerializerMethodField('get_profile')
    watched = StoryWatchesSerializer(many=True)

    class Meta:
        model = Story
        fields = ('created_at', 'userid', 'id', 'file',
                  'username', 'profile', 'watched','mediatype')
        # depth = 1

    def get_username(self, user):
        if user.userid.get_first_name():
            return user.userid.get_first_name()

    def get_profile(self, user):
        if user.userid.get_profile():
            photo = user.userid.get_profile()
            return photo.url


class DownloadsCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllDownloads
        fields = '__all__'
