from rest_framework import serializers
from userprofile.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

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

    user = UserSerializer(many=False)

    class Meta:
        '''
            Mate class for UserProfile serializer
        '''

        model = UserProfile
        fields = ['id', 'user', 'firstname', 'surname']

    def update(self, instance, validated_data):
        user_data = {}
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
        user = instance.user

        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.save()

        user.email = user_data.get('email', user.email)
        user.username = user_data.get('username', user.username)
        user.save()

        return instance
