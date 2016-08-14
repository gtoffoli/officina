# -*- coding: utf-8 -*-"""

import simplejson as json
from Products.CMFCore.utils import getToolByName

def export_images(self):
    pathname = 'C:/django19/oe_migration/images/'
    catalog = getToolByName(self, 'portal_catalog')
    export_dict = {}    
    image_list = []
    brains = catalog.searchResults(portal_type='Image')
    print len(brains), 'images'
    extensions = ['gif', 'jpg', 'jpeg', 'png',]
    for brain in brains:
        image = brain.getObject()
        id = image.id
        title = image.title
        image_dict = {
           'id': image.id,
           'title': image.title,
        }
        image_list.append(image_dict)
        splitted_title = title.split('.')
        try:
            if len(splitted_title) < 2 or splitted_title[-1] not in extensions:
                splitted_id = id.split('.')
                if len(splitted_id) > 1 and splitted_id[-1] in extensions:
                    title = '%s.%s' % (title, splitted_id[-1])
            data = image.data
            file = open(pathname+title, 'wb')
            file.write(data)
            file.close
        except:
            pass
        
    export_dict['images'] = image_list
    pretty = json.dumps(export_dict, indent=4, ensure_ascii=False)
    response = self.REQUEST.response
    response.setHeader("Content-type", "application/json; charset=utf-8")
    response.setHeader("Content-Disposition", "filename=officina.json")
    response.setHeader("Content-Transfer-Encoding", "8bit")
    return pretty

def export_catalog(self):
    # catalog = self.portal_catalog
    catalog = getToolByName(self, 'portal_catalog')
    export_dict = {}    

    author_list = []
    brains = catalog.searchResults(portal_type='IdrAuthor')
    print len(brains), 'authors'
    for brain in brains:
        author = brain.getObject()
        """
        references = object.getReferenceImpl('IdrIndividualAuthorship')
        target = reference.getTargetObject()
        """
        author_dict = {
           'id': author.id,
           'family_name': author.getFamily_name(),
           'given_name': author.getGiven_name(),
           'presentation': author.getAuthor_multi_desc().get('it', ''),
        }
        author_list.append(author_dict)
    export_dict['authors'] = author_list

    collection_list = []
    brains = catalog.searchResults(portal_type='IdrCollection')
    print len(brains), 'collections'
    for brain in brains:
        collection = brain.getObject()
        schema = collection.Schema()
        # print collection.Title()
        collection_dict = {
           'id': collection.id,
           'title': collection.Title(),
           'subtitle': collection.getMulti_subtitle().get('it', ''),
           'director': collection.getMulti_director().get('it', ''),
           'format': collection.getCollection_format(),
           'presentation': collection.getMultilanguage_pres().get('it', ''),
        }
        collection_list.append(collection_dict)
    export_dict['collections'] = collection_list

    item_list = []
    item_collection_relation_list = []
    item_author_relation_list = []
    brains = catalog.searchResults(portal_type='IdrItem')
    print len(brains), 'items'
    for brain in brains:
        item = brain.getObject()
        collection = item.getCollection() or None
        medium_image = item.get_medium_image(size='150')
        small_image = item.getSmallImage()
        big_image = item.getBigImage()
        item_dict = {
           'id': item.id,
           'title': item.Title(),
           'subtitle': item.getMulti_subtitle().get('it', ''),
           'presentation': item.getMulti_desc().get('it', ''),
           'isbn': item.getNumber_isbn(),
           'pde': item.getPde(),
           'year': item.getYears(),
           'pages': item.getPages().get('it', ''),
           'price': item.getPrice(),
           'small_image': small_image and small_image.id or '',
           'medium_image': medium_image and medium_image.id or '',
           'status': item.getItem_status(),
        }
        if big_image:
            item_dict['big_image'] = big_image.id
        item_list.append(item_dict)
        collection = item.getCollection()
        item_collection_dict =  {
           'item': item.id,
           'collection': collection.id,
        }
        item_collection_relation_list.append(item_collection_dict)
        refs = item.getReferenceImpl('IdrIndividualAuthorship')
        refs.sort(lambda x,y: cmp(getattr(x,'order',None), getattr(y,'order',None)))
        for ref in refs:
            author = ref.getTargetObject()
            content_object = ref.getContentObject()
            author_role = content_object.getAuthor_role()
            author_role_prefix = content_object.getAuthor_role_prefix(),
            author_role_prefix = (author_role_prefix and author_role_prefix[0].get('it', '')) or (author_role!='author' and 'a cura di') or ''
            item_author_dict =  {
               'item': item.id,
               'author': author.id,
               'author_role': author_role,
               'author_role_prefix': author_role_prefix,               
            }
            item_author_relation_list.append(item_author_dict)
    export_dict['items'] = item_list
    export_dict['item_collection_relations'] = item_collection_relation_list
    export_dict['item_author_relations'] = item_author_relation_list

    distributor_list = []
    brains = catalog.searchResults(portal_type='IdrDistributor')
    print len(brains), 'distributors'
    for brain in brains:
        distributor = brain.getObject()
        distributor_dict = {
           'id': distributor.id,
           'title': distributor.Title(),
           'area': distributor.getArea(),
           'street_address': distributor.getStreet_address(),
           'postal_code': distributor.getPostal_code(),
           'city': distributor.getCity(),
           'email': distributor.getEmail(),
           'fax': distributor.getFax(),
        }
        distributor_list.append(distributor_dict)
    export_dict['distributors'] = distributor_list

    pretty = json.dumps(export_dict, indent=4, ensure_ascii=False)
    response = self.REQUEST.response
    response.setHeader("Content-type", "application/json; charset=utf-8")
    response.setHeader("Content-Disposition", "filename=officina.json")
    response.setHeader("Content-Transfer-Encoding", "8bit")
    return pretty
