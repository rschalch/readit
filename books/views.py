from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import View

from books.models import Book, Author


# Create your views here.

# functional view example
def list_books(request):
    """
    List the books that have reviews
    :param request:
    :return:
    """

    # prefetch_related will save us from getting to many database queries
    # since there's a loop looking for book.list_authors in the template
    # so: be careful with database calls inside loops
    books = Book.objects.exclude(date_reviewed__isnull=True).prefetch_related('authors')

    context = {
        'books': books
    }

    # return HttpResponse(request.user.username)
    return render(request, 'list.html', context)


# class based view example
class AuthorList(View):
    def get(self, request):
        authors = Author.objects.annotate(
            published_books=Count("books")  # "books": related_name of authors field (manytomany) in Book model
        ).filter(
            published_books__gt=0
        )

        context = {
            'authors': authors
        }

        return render(request, 'authors.html', context)


# class based GENERIC view example
class BookDetail(DetailView):
    model = Book
    template_name = 'book.html'

class AuthorDetail(DetailView):
    model = Author
    template_name = "author.html"
