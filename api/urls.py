from django.urls import path, include

urlpatterns = [
    # AUTH

    # USER PROFILE
    path('userprofile/', include('api.userprofile.urls')),
]
