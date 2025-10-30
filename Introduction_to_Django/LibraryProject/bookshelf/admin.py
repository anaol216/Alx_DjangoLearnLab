from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Fields to display in list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add search functionality
    search_fields = ('title', 'author')
    
    # Add filters in the sidebar
    list_filter = ('publication_year',)

# Register the Book model with the custom admin
admin.site.register(Book, BookAdmin)
