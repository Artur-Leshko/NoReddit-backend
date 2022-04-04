from django.urls import path
from . import views

urlpatterns = [
    path('self/profile/', views.UserProfileView.as_view(), name='userprofile'),
    path('<str:pk>/profile/', views.UserProfilePublicView.as_view(), name="userprofile_public"),
]
