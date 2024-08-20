from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, TestDetails


class TestDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestDetails
        fields = ['sample_collected_at', 'age', 'doctor']   

class UserProfileSerializer(serializers.ModelSerializer):
    test_details = TestDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'date_of_birth', 'test_details']
        
     

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']
