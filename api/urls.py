from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import signup

urlpatterns = [
    # AUTH
    path('auth/sign-up/', signup, name='user_registration'),
    path('auth/sign-in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # USER PROFILE
    path('user/', include('api.userprofile.urls')),

    # POSTS
    path('posts/', include('api.posts.urls')),

    # CATEGORIES
    path('categories/', include('api.categories.urls')),
]
