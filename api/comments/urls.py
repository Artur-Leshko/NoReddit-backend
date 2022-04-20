from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentView

router = DefaultRouter()
router.register('comments', CommentView)

urlpatterns = [
    path('', include(router.urls)),
]
