from rest_framework import serializers

from userprofile.models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    '''
        Serializer class  for User model
    '''

    is_admin = serializers.ReadOnlyField()

    class Meta:
        '''
            Meta class for User serializer
        '''
        model = User
        fields = ['username', 'email', 'is_admin']

class UserProfileSerializer(serializers.ModelSerializer):
    '''
        Serializer class for UserProfile model
    '''

    user = UserSerializer(many=False, read_only=True)

    class Meta:
        '''
            Mate class for UserProfile serializer
        '''

        model = UserProfile
        fields = ['id', 'user', 'firstname', 'surname']
