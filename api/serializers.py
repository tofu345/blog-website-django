from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from api.models import Post


class PostSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%b %d %Y", required=False)
    updated = serializers.DateTimeField(format="%b %d %Y", required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'slug',
                  'get_absolute_url', 'created', 'updated']
        validators = [
            UniqueTogetherValidator(
                message='You already have another post with this title',
                queryset=Post.objects.all(),
                fields=['title', 'author']
            )
        ]
