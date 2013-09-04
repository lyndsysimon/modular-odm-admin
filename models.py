# todo: warn on no default, or something
# todo: get default collection name for picklestorage, mongostorage constructors
# todo: requirements.txt
# todo: distutils

import pprint

from modularodm import fields
from modularodm import StoredObject
from modularodm.storage.picklestorage import PickleStorage
from modularodm.validators import *
from modularodm.query.querydialect import DefaultQueryDialect as Q

pp = pprint.PrettyPrinter(indent=4)

import random
import logging
debug = True

logging.basicConfig(level=logging.DEBUG)
if debug:
    import os
    for f in ('team','manager','player'):
        try:
            os.remove('db_{}.pkl'.format(f))
        except OSError:
            pass


class Team(StoredObject):
    name = fields.StringField(primary=True)
    owner = fields.ForeignField('Manager', backref='owns')
    wins = fields.IntegerField(list=True)
    playoffs = fields.BooleanField(default=None, list=True)
    schedule = fields.StringField(list=True)
    players = fields.ForeignField('Player', list=True, backref='plays_for')


class Manager(StoredObject):
    name = fields.StringField(primary=True)
    players_managed = fields.ForeignField('Player', list=True, backref='managed_by')


class Player(StoredObject):
    name = fields.StringField(primary=True)
    number = fields.IntegerField()
    rating = fields.FloatField(default=0.0)
    injured = fields.BooleanField(default=False)

Team.set_storage(PickleStorage('team'))
Manager.set_storage(PickleStorage('manager'))
Player.set_storage(PickleStorage('player'))

if debug:
    d = Player(name="Griffin", number=10, rating=85.0, injured=True)
    d.save()

    e = Player(name="Morris", number=46, rating=80.2, injured=False)
    e.save()

    f = Player(name="Moss", number=89, rating=82.7, injured=False)
    f.save()

    g = Player(name="Tannehill", number=17, rating=75.0, injured=False)
    g.save()

    h = Player(name="Wallace", number=11, rating=80.0, injured=False)
    h.save()

    i = Player(name="Wake", number=91, rating=84.4, injured=False)
    i.save()

    j = Player(name="Cutler", number=6, rating=70.2, injured=False)
    j.save()

    k = Player(name="Marshall", number=15, rating=77.0, injured=False)
    k.save()

    l = Player(name="Collins", number=93, rating=72.4, injured=False)
    l.save()

    a = Manager(name="finsfan", players_managed=[d, g, h, i])
    a.save()

    b = Manager(name="skinsfan", players_managed=[d, e, f])
    b.save()

    c = Manager(name="bearsfan", players_managed=[j, k, l])
    c.save()

    m = Team(
        name="FinsRock",
        owner=a,
        wins=[3, 1, 2],
        playoffs=[True, False, True],
        schedule=["Home", "Away", "Away"],
        players=[d, g, h, i]
    )
    m.save()

    n = Team(
        name="SkinsRock",
        owner=b,
        wins=[2, 0, 1],
        playoffs=[True, False, False],
        schedule=["Home", "Away", "Home"],
        players=[d, e, f]
    )
    n.save()

    o = Team(
        name="BearsRock",
        owner=c,
        wins=[3, 1, 4],
        playoffs=[False, False, False],
        schedule=["Away", "Away", "Home"],
        players=[j, k, l]
    )
    o.save()