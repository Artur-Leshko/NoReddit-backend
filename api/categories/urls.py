from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoriesListView.as_view(), name='categories_list'),
    path('/<str:pk>/', views.CategoryRetrieveView.as_view(), name='category_detail'),
]
