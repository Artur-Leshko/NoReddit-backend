from django.urls import path
from . import views

urlpatterns = [
    path('/popular', views.PopularPostsList.as_view(), name='posts_popular'),
]
