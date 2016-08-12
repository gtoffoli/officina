# -*- coding: utf-8 -*-"""

from django.contrib import admin
from .models import Series, Author, Book, BookAuthor

class SeriesAdmin(admin.ModelAdmin):
    list_display = ['import_id', 'id', 'title', 'subtitle', 'workflow_state',]

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['import_id', 'id', 'family_name', 'given_name', 'workflow_state',]

class BookAdmin(admin.ModelAdmin):
    list_display = ['import_id', 'id', 'title', 'subtitle', 'workflow_state', 'publication_state', 'series', 'isbn', 'pde', 'year', 'price',]

class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'author', 'role', 'role_prefix',]

    def book(self, obj):
        return obj.book.title

    def author(self, obj):
        return obj.author.get_full_name()

admin.site.register(Series, SeriesAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)


