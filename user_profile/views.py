from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class UserProfileView(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

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

    def put(self, request, pk):
        user_profile = self.get_object(pk)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_profile = self.get_object(pk=pk)
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def deposit(request, pk, amount):
    if amount not in UserProfile.ALLOWED_COINS:
        return JsonResponse({'message': 'Invalid amount.'})

    user_profile = UserProfile.objects.get(user__pk=pk)

    # forbidden for sellers
    if user_profile.role == UserProfile.SELLER:
        return JsonResponse({'message': 'Forbidden action for users of role seller.'})

    user_profile.deposit += amount
    user_profile.save()

    return JsonResponse({'message': 'Success'})
