from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('posts', views.PostListView.as_view(), name='post_list'),
    path('posts/<str:author>/<slug:slug>',
         views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<str:author>',
         views.PostAuthorView.as_view(), name='post_author'),

    path('user/info', views.UserInfoView.as_view(), name="user_info"),
]
