from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.userprofile.serializers import UserProfileSerializer
from userprofile.models import UserProfile, Followers
from api.exeptions import CustomApiException

User = get_user_model()

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

    def get_object(self, pk):
        '''
            returns UserProfile object
        '''

        try:
            userprofile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise CustomApiException(404, "User profile does not exist")

        return userprofile

    def post(self, request, pk):
        '''
            create new cortege in m2m table, returns obj of UserProfile that followed UserProfile
        '''
        userprofile = self.get_object(request.user.id)
        followed_userprofile = self.get_object(pk)

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

    def get_object(self, pk):
        '''
            returns UserProfile object
        '''

        try:
            userprofile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise CustomApiException(404, "User profile does not exist")

        return userprofile

    def post(self, request, pk):
        '''
            removes cortege in m2m table
        '''
        userprofile = self.get_object(request.user.id)
        followed_userprofile = self.get_object(pk)

        userprofile.followers.remove(followed_userprofile)
        userprofile.save()

        serilizer = UserProfileSerializer(userprofile)

        return Response(serilizer.data, status=status.HTTP_200_OK)
