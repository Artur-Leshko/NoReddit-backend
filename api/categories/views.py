from rest_framework import generics, permissions

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
