from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import MyUser


class MyUserAdmin(UserAdmin):
    # 필요한 요소만
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'gender', 'nickname')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'nickname',)
    list_filter = ('is_staff', 'is_superuser',)


admin.site.register(MyUser, MyUserAdmin)
