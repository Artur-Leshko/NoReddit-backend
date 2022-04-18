from rest_framework import generics, permissions, serializers

from api.exeptions import CustomApiException
from .serializers import CategorySerializer, CategoryDetailSerializer
from categories.models import Category

class CategoriesListView(generics.ListAPIView):
    '''
        Categories list
    '''
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    queryset = Category.objects.all()

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
