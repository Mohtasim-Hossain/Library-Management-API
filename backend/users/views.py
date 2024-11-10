from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()

class HomeView(APIView):
    """Home view accessible to everyone."""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Welcome to the Library Management System!"})


class RegisterView(generics.CreateAPIView):
    """View to handle user registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """View to handle user login and token generation."""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = serializer.get_tokens(user)

            # Determine the redirect URL based on the user's role
            if user.is_admin():
                redirect_url = "/admin-dashboard"
            else:
                redirect_url = "/"

            # Include the redirect URL and user data in the response
            return Response({
                "tokens": tokens,
                "user": UserSerializer(user).data,
                "redirect_url": redirect_url
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AdminView(APIView):
    """Admin dashboard view, restricted to admins."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_admin():
            return Response({"message": f"Welcome Admin {request.user.username}"})
        return Response({"error": "You do not have permission to access this page."}, status=status.HTTP_403_FORBIDDEN)
