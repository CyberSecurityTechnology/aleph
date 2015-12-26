import logging

from aleph.core import db
from aleph.model.entity import Entity
from aleph.model.common import TimeStampedModel


log = logging.getLogger(__name__)


class Reference(db.Model, TimeStampedModel):
    id = db.Column(db.Integer(), primary_key=True)
    document_id = db.Column(db.BigInteger, db.ForeignKey('document.id'))
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    weight = db.Column(db.Integer)

    entity = db.relationship(Entity, backref=db.backref('tags',
                                                        lazy='dynamic'))

    @classmethod
    def delete_document(cls, document_id):
        q = db.session.query(cls)
        q = q.filter_by(document_id=document_id)
        q.delete()

    def __repr__(self):
        return '<Reference(%r, %r)>' % (self.document_id, self.entity_id)
