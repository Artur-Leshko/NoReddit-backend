from rest_framework import status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from userprofile.models import UserProfile

User = get_user_model()

@csrf_exempt
@transaction.atomic
def signup(request):
    '''
        view for sign-up new user
    '''
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            with transaction.atomic():
                user = User.objects.create(email=data['email'], username=data['username'])
                user.set_password(data['password'])
                user.save()

                userprofile = UserProfile.objects.create(user=user, id=user.id)
                userprofile.save()
        except IntegrityError:
            return JsonResponse({'message': 'That username or email has already been taken! Please choose another one.'},
                status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'message': 'Some of the data is missing: username, password or email'},
                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'You have successfully registered! Now sign-in!'},
                status=status.HTTP_201_CREATED)
