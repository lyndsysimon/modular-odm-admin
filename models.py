# todo: warn on no default, or something
# todo: get default collection name for picklestorage, mongostorage constructors
# todo: requirements.txt
# todo: distutils

import pprint

from modularodm import StoredObject
from modularodm.fields.StringField import StringField
from modularodm.fields.IntegerField import IntegerField
from modularodm.fields.FloatField import FloatField
from modularodm.fields.BooleanField import BooleanField
from modularodm.fields.DateTimeField import DateTimeField
from modularodm.fields.ForeignField import ForeignField
from modularodm.storage.PickleStorage import PickleStorage
from modularodm.storage.MongoStorage import MongoStorage
from modularodm.validators import *
from modularodm.query.querydialect import DefaultQueryDialect as Q

pp = pprint.PrettyPrinter(indent=4)

import random
import logging

logging.basicConfig(level=logging.DEBUG)

import os
try:os.remove('db_blog.pkl')
except:pass
try:os.remove('db_tag.pkl')
except:pass

class Tag(StoredObject):
    value = StringField(primary=True)
    count = StringField(default='c', validate=True)
    misc = StringField()
    misc2 = StringField()
    # created = DateTimeField(validate=True)
    # modified = DateTimeField(validate=True, auto_now=True)
    keywords = StringField(default=['keywd1', 'keywd2'], validate=[MinLengthValidator(5), MaxLengthValidator(10)], list=True)
    mybool = BooleanField(default=False)
    myint = IntegerField()
    myfloat = FloatField()

class Blog(StoredObject):
    _id = StringField(primary=True, optimistic=True)
    body = StringField(default='blog body')
    title = StringField(default='asdfasdfasdf', validate=MinLengthValidator(8))
    tag = ForeignField('Tag', backref='tagged')
    tags = ForeignField('Tag', list=True, backref='taggeds')
    _meta = {'optimistic':True}


# import pdb; pdb.set_trace()

# Tag.set_storage(MongoStorage(db, 'tag'))
# Blog.set_storage(MongoStorage(db, 'blog'))
Tag.set_storage(PickleStorage('tag'))
Blog.set_storage(PickleStorage('blog'))

t = Tag(value="tester")
t.save()

l = Tag(value="next")
l.save()

b = Blog(body="Hello world!", tag=t)
b.save()

# b2 = Blog(body="Goodbye world")
# b2.save()



