# -*- coding: utf-8 -*-"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, AutoSlugField

DRAFT = 0
PUBLISHED = 1
WORKFLOW_STATE_CHOICES = (
    (DRAFT, _('Draft')),
    (PUBLISHED, _('Published')),)
WORKFLOW_STATE_DICT = dict(WORKFLOW_STATE_CHOICES)

PLANNED = 0
IN_PRESS = 1
IN_DISTRIBUTION = 2
OUT_OF_PRINT = 3
PUBLICATION_STATE_CHOICES = (
    (PLANNED, _('Planned')),
    (IN_PRESS, _('In press')),
    (IN_DISTRIBUTION, _('In distribution')),
    (OUT_OF_PRINT, _('Out of print')),)
PUBLICATION_STATE_DICT = dict(PUBLICATION_STATE_CHOICES)

class HasWorkflow(object):
    class Meta:
        abstract = True

class Series(models.Model, HasWorkflow):
    class Meta:
        verbose_name = _('book series')
        verbose_name_plural = _('book series')

    import_id = models.CharField(max_length=100, blank=True)
    workflow_state = models.IntegerField(choices=WORKFLOW_STATE_CHOICES, default=DRAFT, null=True)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='title', editable=True)
    subtitle = models.CharField(max_length=200, blank=True)
    director = models.CharField(max_length=200, blank=True)
    format = models.CharField(max_length=200, blank=True)
    presentation = models.TextField(blank=True)

def author_slug(instance):
    return '%s %s' % (instance.family_name, instance.given_name)

class Author(models.Model, HasWorkflow):
    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    import_id = models.CharField(max_length=100, blank=True)
    workflow_state = models.IntegerField(choices=WORKFLOW_STATE_CHOICES, default=DRAFT, null=True)
    family_name = models.CharField(max_length=100)
    given_name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='author_slug', editable=True)
    presentation = models.TextField(blank=True)

    def get_full_name(self):
        return '%s, %s' % (self.family_name, self.given_name)

class Book(models.Model, HasWorkflow):
    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    import_id = models.CharField(max_length=100, blank=True)
    workflow_state = models.IntegerField(choices=WORKFLOW_STATE_CHOICES, default=DRAFT)
    publication_state = models.IntegerField(choices=PUBLICATION_STATE_CHOICES, default=IN_PRESS)
    series = models.ForeignKey(Series, related_name='series_books', blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='title', editable=True)
    subtitle = models.CharField(max_length=200, blank=True)
    presentation = models.TextField(blank=True)
    isbn = models.CharField(max_length=13, blank=True)
    pde = models.CharField(max_length=5, blank=True)
    year = models.CharField(max_length=100, blank=True)
    pages = models.CharField(max_length=100, blank=True)
    price = models.FloatField(default=0.0)
    small_image = models.ImageField(upload_to='small_images', blank=True)
    medium_image = models.ImageField(upload_to='medium_images', blank=True)
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))

AUTHOR = 1
EDITOR = 2
AUTHOR_ROLE_CHOICES = (
    (AUTHOR, _('Author')),
    (EDITOR, _('Editor')),)
AUTHOR_ROLE_DICT = dict(AUTHOR_ROLE_CHOICES)

class BookAuthor(models.Model):
    class Meta:
        verbose_name = _('book author relationship')
        verbose_name_plural = _('book author relationships')

    book = models.ForeignKey(Book, related_name='book_authors')
    author = models.ForeignKey(Author, related_name='author_books')
    role = models.IntegerField(choices=AUTHOR_ROLE_CHOICES, default=AUTHOR)
    role_prefix = models.CharField(max_length=100, blank=True)



