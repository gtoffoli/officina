# -*- coding: utf-8 -*-"""

from django.contrib import admin
from .models import Series, Author, Book, BookAuthor, Area, Distributor, DistributorArea

class SeriesAdmin(admin.ModelAdmin):
    list_display = ['import_id', 'id', 'title', 'subtitle', 'workflow_state', 'pres',]

    def pres(self, obj):
        return obj.presentation and obj.presentation[:20] or ''

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['import_id', 'id', 'family_name', 'given_name', 'workflow_state', 'pres',]

    def pres(self, obj):
        return obj.presentation and obj.presentation[:20] or ''

class BookAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('product_name',)}
    list_display = ['import_id', 'id', 'product_name', 'subtitle', 'workflow_state', 'publication_state', 'series_title', 'isbn', 'pde', 'year', 'unit_price', 'pres',]
    search_fields = ('product_name',)

    def series_title(self, obj):
        return obj.series and obj.series.title or ''

    def pres(self, obj):
        return obj.description and obj.description[:20] or ''

class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_title', 'author_name', 'role', 'role_prefix',]

    def book_title(self, obj):
        return obj.book.title

    def author_name(self, obj):
        return obj.author.get_full_name()

class AreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]

class DistributorAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'city', 'street_address', 'postal_code', 'email', 'fax',]

class DistributorAreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'distributor_title', 'area_name',]

    def distributor_title(self, obj):
        return obj.distributor.title

    def area_name(self, obj):
        return obj.area.name

admin.site.register(Series, SeriesAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(DistributorArea, DistributorAreaAdmin)

