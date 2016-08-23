from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now


class Book(models.Model):
    # primary key is auto-generated
    title = models.CharField(max_length=150)
    # author = models.CharField(max_length=70, help_text="Use pen name, not real name")
    authors = models.ManyToManyField("Author", related_name="books")
    review = models.TextField(blank=True, null=True)  # field not required
    reviewed_by = models.ForeignKey(User, blank=True, null=True, related_name="reviews")
    date_reviewed = models.DateTimeField(blank=True, null=True)
    # by default Django displays the field capitalizing the field and substituting underscores by spaces
    # but we can choose how to display it by changing the verbose_name attribute
    is_favourite = models.BooleanField(default=False, verbose_name="Favourite ?")

    def __str__(self):
        return "{} by {}".format(self.title, self.list_authors())

    def list_authors(self):
        return ", ".join([author.name for author in self.authors.all()])

    # we will override the save method using args and kwargs to
    # ensure that we have access to future django implementations of the save method
    def save(self, *args, **kwargs):
        # if we are submitting a review and date_reviewed is empty or none or null
        if self.review and self.date_reviewed is None:
            self.date_reviewed = now()

        # ensure the save method is called
        super(Book, self).save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=70, help_text="Use pen name, not real name", unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk', self.pk})
