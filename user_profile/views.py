from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class UserProfileRecordView(APIView):
    def get(self, format=None):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def deposit(request, pk, amount):
    # perhaps vending machines validate amount on their own, so this isn't needed
    if amount % 5 != 0:
        return JsonResponse({'message': 'Invalid amount.'})

    user_profile = UserProfile.objects.get(user__pk=pk)
    user_profile.deposit += amount
    user_profile.save()

    return JsonResponse({'message': 'Success'})
