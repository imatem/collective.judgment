# -*- coding: utf-8 -*-
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

    def _hash(self, request):
        hash_ = md5()
        hash_.update(request.getClientAddr())
        for key in ["User-Agent", "Accept-Language",
                    "Accept-Encoding"]:
            hash_.update(request.getHeader(key))
        return hash_.hexdigest()

    def vote(self, vote, request):
        if self.already_voted(request):
            raise KeyError("You may not vote twice")
        vote = int(vote)
        self.annotations['voted'].append(self._hash(request))
        votes = self.annotations['votes']
        if vote not in votes:
            votes[vote] = 1
        else:
            votes[vote] += 1

    def average_vote(self):
        if not self.has_votes():
            return 0
        total_votes = sum(self.annotations['votes'].values())
        total_points = sum([vote * count for (vote, count) in
                            self.annotations['votes'].items()])
        return float(total_points) / total_votes

    def has_votes(self):
        return len(self.annotations.get('votes', [])) != 0

    def already_voted(self, request):
        return self._hash(request) in self.annotations['voted']

    def clear(self):
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict({'voted': PersistentList(),
                                           'votes': PersistentDict()})
        self.annotations = annotations[KEY]
