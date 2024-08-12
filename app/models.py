from string import capwords
from typing import Optional

from sqlalchemy.orm import Mapped
from app import db, ma
from marshmallow import fields
from typing import List
import lkml


class DimensionTags(db.Model):
    id: Mapped[int] = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = db.Column(db.String, db.ForeignKey('dimension.name'), nullable=False)
    primary_tag: Mapped[Optional[str]] = db.Column(db.String, nullable=True)
    secondary_tag: Mapped[Optional[str]] = db.Column(db.String, nullable=True)
    data_group: Mapped[[Optional[str]]] = db.Column(db.String, nullable=True)

    def __init__(self, name: str, primary_tag: Optional[str], secondary_tag: Optional[str], data_group: Optional[str]):
        self.name = name
        self.primary_tag = primary_tag
        self.secondary_tag = secondary_tag
        self.data_group = data_group

    def __repr__(self):
        return '<DimensionTag{}>'.format(self.name, self.primary_tag, self.secondary_tag, self.data_group)


class DimensionTagsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DimensionTags
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Dimension(db.Model):
    name: Mapped[str] = db.Column(db.String, nullable=False, primary_key=True)
    type: Mapped[str] = db.Column(db.String, nullable=False)
    label: Mapped[Optional[str]] = None
    description: Mapped[Optional[str]] = None
    qualifiedName: Mapped[Optional[str]] = db.Column(db.String, nullable=True)

    dimensionTags = db.relationship('DimensionTags', backref='dimension', uselist=False)

    def __init__(self, name: str, type: str, label: Optional[str] = None, description: Optional[str] = None
                 , qualifiedName: Optional[str] = None):
        self.name = name
        self.type = type
        self.label = label or capwords(self.name.split('__')[-1].replace('_', ' '))
        self.description = description
        self.qualifiedName = qualifiedName

    def __repr__(self):
        return '<Dimension {}>'.format(self.name)


#
class DimensionSchema(ma.SQLAlchemyAutoSchema):
    # queryableGranularities = fields.List(fields.Str() or None)
    class Meta:
        model = Dimension
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    dimensionTags = fields.Nested("DimensionTagsSchema", many=False)


dimension_schema = DimensionSchema()
dimensions_schema = DimensionSchema(many=True)
dimension_tag_schema = DimensionTagsSchema()
dimension_tags_schema = DimensionTagsSchema(many=True)
