from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoriesListView.as_view(), name='categories_list'),
    path('create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('<str:pk>/', views.CategoryRetrieveView.as_view(), name='category_detail'),
    path('<str:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('<str:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('<str:pk>/posts/', views.CategoryPostsListView.as_view(), name='category_posts'),
]
