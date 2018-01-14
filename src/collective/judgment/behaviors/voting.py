from hashlib import md5
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations


KEY = "collective.judgment.behaviors.voting.Vote"


class Vote(object):
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if KEY not in annotations.keys():
            annotations[KEY] = PersistentDict({
                'voted': PersistentList(),
                'votes': PersistentDict(),
            })
        self.annotations = annotations[KEY]

    @property
    def votes(self):
        return self.annotations['votes']

    @property
    def voted(self):
        return self.annotations['voted']
