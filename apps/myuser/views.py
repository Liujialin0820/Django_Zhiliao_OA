from django.shortcuts import render
from datetime import datetime

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.myuser.serializers import LoginSerializer
from apps.myuser.authentications import generate_jwt


class LoginView(APIView):
    def post(self, request):
        # 1. 验证数据
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            user.last_login = datetime.now()
            user.save()
            token = generate_jwt(user)
            return Response({"token": token})
        else:
            return Response(serializer.errors, status=400)
