from django.urls import path
from . import views

urlpatterns = [
    path('self/profile/', views.UserProfileView.as_view(), name='userprofile'),
    path('<str:pk>/profile/', views.UserProfilePublicView.as_view(), name="userprofile_public"),
    path('<str:pk>/subscribe/', views.UserProfileSubscribeView.as_view(), name="userprofile_subscribe"),
    path('<str:pk>/unsubscribe/', views.UserProfileUnsubscribeView.as_view(), name="userprofile_unsubscrive"),
]
