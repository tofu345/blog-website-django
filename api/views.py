from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from rest_framework import generics, status, views
from rest_framework.response import Response

from api import serializers
from api.serializers import PostSerializer

from .models import Post


def home_view(request):
    return redirect('/posts')


class PostListView(LoginRequiredMixin, generics.ListAPIView, generics.CreateAPIView):
    model = Post
    serializer_class = PostSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "responseCode": 100,
                "message": "Post Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "responseCode": 103,
                "message": "Error Creating Post",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        return Response({
            "responseCode": 100,
            "message": "Posts List",
            "data": super().list(request, *args, **kwargs).data
        })


class PostDetailView(LoginRequiredMixin, generics.RetrieveAPIView, generics.UpdateAPIView):
    model = Post
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if instance:
            serializer = self.serializer_class(instance)
            return Response({
                "responseCode": 100,
                "message": "Posts Detail",
                "data": serializer.data
            })
        else:
            return Response({
                "responseCode": 103,
                "message": "Post Not Found."
            }, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        try:
            return Post.objects.get(author=self.kwargs['author'], slug=self.kwargs['slug'])
        except Post.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if not instance:
            return Response({
                "responseCode": 103,
                "message": "Post Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "responseCode": 100,
                "message": "Post Updated successfully",
                "data": serializer.data
            })
        else:
            return Response({
                "responseCode": 103,
                "message": "Error Updating Post",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if instance:
            instance.delete()
            return Response({
                "responseCode": 100,
                "message": "Post Deleted!"
            })
        else:
            return Response({
                "responseCode": 103,
                "message": "Post not found. Perhaps its been deleted?"
            })


class PostAuthorView(LoginRequiredMixin, views.APIView):
    model = Post
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        author_posts = Post.objects.filter(author=self.kwargs['author'])
        serializer = self.serializer_class(author_posts, many=True)

        return Response({
            "responseCode": 100,
            "data": {
                "post_count": author_posts.count(),
                "posts": serializer.data
            }
        })
