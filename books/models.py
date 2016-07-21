from __future__ import unicode_literals

from django.db import models


class Book(models.Model):
    # primary key is auto-generated
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=70)
    review = models.TextField(blank=True, null=True) # field not required
    date_reviewed = models.DateTimeField(blank=True, null=True)
    is_favourite = models.BooleanField(default=False)
