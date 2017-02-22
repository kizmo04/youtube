from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from member.models import MyUser


class MyUserAdmin(UserAdmin):
    pass


admin.site.register(MyUser, MyUserAdmin)

"""
키워드로 전달받은 검색어를 이용한 결과를 데이터베이스에 저장하는 부분 삭제
결과를 적절히 가공하거나 그대로 템플릿으로 전달
템플릿에서는 해당 결과를 데이터베이스를 거치지 않고 바로 출력
"""