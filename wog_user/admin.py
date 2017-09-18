from django.contrib import admin

from guardian.models import UserObjectPermission
from wog_user.models import User


# Register your models here.
admin.site.register(User)

class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission', 'object_pk')

admin.site.register(UserObjectPermission, UserPermissionAdmin)