from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from userprofile.models import UserProfile
from posts.models import Post, Vote
from .serializers import PostSerializer, CreatePostSerializer
from api.exeptions import CustomApiException

User = get_user_model()

# path('', views.CreatePost.as_view() , name='posts_create'),
# path('popular/', views.PopularPostsList.as_view(), name='posts_popular'),
# path('<str:pk>/upvote/', views.UpvotePostDetail.as_view(), name='post_upvote'),
# path('<str:pk>/downvote/', views.DownvotePostDetail.as_view(), name='post_downvote'),
# path('<str:pk>/', views.RetrievePostView.as_view(), name='post_show'),
# path('<str:pk>/delete/', views.DestroyPostView.as_view(), name='post_delete'),
# path('<str:pk>/edit/', views.UpdatePostView.as_view(), name='post_edit'),

class PostsAndVotesTests(APITestCase):
    '''
        Tests for Posts and Votes
    '''

    def setUp(self):
        '''
            set ups database for tests
        '''

        self.first_user = User.objects.create_user(username='my user',
            email='abcdf@mail.ru', password='qwe123')
        self.first_user.save()
        self.firt_userprofile = UserProfile.objects.create(user=self.first_user,
            id=self.first_user.id)
        self.firt_userprofile.save()

        self.second_user = User.objects.create_user(username='my second user',
            email='beee@mail.ru', password='qwe123')
        self.second_user.save()
        self.second_userprofile = UserProfile.objects.create(user=self.second_user,
            id=self.second_user.id)
        self.second_userprofile.save()

        self.third_user = User.objects.create_user(username='my user',
            email='klmn@mail.ru', password='qwe123')
        self.third_user.save()
        self.third_userprofile = UserProfile.objects.create(user=self.third_user,
            id=self.third_user.id)
        self.third_userprofile.save()

        self.first_user_post = Post.objects.create(owner=self.firt_userprofile,
            title="First user post", main_text="Qwe rty")
        self.first_user_post.save()
