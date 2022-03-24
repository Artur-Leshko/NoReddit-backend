from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserProfileView.as_view(), name='userprofile'),
    path('<str:pk>/', views.UserProfilePublicView.as_view(), name="userprofile_public"),
]
