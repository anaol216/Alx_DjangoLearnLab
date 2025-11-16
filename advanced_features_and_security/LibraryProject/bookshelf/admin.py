from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

admin.site.register(Book, BookAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined', 'date_of_birth')
    list_editable = ('first_name', 'last_name', 'date_of_birth')

    # FIX: list_display_links must point to an existing field in list_display
    list_display_links = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'first_name', 'last_name', 'date_of_birth'
            )
        }),
    )

    readonly_fields = ('last_login', 'date_joined')


# Remove default User if registered
try:
    from django.contrib.auth.models import User as DefaultUser
    admin.site.unregister(DefaultUser)
except admin.sites.NotRegistered:
    pass

admin.site.register(CustomUser, CustomUserAdmin)
