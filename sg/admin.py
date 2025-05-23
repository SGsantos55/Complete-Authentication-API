from django.contrib import admin
from sg.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UserAdmin(BaseUserAdmin):


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name",'df', "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",'df')}),
        ("Permissions", {"fields": ("is_admin",)}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],#to apply css 
                "fields": ["email", "name",'df', "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email",'id']
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
