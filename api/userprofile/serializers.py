from rest_framework import serializers
from userprofile.models import UserProfile
from django.contrib.auth import get_user_model
from api.exeptions import CustomApiException

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
        fields = ['username', 'is_admin']

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
        fields = ['id', 'user', 'avatar', 'firstname', 'surname']

    def update(self, instance, validated_data):
        user_data = {}
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
        user = instance.user

        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()

        user.username = user_data.get('username', user.username)
        user.save()

        return instance

class UserProfileReadSerializer(serializers.ModelSerializer):
    '''
        Serializer class for Userprofile model that user in post urls
    '''

    class Meta:
        '''
            Meta class for UserProfilePost serializer
        '''
        model = UserProfile
        fields = ['id', 'username', 'firstname', 'avatar', 'surname']
        read_only_fields = ['id', 'username', 'firstname', 'avatar', 'surname']
