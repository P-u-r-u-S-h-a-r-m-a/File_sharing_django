from django.contrib.auth import authenticate,login,logout
from user.models import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user.serializers import *
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(ensure_csrf_cookie,name='dispatch')
class GETCSRFToken(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        return Response({'success':'CSRF is set'})
    
class Signup(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=CustomUserSeriallizer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(email=email) 
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=user.username, password=password)  
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'detail': 'Logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Account is inactive, please verify email'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Email or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self,request):
        logout(request)
        return Response({'detail':'User Logged out Successfully.'},
                        status=status.HTTP_200_OK)


    
