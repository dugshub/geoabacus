from sqlalchemy.orm import Mapped
from app import db


class Dimension(db.Model):
    name: Mapped[str] = db.Column(db.String, nullable=False, primary_key=True)
    primary_tag: Mapped[str] = db.Column(db.String, nullable=True)
    secondary_tag: Mapped[str] = db.Column(db.String, nullable=True)
    data_group: Mapped[str] = db.Column(db.String, nullable=True)

    def __init__(self, name: str, primary_tag: str, secondary_tag: str, data_group: str):
        self.name = name
        self.primary_tag = primary_tag
        self.secondary_tag = secondary_tag
        self.data_group = data_group

    def __repr__(self):
        return '<Dimension {}>'.format(self.name)

#
# class DimensionSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Dimension
#         load_instance = True
#         sqla_session = db.session
#
#
# dimension_schema = DimensionSchema()
# dimensions_schema = DimensionSchema(many=True)
