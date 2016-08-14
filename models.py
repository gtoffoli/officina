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
    workflow_state = models.IntegerField(verbose_name='workflow', choices=WORKFLOW_STATE_CHOICES, default=DRAFT, null=True)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='title', editable=True)
    subtitle = models.CharField(max_length=200, blank=True)
    director = models.CharField(max_length=200, blank=True)
    format = models.CharField(max_length=200, blank=True)
    presentation = models.TextField(blank=True)

class Author(models.Model, HasWorkflow):
    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    import_id = models.CharField(max_length=100, blank=True)
    workflow_state = models.IntegerField(verbose_name='workflow', choices=WORKFLOW_STATE_CHOICES, default=DRAFT, null=True)
    family_name = models.CharField(max_length=100)
    given_name = models.CharField(max_length=100)
    # slug = AutoSlugField(unique=True, populate_from='get_full_name', editable=True)
    slug = AutoSlugField(unique=True, populate_from=('given_name', 'family_name',), editable=True)
    presentation = models.TextField(blank=True)
    books = models.ManyToManyField('Book', through='BookAuthor', blank=True)

    def get_full_name(self):
        return '%s, %s' % (self.family_name, self.given_name)

class Book(models.Model, HasWorkflow):
    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    import_id = models.CharField(max_length=100, blank=True)
    workflow_state = models.IntegerField(verbose_name='workflow', choices=WORKFLOW_STATE_CHOICES, default=DRAFT)
    publication_state = models.IntegerField(verbose_name='publication', choices=PUBLICATION_STATE_CHOICES, default=IN_PRESS)
    series = models.ForeignKey(Series, related_name='series_books', blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(unique=True, populate_from='title', editable=True)
    subtitle = models.CharField(max_length=300, blank=True)
    presentation = models.TextField(blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    pde = models.CharField(max_length=5, blank=True)
    year = models.CharField(max_length=100, blank=True)
    pages = models.CharField(max_length=100, blank=True)
    price = models.FloatField(default=0.0)
    small_image = models.ImageField(upload_to='small_images', blank=True)
    medium_image = models.ImageField(upload_to='medium_images', blank=True)
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))
    authors = models.ManyToManyField('Author', through='BookAuthor', blank=True)

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

    book = models.ForeignKey(Book, related_name='book_author')
    author = models.ForeignKey(Author, related_name='author_book')
    role = models.IntegerField(choices=AUTHOR_ROLE_CHOICES, default=AUTHOR)
    role_prefix = models.CharField(max_length=100, blank=True)

class Area(models.Model):
    class Meta:
        verbose_name = _('distribution area')
        verbose_name_plural = _('distribution areas')

    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='name', editable=True)
    distributors = models.ManyToManyField('Distributor', through='DistributorArea', blank=True)

class Distributor(models.Model, HasWorkflow):
    class Meta:
        verbose_name = _('distributor')
        verbose_name_plural = _('distributors')

    workflow_state = models.IntegerField(verbose_name='workflow', choices=WORKFLOW_STATE_CHOICES, default=DRAFT)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='title', editable=True)
    street_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    areas = models.ManyToManyField('Area', through='DistributorArea', blank=True)

class DistributorArea(models.Model):
    class Meta:
        verbose_name = _('distributor area')
        verbose_name_plural = _('distributor areas')

    distributor = models.ForeignKey(Distributor, related_name='distributor_area')
    area = models.ForeignKey(Area, related_name='area_distributor')



