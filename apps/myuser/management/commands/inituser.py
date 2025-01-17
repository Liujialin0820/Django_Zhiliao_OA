from django.core.management.base import BaseCommand
from apps.myuser.models import MyUser, MyDepartment
from rest_framework.response import Response


class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = MyDepartment.objects.get(name="董事会")
        developer = MyDepartment.objects.get(name="产品开发部")
        operator = MyDepartment.objects.get(name="运营部")
        saler = MyDepartment.objects.get(name="销售部")
        hr = MyDepartment.objects.get(name="人事部")
        finance = MyDepartment.objects.get(name="财务部")

        # 董事会的员工，都是superuser用户
        # 1. 东东：属于董事会的leader
        dongdong = MyUser.objects.create_superuser(
            email="dongdong@qq.com",
            username="东东",
            password="111111",
            department=boarder,
        )
        # 2. 多多：董事会
        duoduo = MyUser.objects.create_superuser(
            email="duoduo@qq.com",
            username="多多",
            password="111111",
            department=boarder,
        )
        # 3. 张三：产品开发部的leader
        zhangsan = MyUser.objects.create_user(
            email="zhangsan@qq.com",
            username="张三",
            password="111111",
            department=developer,
        )
        # 4. 李四：运营部leader
        lisi = MyUser.objects.create_user(
            email="lisi@qq.com", username="李四", password="111111", department=operator
        )
        # 5. 王五：人事部的leader
        wangwu = MyUser.objects.create_user(
            email="wangwu@qq.com", username="王五", password="111111", department=hr
        )
        # 6. 赵六：财务部的leader
        zhaoliu = MyUser.objects.create_user(
            email="zhaoliu@qq.com",
            username="赵六",
            password="111111",
            department=finance,
        )
        # 7. 孙七：销售部的leader
        sunqi = MyUser.objects.create_user(
            email="sunqi@qq.com", username="孙七", password="111111", department=saler
        )

        # 给部门指定leader和manager
        # 分管的部门
        # 东东：产品开发部、运营部、销售部
        # 多多：人事部、财务部
        # 1. 董事会
        boarder.leader = dongdong
        boarder.manager = None

        # 2. 产品开发部
        developer.leader = zhangsan
        developer.manager = dongdong

        # 3. 运营部
        operator.leader = lisi
        operator.manager = dongdong

        # 4. 销售部
        saler.leader = sunqi
        saler.manager = dongdong

        # 5. 人事部
        hr.leader = wangwu
        hr.manager = duoduo

        # 6. 财务部
        finance.leader = zhaoliu
        finance.manager = duoduo

        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()

        self.stdout.write("初始用户创建成功！")
