from django.http import HttpResponse
from django.shortcuts import render
from books.models import Book

# Create your views here.

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