from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

#Register your models here.

#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(Genre)
#admin.site.register(BookInstance)
#admin.site.register(Language)

admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('lastName', 'firstName', 'dateOfBirth', 'dateOfDeath')
    fields = ['firstName', 'lastName', ('dateOfBirth', 'dateOfDeath')]
    inlines = [BookInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'displayGenre')
    inlines = [BookInstanceInline]

admin.site.register(Book, BookAdmin)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'dueBack', 'id')
    listFilter = ('status', 'dueBack')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'dueBack', 'borrower')
        }),
    )
