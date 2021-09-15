from rest_framework import serializers
from django.contrib.auth.models import User
from user_profile.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'role','deposit')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.set_password(user.password)
        user.save()
        user_profile = UserProfile.objects.create(
            user=user, role=validated_data.pop('role'), deposit=validated_data.pop('deposit')
        )
        return user_profile

    def update(self, instance, validated_data):
        user_data = validated_data.get('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.update(
                instance=instance.user,
                validated_data=user_serializer.validated_data
            )
            validated_data['user'] = user

        return super().update(instance, validated_data)
