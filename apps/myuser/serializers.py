from rest_framework import serializers
from apps.myuser.models import MyDepartment, UserStatusChoice
from .models import MyUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,error_messages={"required": "Please enter your email address."})
    password = serializers.CharField(max_length=20, min_length=6)

    # 邮箱密码都在attrs
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # first 方法 有就返回第一个 没有就返回None
            user = MyUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("Email does not exist.")
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password")
            # 判断状态
            if user.status != UserStatusChoice.ACTIVED:
                raise serializers.ValidationError("User status abnormal")
            attrs["user"] = user

        else:
            raise serializers.ValidationError("Please enter your email and password!")

        # 验证成功就返回attrs
        return attrs


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDepartment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = MyUser
        exclude = ["password", "groups", "user_permissions"]
