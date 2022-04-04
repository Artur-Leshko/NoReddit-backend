from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreatePost.as_view() , name='posts_create'),
    path('popular/', views.PopularPostsList.as_view(), name='posts_popular'),
    path('<str:pk>/upvote/', views.UpvotePostDetail.as_view(), name='post_upvote'),
    path('<str:pk>/downvote/', views.DownvotePostDetail.as_view(), name='post_downvote'),
]
