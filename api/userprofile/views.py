from django.http import Http404
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.userprofile.serializers import UserProfileSerializer
from userprofile.models import UserProfile

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
            raise Http404

        return userprofile

    def get(self, request):
        '''
            Return userprofile of logged in user
        '''

        userprofile = self.get_object(request.user)
        data = UserProfileSerializer(userprofile).data
        return Response(data, status=200)

    def put(self, request):
        '''
            Updates data for loggen in user
        '''
        userprofile = self.get_object(request.user)
        # implenet put method

    def delete(self, request):
        '''
            Deletes UserProfile for logged in user
        '''
        userprofile = self.get_object(request.user)
        userprofile.delete()
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
            raise Http404

        return userprofile

    def get(self, request, pk, format=None):
        '''
            Return public userprofile of any user
        '''

        userprofile = self.get_object(pk)
        data = UserProfileSerializer(userprofile).data
        return Response(data, status=200)
