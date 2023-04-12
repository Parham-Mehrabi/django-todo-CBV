from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model

user = get_user_model()

 
class CostumeUserAdmin(UserAdmin):
    model = user
    list_display = ('email','is_staff','is_superuser','is_active')
    list_filter = ('email','is_staff','is_superuser','is_active')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (
        'AUTH',{
            'fields': ('email','password')
        }),
        ('STATUS',{ 
            'fields': ('is_staff','is_superuser','is_active')
        })
    )

    add_fieldsets = (
        (None,{
            'fields':('email','password1', 'password2', 'is_staff', 'is_superuser', 'is_active')
        }),
    )

admin.site.register(user,CostumeUserAdmin)

