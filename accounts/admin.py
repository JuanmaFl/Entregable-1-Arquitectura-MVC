from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'company', 'position', 'is_staff', 'is_superuser')
    ordering = ('email',)
    search_fields = ('email', 'full_name', 'company', 'position')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('full_name', 'age', 'position', 'company')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'full_name',
                'age',
                'position',
                'company',
                'password1',
                'password2',
                'is_staff',
                'is_superuser'
            ),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
