from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import UserProfile

class SignupView(APIView):
    def post(self, request):
        data = request.data
        if UserProfile.objects.filter(username=data.get('username')).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = UserProfile.objects.create_user(
            username=data['username'],
            password=data['password'],
            security_question=data['question'],
            security_answer=data['answer']
        )
        return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class GetQuestionView(APIView):
    def post(self, request):
        username = request.data.get('username')
        try:
            user = UserProfile.objects.get(username=username)
            return Response({"question": user.security_question}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        answer = data.get('answer')
        new_password = data.get('new_password')
        
        try:
            user = UserProfile.objects.get(username=username)
            if user.security_answer == answer:
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Wrong answer"}, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)