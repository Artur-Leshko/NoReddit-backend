from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from userprofile.models import UserProfile

User = get_user_model()

@csrf_exempt
@transaction.atomic
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)

            with transaction.atomic():
                user = User.objects.create(email=data['email'], username=data['username'])
                user.set_password(data['password'])
                user.save()

                userprofile = UserProfile.objects.create(user=user, id=user.id)
                userprofile.save()

                refreshToken = RefreshToken.for_user(user)

            return JsonResponse({ 'refresh': str(refreshToken), 'access': str(refreshToken.access_token), })
        except IntegrityError:
            return JsonResponse({ 'error': 'That username or email has already been taken! Please choose another one.' }, status=status.HTTP_400_BAD_REQUEST)
