# -*- coding: utf-8 -*-"""

import os
import json
from decimal import Decimal
from .models import Series, Author, Book, BookAuthor, Area, Distributor, DistributorArea
from .models import IN_PRESS, IN_DISTRIBUTION, OUT_OF_PRINT
from .models import AUTHOR, EDITOR


def load_data():
    PROJECT_ROOT = os.path.dirname(__file__)
    BASE_DIR = os.path.dirname(PROJECT_ROOT)
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    IMPORT_PATH = os.path.join(MEDIA_ROOT, "oe_migration", "officina.json")
    f = open(IMPORT_PATH, encoding='utf8')
    s = f.read()
    f.close()
    data = json.loads(s)
    return data

def import_series(data):
    series_list = data['collections']
    for d in series_list:
        series = Series(import_id=d['id'], title=d['title'], subtitle=d['subtitle'], director=d['director'], format=d['format'], presentation=d['presentation'])
        series.save()
    print('series: ', len(series_list))

def import_authors(data):
    author_list = data['authors']
    for d in author_list:
        author = Author(import_id=d['id'], family_name=d['family_name'], given_name=d['given_name'], presentation=d['presentation'])
        author.save()
    print('authors: ', len(author_list))

publication_mapping = {
   '-': IN_DISTRIBUTION,
   'inpress': IN_PRESS,
   'new': IN_DISTRIBUTION,
   'low': IN_DISTRIBUTION,
   'outofprint': OUT_OF_PRINT,
}

def import_books(data):
    book_list = data['items']
    for d in book_list:
        publication_state = publication_mapping.get(d['status'], IN_DISTRIBUTION)
        pages = d['pages'][:100]
        price = d['price']
        if price is None: price = 0.0
        small_image = d['small_image']
        small_image = small_image and 'images/'+small_image or ''
        medium_image = d['medium_image']
        medium_image = medium_image and 'images/'+medium_image or ''
        # book = Book(import_id=d['id'], publication_state=publication_state, title=d['title'], subtitle=d['subtitle'], isbn=d['isbn'], pde=d['pde'], year=d['year'], pages=pages, price=price, small_image=d['small_image'], medium_image=d['medium_image'], presentation=d['presentation'])
        book = Book(import_id=d['id'], publication_state=publication_state, product_name=d['title'], subtitle=d['subtitle'], isbn=d['isbn'], pde=d['pde'], year=d['year'], pages=pages, unit_price=Decimal(price), description=d['presentation'], small_image=small_image, medium_image=medium_image)
        book.save()
    print('books: ', len(book_list))

def import_book_series_relationships(data):
    book_series_list = data['item_collection_relations']
    for d in book_series_list:
        book = Book.objects.get(import_id=d['item'])
        series = Series.objects.get(import_id=d['collection'])
        book.series = series
        book.save()
    print(len(book_series_list))

author_role_mapping = {
   'author': AUTHOR,
   'editor': IN_PRESS,
}

def import_book_author_relationships(data):
    book_author_list = data['item_author_relations']
    for d in book_author_list:
        book = Book.objects.get(import_id=d['item'])
        author = Author.objects.get(import_id=d['author'])
        role = author_role_mapping.get(d['author_role'])
        role_prefix = d['author_role_prefix']
        book_author = BookAuthor(book=book, author=author, role=role, role_prefix=role_prefix)
        book_author.save()
    print(len(book_author_list))

def import_distributors(data):
    distributors_list = data['distributors']
    for d in distributors_list:
        areas = d['area']
        for name in areas:
            if not Area.objects.filter(name=name):
                area = Area(name=name)
                area.save()
    for d in distributors_list:
        distributor = Distributor(title=d['title'], street_address=d['street_address'], postal_code=d['postal_code'], city=d['city'], email=d['email'], fax=d['fax'])
        distributor.save()
        areas = d['area']
        for name in areas:
            areas = Area.objects.filter(name=name)
            if areas:
                distributor_area = DistributorArea(distributor=distributor, area=areas[0])
                distributor_area.save()
    print(len(distributors_list))

def import_catalog():
    data = load_data()
    import_series(data)
    import_authors(data)
    import_books(data)
    import_book_series_relationships(data)
    import_book_author_relationships(data)
    import_distributors(data)

