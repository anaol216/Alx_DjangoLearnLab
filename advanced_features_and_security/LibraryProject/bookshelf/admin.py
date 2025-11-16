from django.contrib import admin
from .models import Book, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

class BookAdmin(admin.ModelAdmin):
    # Fields to display in list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add search functionality
    search_fields = ('title', 'author')
    
    # Add filters in the sidebar
    list_filter = ('publication_year',)

# Register the Book model with the custom admin
admin.site.register(Book, BookAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined', 'date_of_birth')
    list_editable = ('first_name', 'last_name', 'date_of_birth')
    list_display_links = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth')}),
    )
    readonly_fields = ('last_login', 'date_joined')


try:
    from django.contrib.auth.models import User as DefaultUser
    admin.site.unregister(DefaultUser)
except admin.sites.NotRegistered:
    pass

admin.site.register(CustomUser, CustomUserAdmin)
