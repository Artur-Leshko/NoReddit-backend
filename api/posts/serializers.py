from django.db import transaction, IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.userprofile.serializers import UserProfilePostSerializer
from api.categories.serializers import CategorySerializer
from api.exeptions import CustomApiException
from posts.models import Post
from categories.models import Category


class PostSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post model
    '''

    owner = UserProfilePostSerializer()
    categories = serializers.ListSerializer(child=CategorySerializer())

    class Meta:
        '''
            Meta class for PostSerializer
        '''
        model = Post
        fields = ['id', 'owner', 'title', 'main_text', 'upvotes', 'downvotes', 'categories']
        read_only_fields = ['id', 'owner', 'upvotes', 'downvotes']

    @transaction.atomic
    def update(self, instance, validated_data):
        categories = []
        if 'categories' in validated_data:
            validated_data.pop('categories')
        categories = self.initial_data.get('categories')

        try:
            with transaction.atomic():
                instance.title = validated_data.get('title', instance.title)
                instance.main_text = validated_data.get('main_text', instance.main_text)
                instance.save()

                for category in categories:
                    db_category = get_object_or_404(Category, id=category.get('id'))

                    if category.get('action') == 'add':
                        instance.category_set.add(Category.objects.get(id=db_category.id))
                    elif category.get('action') == 'delete':
                        instance.category_set.remove(Category.objects.get(id=db_category.id))
                    else:
                        raise IntegrityError
        except IntegrityError:
            raise CustomApiException(404, "Category action either unkown or not provided!")
        except (Category.DoesNotExist, ValidationError):
            raise CustomApiException(404, "Category does not exist!")

        return instance

class CreatePostSerializer(serializers.ModelSerializer):
    '''
        Serializer for creating Post model
    '''

    categories = serializers.ListSerializer(child=CategorySerializer())

    class Meta:
        '''
            Meta class for CreatePostSerializer
        '''
        model = Post
        fields = ['id', 'title', 'main_text', 'categories']

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('categories')

        try:
            with transaction.atomic():

                instance = Post.objects.create(**validated_data)
                instance.save()

                for index, value in enumerate(self.initial_data.get('categories')):
                    category = get_object_or_404(Category, id=value.get('id'))
                    instance.category_set.add(Category.objects.get(id=category.id))
        except (IntegrityError, Category.DoesNotExist, ValidationError):
            raise CustomApiException(404, "Category does not exist!")

        return instance
