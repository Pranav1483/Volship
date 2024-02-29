from rest_framework import serializers
from .models import Users, Posts


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'

class PostsSerializer(serializers.ModelSerializer):

    user = UsersSerializer()
    class Meta:
        model = Posts
        fields = '__all__'