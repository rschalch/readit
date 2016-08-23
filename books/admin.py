from django.contrib import admin
from .models import Book, Author


# instead of using admin.site.register(Book, BookAdmin) we can use a register decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Book Details", {"fields": ["title", "authors"]}),
        ("Review", {"fields": ["is_favourite", "review", "reviewed_by", "date_reviewed"]}),
    ]

    readonly_fields = ("date_reviewed",)

    # since we cannot display authors as it's a manytomany field
    # we must create a method that returns a list of authors from
    # the given obj, in this particular case, a BOOK
    def book_authors(self, obj):
        return obj.list_authors()

    book_authors.short_description = "Author(s)"

    # "book_authors" refers to the above method
    list_display = ("title", "book_authors", "date_reviewed", "is_favourite")
    list_editable = ("is_favourite",)

    # allow the ordering of columns
    list_display_links = ("title", "date_reviewed")

    # add filters to list page
    list_filter = ("is_favourite",)

    # in order to search by authors we must access the Author's "name" field
    # to do this we can traverse from authors to name by using double underscores
    search_fields = ("title", "authors__name")


# Register your models here.
admin.site.register(Author)
