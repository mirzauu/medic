from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import UserProfile
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated  


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not check_password(password, user.password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)

        response = JsonResponse({
            'detail': 'Login successful',
            'user': {
                'username': user.username,
                'email': user.email,
                'phone_number': user_profile.phone_number,
                'address': user_profile.address,
                'date_of_birth': user_profile.date_of_birth,
            },
            'access_token': access_token,
            'refresh_token': refresh_token,
        })

        response.set_cookie(
            key='access_token', 
            value=access_token, 
            httponly=False, 
            secure=True, 
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token', 
            value=refresh_token, 
            httponly=True, 
            secure=True, 
            samesite='Lax'
        )
        
        return response

       

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        
        data = {
            "username": serializer.data['username'],
            "phone_number": serializer.data['profile']['phone_number'],
            "address": serializer.data['profile']['address'],
            "test_details": [
                {
                    "age": test_detail['age'],
                    "doctor_name": test_detail['doctor']['name'],
                    "sample_collected_at": test_detail['sample_collected_at'],
                    "tests": [
                        {
                            "description": test['Test_Description'],
                            "value": test_detail['Value_Observed'], 
                            "referenceInterval": test['Biological_Reference_Interval']
                        }
                        for test in test_detail['tests']
                    ]
                }
                for test_detail in serializer.data['profile']['test_details']
            ]
        }
        return Response(data)
