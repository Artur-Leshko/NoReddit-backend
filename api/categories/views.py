from rest_framework import generics, permissions, serializers
from rest_framework.pagination import PageNumberPagination

from api.exeptions import CustomApiException
from .serializers import CategorySerializer, CategoryDetailSerializer
from categories.models import Category
from posts.models import Post
from api.posts.serializers import PostSerializer

class CategoriesListView(generics.ListAPIView):
    '''
        Categories list
    '''
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    queryset = Category.objects.all()

class PostPagination(PageNumberPagination):
    '''
        Number of posts for pagiantion
    '''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CategoryRetrieveView(generics.RetrieveAPIView):
    '''
        Category detail view
    '''
    serializer_class = CategoryDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    lookup_field = "pk"

class CategoryCreateView(generics.CreateAPIView):
    '''
        Category create view
    '''
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except serializers.ValidationError:
            raise CustomApiException(400, "Bad request!")

class CategoryUpdateView(generics.UpdateAPIView):
    '''
        Category update view
    '''
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()

    def put(self, request, *args, **kwargs):
        try:
            return self.partial_update(request, *args, **kwargs)
        except serializers.ValidationError:
            raise CustomApiException(400, "Bad request!")

class CategoryDeleteView(generics.DestroyAPIView):
    '''
        Category delete view
    '''
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()

class CategoryPostsListView(generics.ListAPIView):
    '''
        Returns posts of particular category
    '''
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def get(self, request, pk):
        '''
            Returns posts of particular category
        '''
        order = 'created_at' if request.query_params.get('ordering') == 'ASC' else '-created_at'
        category = Category.objects.get(name=pk)
        posts = category.posts.all().order_by(order)
        serializer = PostSerializer(self.paginate_queryset(posts), many=True)

        return self.get_paginated_response(serializer.data)
