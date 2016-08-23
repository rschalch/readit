from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import View

from books.forms import ReviewForm, BookForm
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


# def review_books(request):
#     """
#     List all of the books that we want to review.
#     """
#     books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')
#
#     context = {
#         'books': books,
#     }
#
#     return render(request, "list-to-review.html", context)


class ReviewList(View):
    """
    List all of the books that we want to review.
    """

    def get(self, request):
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')

        context = {
            'books': books,
            'form': BookForm
        }

        return render(request, "list-to-review.html", context)

    def post(self, request):
        form = BookForm(request.POST)
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')

        if form.is_valid():
            form.save()
            return redirect('review-books')

        context = {
            'form': form,
            'books': books,
        }

        return render(request, "list-to-review.html", context)

@login_required
def review_book(request, pk):
    """
    Review an individual book
    """
    book = get_object_or_404(Book, pk=pk)
    form = ReviewForm

    if request.method == 'POST':
        # process form
        form = ReviewForm(request.POST)

        if form.is_valid():
            book.is_favourite = form.cleaned_data['is_favourite']
            book.review = form.cleaned_data['review']
            book.reviewed_by = request.user
            book.save()

            return redirect('review-books')

    context = {
        'book': book,
        'form': form,
    }

    return render(request, "review-book.html", context)


class CreateAuthor(CreateView):
    model = Author
    fields = ['name', ]
    template_name = 'create-author.html'

    def get_success_url(self):
        return reverse('review-books')
