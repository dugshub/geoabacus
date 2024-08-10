from string import capwords
from typing import Optional

from sqlalchemy.orm import Mapped
from app import db, ma
import lkml


class Dimension(db.Model):
    name: Mapped[str] = db.Column(db.String, nullable=False, primary_key=True)
    type: Mapped[str] = db.Column(db.String, nullable=False)
    primary_tag: Mapped[str] = db.Column(db.String, nullable=True)
    secondary_tag: Mapped[str] = db.Column(db.String, nullable=True)
    data_group: Mapped[str] = db.Column(db.String, nullable=True)
    label: Mapped[Optional[str]] = None

    def __init__(self, name: str, primary_tag: str, secondary_tag: str, data_group: str, type: str,
                 label: Optional[str] = None):
        self.name = name
        self.type = type
        self.primary_tag = primary_tag
        self.secondary_tag = secondary_tag
        self.data_group = data_group
        self.label = label or capwords(self.name.split('__')[-1].replace('_', ' '))

    def __repr__(self):
        return '<Dimension {}>'.format(self.name)


#
class DimensionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Dimension
        load_instance = True
        sqla_session = db.session


dimension_schema = DimensionSchema()
dimensions_schema = DimensionSchema(many=True)
