from rest_framework import status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from userprofile.models import UserProfile
from api.exeptions import CustomApiException

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
            raise CustomApiException(400, 'That username or email has already been taken! Please choose another one.')
        except:
            raise CustomApiException(400, 'Some of the data is missing: username, password or email')
        return JsonResponse({'message': 'You have successfully registered! Now sign-in!'},
                status=status.HTTP_201_CREATED)

