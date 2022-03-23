from rest_framework import serializers

from userprofile.models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    '''
        Serializer class  for User model
    '''

    is_active = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()

    class Meta:
        '''
            Meta class for User serializer
        '''
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_admin']

class UserProfileSerializer(serializers.ModelSerializer):
    '''
        Serializer class for UserProfile model
    '''

    user = UserSerializer(many=False, read_only=True)
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        '''
            Mate class for UserProfile serializer
        '''

        model = UserProfile
        fields = ['id', 'user', 'firstname', 'surname', 'created_at', 'updated_at']
