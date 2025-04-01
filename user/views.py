from rest_framework import status, generics,status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView

from .serializers import (
    MyTokenObtainPairSerializer, 
    UserSerializer, 
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)

User = get_user_model()

class CurrentUserView(APIView):
    """ Returns the authenticated user's details. """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "name": user.get_full_name(),
            "user_type": user.user_type 
        })

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that uses our enhanced token serializer
    """
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    """
    API view to register a new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class PasswordResetRequestView(generics.GenericAPIView):
    """
    API view for requesting a password reset
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate token and uid
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Build reset URL (this would point to your frontend)
                reset_url = f"http://localhost:5173/reset-password?uid={uid}&token={token}"
                
                # Send email
                subject = "Password Reset Request"
                message = f"Please use the following link to reset your password: {reset_url}"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]
                
                send_mail(subject, message, from_email, recipient_list)
                
                return Response(
                    {"detail": "Password reset email has been sent."},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                # We don't want to reveal which emails are in the database for security
                return Response(
                    {"detail": "Password reset email has been sent."},
                    status=status.HTTP_200_OK
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    """
    API view for confirming a password reset
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(serializer.validated_data['uidb64']))
                user = User.objects.get(pk=uid)
                
                # Check if token is valid
                if default_token_generator.check_token(user, serializer.validated_data['token']):
                    # Set new password
                    user.set_password(serializer.validated_data['password'])
                    user.save()
                    
                    return Response(
                        {"detail": "Password has been reset successfully."},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"detail": "Invalid token."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response(
                    {"detail": "Invalid user ID."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
