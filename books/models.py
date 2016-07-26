from __future__ import unicode_literals

from django.db import models


class Book(models.Model):
    # primary key is auto-generated
    title = models.CharField(max_length=150)
    # author = models.CharField(max_length=70, help_text="Use pen name, not real name")
    authors = models.ManyToManyField("Author", related_name="books")
    review = models.TextField(blank=True, null=True)  # field not required
    date_reviewed = models.DateTimeField(blank=True, null=True)
    # by default Django displays the field capitalizing the field and substituting underscores by spaces
    # but we can choose how to display it by changing the verbose_name attribute
    is_favourite = models.BooleanField(default=False, verbose_name="Favourite ?")

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=70, help_text="Use pen name, not real name", unique=True)

    def __str__(self):
        return self.name
