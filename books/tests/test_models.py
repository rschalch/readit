from django.test import TestCase

from books.factories import AuthorFactory
from books.models import Book


# Create your tests here.
class BookTest(TestCase):

    # function that runs before the tests
    def setUp(self):
        # lets create authors and override their value
        self.author1 = AuthorFactory(name="Author 1")
        self.author2 = AuthorFactory(name="Author 2")

        self.book = Book(title="Book 1")
        self.book.save()
        self.book.authors.add(self.author1.pk, self.author2.pk)

    # function that runs after the tests
    def tearDown(self):
        self.author1.delete()
        self.author2.delete()
        self.book.delete()

    def test_can_list_authors(self):
        self.assertEqual("Author 1, Author 2", self.book.list_authors())

    def test_string_method(self):
        self.assertEqual("Book 1 by Author 1, Author 2", self.book.__str__())

    def test_custom_save_method(self):
        self.assertIsNone(self.book.date_reviewed)
        self.book.review = "A review"
        self.book.save()
        self.assertIsNotNone(self.book.date_reviewed)