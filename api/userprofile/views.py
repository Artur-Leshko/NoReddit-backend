from django.http import Http404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from userprofile.models import UserProfile
from api.userprofile.serializers import UserProfileSerializer

class UserProfileView(APIView):
    '''
        Output of the Userprofile
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        '''
            Return userprofile of logged in user
        '''

        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            raise Http404

        data = UserProfileSerializer(userprofile).data
        return Response(data, status=200)
