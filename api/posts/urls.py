from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListPosts.as_view() , name='posts_list'),
    path('create/', views.CreatePost.as_view() , name='posts_create'),
    path('popular/', views.PopularPostsList.as_view(), name='posts_popular'),
    path('<str:pk>/upvote/', views.UpvotePostDetail.as_view(), name='post_upvote'),
    path('<str:pk>/downvote/', views.DownvotePostDetail.as_view(), name='post_downvote'),
    path('<str:pk>/', views.RetrievePostView.as_view(), name='post_show'),
    path('<str:pk>/delete/', views.DestroyPostView.as_view(), name='post_delete'),
    path('<str:pk>/edit/', views.UpdatePostView.as_view(), name='post_edit'),
    path('<str:pk>/comments/', views.PostCommentsList.as_view(), name='post_comments'),
]
