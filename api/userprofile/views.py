from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from api.userprofile.serializers import UserProfileSerializer, FollowerSerializer
from userprofile.models import UserProfile
from api.exeptions import CustomApiException

User = get_user_model()

QUERY_STRING_FOR_FOLLOWERS = '''
    SELECT u.id, u.firstname, u.surname, u.avatar, u.user_id
        FROM userprofile_userprofile u
            JOIN userprofile_followers uf ON uf.follower_id = u.id
                AND uf.followed_id = %s
'''

QUERY_STRING_FOR_FOLLOWED = '''
    SELECT u.id, u.firstname, u.surname, u.avatar, u.user_id
        FROM userprofile_userprofile u
            JOIN userprofile_followers uf ON uf.followed_id = u.id
                AND uf.follower_id = %s
'''


class FollowerPagination(PageNumberPagination):
    '''
        Pagination class for followers
    '''
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UsersListView(generics.ListAPIView):
    '''
        returns list of users
    '''
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['^firstname', '^surname', '^user__username']
    ordering_fields = ['firstname', 'surname', 'user__username']
    ordering = ['firstname']

class UserProfileView(APIView):
    '''
        Output of the Userprofile
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, user):
        '''
            returns UserProfile object
        '''

        try:
            userprofile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise CustomApiException(404, "User profile does not exist")

        return userprofile

    def get(self, request):
        '''
            Return userprofile of logged in user
        '''

        userprofile = self.get_object(request.user)
        data = UserProfileSerializer(userprofile).data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        '''
            Updates data for loggen in user
        '''
        userprofile = self.get_object(request.user)
        serializer = UserProfileSerializer(userprofile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        raise CustomApiException(400, 'Bad data!')

    def delete(self, request):
        '''
            Deletes UserProfile for logged in user
        '''
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfilePublicView(APIView):
    '''
        Output for the public UserProfile
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        '''
            Returns UserProfile for public user
        '''

        try:
            userprofile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise CustomApiException(404, "User profile does not exist")

        return userprofile

    def get(self, request, pk):
        '''
            Return public userprofile of any user
        '''

        userprofile = self.get_object(pk)
        data = UserProfileSerializer(userprofile).data
        return Response(data, status=status.HTTP_200_OK)


class UserProfileSubscribeView(APIView):
    '''
        Subscribes user on another user
    '''

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        '''
            create new cortege in m2m table, returns obj of UserProfile that followed UserProfile
        '''
        userprofile = get_object_or_404(UserProfile, id=request.user.id)
        followed_userprofile = get_object_or_404(UserProfile, id=pk)

        if userprofile == followed_userprofile:
            raise CustomApiException(400, "You can not subscribe on yourself!")

        userprofile.followers.add(followed_userprofile)
        userprofile.save()

        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileUnsubscribeView(APIView):
    '''
        Unsubscribes user from another user
    '''

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        '''
            removes cortege in m2m table
        '''
        userprofile = get_object_or_404(UserProfile, id=request.user.id)
        followed_userprofile = get_object_or_404(UserProfile, id=pk)

        userprofile.followers.remove(followed_userprofile)
        userprofile.save()

        serilizer = UserProfileSerializer(userprofile)

        return Response(serilizer.data, status=status.HTTP_200_OK)

class FollowerListView(APIView, FollowerPagination):
    '''
        return list of followers for user
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        '''
            returns list of followers for user
        '''
        users = UserProfile.objects.raw(QUERY_STRING_FOR_FOLLOWERS, [pk])
        serializer = FollowerSerializer(self.paginate_queryset(users, request, view=self), many=True)

        return self.get_paginated_response(serializer.data)

class FollowedListView(APIView, FollowerPagination):
    '''
        return list of followers for user
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        '''
            returns list of followers for user
        '''
        users = UserProfile.objects.raw(QUERY_STRING_FOR_FOLLOWED, [pk])
        serializer = FollowerSerializer(self.paginate_queryset(users, request, view=self), many=True)

        return self.get_paginated_response(serializer.data)
