#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from .index import CanopyIndex
import collections
import itertools
import transaction

logger = logging.getLogger(__name__)

class TfIdfIndex(object) :
    def __init__(self, stop_words=[], name=None) :
        import ZODB, ZODB.FileStorage
        storage = ZODB.FileStorage.FileStorage('mydata' + name + '.fs')
        db = ZODB.DB(storage)
        connection = db.open()
        self.root = connection.root
        
        
        self.root._index = CanopyIndex(stop_words)
 
        try : # py 2
            self._doc_to_id = collections.defaultdict(itertools.count(1).next)
        except AttributeError : # py 3
            self._doc_to_id = collections.defaultdict(itertools.count(1).__next__)

        
        self._parseTerms = self.root._index.lexicon.parseTerms

    def index(self, doc) :
        i = self._doc_to_id[doc]
        self.root._index.index_doc(i, doc)
        
    def unindex(self, doc) :
        i = self._doc_to_id.pop(doc)
        self.root._index.unindex_doc(i)
        self.initSearch()

    def initSearch(self) :
        self.root._index.initSearch()

    def search(self, doc, threshold=0) :
        query_list = self._parseTerms(doc)
 
        if query_list :
            results = [center for score, center 
                       in self.root._index.apply(query_list, threshold)]
        else :
            results = []

        return results

