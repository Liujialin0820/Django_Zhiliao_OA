from datetime import datetime

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.myuser.serializers import LoginSerializer, UserSerializer
from apps.myuser.authentications import generate_jwt
from rest_framework import status


class LoginView(APIView):
    def post(self, request):
        # 1. 验证数据是否可用
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.now()
            user.save()
            token = generate_jwt(user)
            return Response({'token': token, 'user': UserSerializer(user).data})
        else:
            print(serializer.errors)
            # person = ｛"username": "张三", "age": 18｝
            # person.values() = ['战三', 18] dict_values
            detail = list(serializer.errors.values())[0][0]
            # drf在返回响应是非200的时候，他的错误参数名叫detail，所以我们这里也叫做detail
            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)
