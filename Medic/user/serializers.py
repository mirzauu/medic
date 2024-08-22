from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, TestDetails, Doctor, Tests

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name']

class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = ['Test_Description', 'Biological_Reference_Interval']

class TestDetailsSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    tests = TestsSerializer(many=True, read_only=True)
    Value_Observed = serializers.IntegerField()

    class Meta:
        model = TestDetails
        fields = ['age', 'doctor', 'sample_collected_at', 'tests', 'Value_Observed']

class UserProfileSerializer(serializers.ModelSerializer):
    test_details = TestDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'test_details']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'profile']
