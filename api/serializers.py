from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Post, User


class PostSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%b %d %Y", required=False)
    updated = serializers.DateTimeField(format="%b %d %Y", required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content',
                  'author', 'slug', 'created', 'updated']
        validators = [
            UniqueTogetherValidator(
                message='You already have another post with this title',
                queryset=Post.objects.all(),
                fields=['title', 'author']
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'image', 'date_joined']
