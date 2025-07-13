from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


#---------------------------------  OTP Verify View  -------------------------------------------
class OTPVerifyView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.save()
            return Response({'message': 'Confirmed Successfully', 'phone_number': phone_number})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#---------------------------------  Register View  -------------------------------------------
# accounts/views.py
class SignUpView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully.',
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#---------------------------------  User Profile View  -------------------------------------------
# accounts/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .models import UserProfile


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile



#---------------------------------  OTP Request View  -------------------------------------------
# accounts/views.py
import random
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import AllowAny


class OTPRequestView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)


        recent_otp = OTP.objects.filter(phone_number=phone_number, created_at__gte=timezone.now() - timedelta(minutes=1))
        if recent_otp.exists():
            return Response({'error': 'You can request OTP only once per minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = str(random.randint(100000, 999999))

        OTP.objects.create(phone_number=phone_number, code=code)

        #OTP Code In Log
        print(f"OTP for {phone_number}: {code}")

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


#---------------------------------  Complete Register View  -------------------------------------------

class CompleteRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CompleteRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Signup Complete Successfully",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

