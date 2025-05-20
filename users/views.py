from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from loguru import logger

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={201: UserRegisterSerializer()}
    )
    def post(self, request):
        logger.info(f"Registration attempt for email: {request.data.get('email')}")
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.success(f"User registered successfully: {user.email}")
            return Response(UserRegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        logger.error(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )
        }
    )
    def post(self, request):
        logger.info(f"Login attempt for email: {request.data.get('email')}")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                user.refresh_token = str(refresh)
                user.save()
                logger.success(f"User logged in successfully: {user.email}")
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            logger.warning(f"Invalid credentials for email: {serializer.validated_data['email']}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        logger.error(f"Login validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        responses={200: UserProfileSerializer()}
    )
    def get(self, request, *args, **kwargs):
        logger.info(f"Profile retrieved for user: {request.user.email}")
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer()}
    )
    def put(self, request, *args, **kwargs):
        logger.info(f"Profile update attempt for user: {request.user.email}")
        response = super().put(request, *args, **kwargs)
        if response.status_code == 200:
            logger.success(f"Profile updated successfully for user: {request.user.email}")
        else:
            logger.error(f"Profile update failed for user: {request.user.email}")
        return response

    def get_object(self):
        return self.request.user
