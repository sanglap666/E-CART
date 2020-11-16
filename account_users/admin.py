from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,UserAddress
from django.contrib.auth.models import Group
# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserCreationForm
from django.contrib import admin


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('username','email','is_admin')
    list_filter=('is_admin',)

    fieldsets = (
        (None,{'fields':('username','email','password')}),
        ('Permissions',{'fields':('is_admin','is_staff','is_active')})
    )

    search_fields = ('username','email')
    ordering = ('username','email')
    filter_horizontal = ()

admin.site.register(UserAddress)
admin.site.register(User,UserAdmin)
admin.site.unregister(Group)
