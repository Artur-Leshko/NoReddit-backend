from rest_framework import generics, permissions, serializers

from api.exeptions import CustomApiException
from .serializers import CategorySerializer
from categories.models import Category

class CategoriesListView(generics.ListAPIView):
    '''
        Categories list
    '''
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()

class CategoryRetrieveView(generics.RetrieveAPIView):
    '''
        Category detail view
    '''
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"
    queryset = Category.objects.get(pk=lookup_field)

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
            raise CustomApiException(404, "Bad request!")
