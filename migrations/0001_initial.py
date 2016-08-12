# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-10 16:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import officina.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_id', models.CharField(blank=True, max_length=100)),
                ('workflow_state', models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0, null=True)),
                ('family_name', models.CharField(max_length=100)),
                ('given_name', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='author_slug', unique=True)),
                ('presentation', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
            bases=(models.Model, officina.models.HasWorkflow),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_id', models.CharField(blank=True, max_length=100)),
                ('workflow_state', models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0)),
                ('publication_state', models.IntegerField(choices=[(0, 'Planned'), (1, 'In press'), (2, 'In distribution'), (3, 'Out of print')], default=1)),
                ('title', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title', unique=True)),
                ('subtitle', models.CharField(blank=True, max_length=200)),
                ('presentation', models.TextField(blank=True)),
                ('isbn', models.CharField(blank=True, max_length=13)),
                ('pde', models.CharField(blank=True, max_length=5)),
                ('year', models.CharField(blank=True, max_length=100)),
                ('pages', models.CharField(blank=True, max_length=100)),
                ('price', models.FloatField(default=0.0)),
                ('small_image', models.ImageField(blank=True, upload_to='small_images')),
                ('medium_image', models.ImageField(blank=True, upload_to='medium_images')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
            },
            bases=(models.Model, officina.models.HasWorkflow),
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Author'), (2, 'Editor')], default=1)),
                ('role_prefix', models.CharField(blank=True, max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_books', to='officina.Author')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_authors', to='officina.Book')),
            ],
            options={
                'verbose_name': 'book author relationship',
                'verbose_name_plural': 'book author relationships',
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_id', models.CharField(blank=True, max_length=100)),
                ('workflow_state', models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0, null=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title', unique=True)),
                ('subtitle', models.CharField(blank=True, max_length=200)),
                ('director', models.CharField(blank=True, max_length=200)),
                ('format', models.CharField(blank=True, max_length=200)),
                ('presentation', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'book series',
                'verbose_name_plural': 'book series',
            },
            bases=(models.Model, officina.models.HasWorkflow),
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='series_books', to='officina.Series'),
        ),
    ]
