from django.http import JsonResponse
from functools import wraps
from rest_framework import status
from user_profile.models import UserProfile


def only_buyers(func):
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(
                user__pk=request.user.pk,
                role=UserProfile.BUYER
            )
        except UserProfile.DoesNotExist:
            return JsonResponse(
                {'message': 'This action is allowed only to users with a buyer role.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return func(request, *args, **kwargs)

    return func_wrapper
