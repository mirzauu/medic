from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import UserProfile
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated  


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Fetch additional user details from UserProfile
            user_profile = UserProfile.objects.get(user=user)
            
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

            # Set the tokens in cookies
            response.set_cookie(
                key='access_token', 
                value=access_token, 
                httponly=True, 
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

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)