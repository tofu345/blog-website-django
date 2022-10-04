
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import GetObjectView, UpdateObjectView
from .models import Post, User
from .serializers import PostSerializer, UserSerializer


def home_view(request):
    return redirect(reverse('post_list'))


class PostListView(generics.ListAPIView, generics.CreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        try:
            data = serializer.data
            post = Post(
                title=data.get('title'),
                content=data.get('content'),
                author=data.get('author'),
            )
            post.save()
            return post
        except Exception as e:
            print(e)
            return False

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = self.perform_create(serializer)
            if post:
                serializer = self.get_serializer(post)
                return Response({
                    "message": "Post Created Successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Error Creating Post",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.model.valid_objects.all()

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Posts List",
            "data": super().list(request, *args, **kwargs).data
        })


class PostDetailView(GetObjectView, UpdateObjectView, generics.UpdateAPIView):
    model = Post
    serializer_class = PostSerializer
    partial_update = True
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            return self.model.valid_objects.get(author=self.kwargs['author'], slug=self.kwargs['slug'])
        except Post.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if instance:
            if instance.author == request.user.username:
                instance.delete()
                return Response({"message": "Post Deleted!"})
            else:
                return Response({"message": "You cant delete posts you did not write."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Post not found. Perhaps its been deleted?"})


class PostAuthorView(views.APIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        author_posts = Post.valid_objects.filter(author=self.kwargs['author'])
        serializer = self.serializer_class(author_posts, many=True)

        return Response({
            "message": f"Posts by {self.kwargs['author']}",
            "data": {"post_count": author_posts.count(), "posts": serializer.data}
        })


class UserInfoView(views.APIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(
            request.user, context={"request": request})
        return Response({"message": "User Information", "data": serializer.data})
