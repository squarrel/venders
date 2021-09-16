from django.http import JsonResponse
from functools import wraps
from rest_framework import status
from user_profile.models import UserProfile


def only_buyers(func):
    @wraps(func)
    def func_wrapper(request, pk, amount, *args, **kwargs):
        user_profile = UserProfile.objects.get(user__pk=pk)
        if user_profile.role != UserProfile.BUYER:
            return JsonResponse(
                {'message': 'This action is allowed only to users with a buyer role.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return func(request, pk, amount, *args, **kwargs)

    return func_wrapper
