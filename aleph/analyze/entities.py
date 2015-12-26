import re
import logging
from collections import defaultdict

from aleph.core import db
from aleph.model import Reference, Selector
from aleph.analyze.analyzer import Analyzer

log = logging.getLogger(__name__)
BATCH_SIZE = 5000


class EntityAnalyzer(Analyzer):

    def compile(self, matcher):
        body = '|'.join(matcher.keys())
        return re.compile('( |^)(%s)( |$)' % body)

    def generate_matchers(self):
        matches = defaultdict(set)
        q = db.session.query(Selector.entity_id, Selector.text)
        for i, (entity_id, text) in enumerate(q.yield_per(self.BATCH_SIZE)):
            matches[text].add(entity_id)
            if i > 0 and i % self.BATCH_SIZE == 0:
                yield self.compile(matches), matches
                matches = defaultdict(set)
        if len(matches):
            yield self.compile(matches), matches

    @property
    def matchers(self):
        if not hasattr(self, '_matchers'):
            self._matchers = list(self.generate_matchers())
        return self._matchers

    def tag_text(self, text, entities):
        for rex, matches in self.matchers:
            for match in rex.finditer(text):
                _, match, _ = match.groups()
                for entity_id in matches.get(match, []):
                    entities[entity_id] += 1

    def analyze_text(self, document, meta):
        entities = defaultdict(int)
        for page in document.pages:
            self.tag_text(page.text, entities)
        self.save(document, meta, entities)

    def analyze_tabular(self, document, meta):
        entities = defaultdict(int)
        for table in document.tables:
            for row in table:
                for text in row.values():
                    self.tag_text(text, entities)
        self.save(document, meta, entities)

    def save(self, document, meta, entities):
        Reference.delete_document(document.id)
        for entity_id, weight in entities.items():
            ref = Reference()
            ref.document = document.id
            ref.entity_id = entity_id
            ref.weight = weight
            db.session.add(ref)
        super(EntityAnalyzer, self).save(document, meta)
