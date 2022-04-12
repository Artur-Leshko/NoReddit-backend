from rest_framework import generics, permissions

from .serializers import CategorySerializer
from categories.models import Category

class CategoriesList(generics.ListAPIView):
    '''
        Categories list
    '''
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
