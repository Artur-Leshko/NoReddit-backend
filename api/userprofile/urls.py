from django.urls import path
from . import views

urlpatterns = [
    path('self/profile/', views.UserProfileView.as_view(), name='userprofile'),
    path('<str:pk>/profile/', views.UserProfilePublicView.as_view(), name="userprofile_public"),
    path('<str:pk>/subscribe/', views.UserProfileSubscribeView.as_view(), name="userprofile_subscribe"),
    path('<str:pk>/unsubscribe/', views.UserProfileUnsubscribeView.as_view(), name="userprofile_unsubscribe"),
    path('<str:pk>/followers/', views.FollowerListView.as_view(), name="userprofile_followers"),
    path('<str:pk>/followed/', views.FollowedListView.as_view(), name="userprofile_followed"),
]
