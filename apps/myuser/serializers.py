from rest_framework import serializers
from apps.myuser.models import UserStatusChoice
from .models import MyUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=20, min_length=6)

    # 邮箱密码都在attrs
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # first 方法 有就返回第一个 没有就返回None
            user = MyUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("邮箱不存在")
            if not user.check_password(password):
                raise serializers.ValidationError("密码错误")
            # 判断状态
            if user.status != UserStatusChoice.ACTIVED:
                raise serializers.ValidationError("用户状态异常")
            attrs["user"] = user

        else:
            raise serializers.ValidationError("请传入邮箱和密码!")

        # 验证成功就返回attrs
        return attrs
