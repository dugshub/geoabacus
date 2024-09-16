import os

from geoalchemy2.types import Geometry
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Shapefile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    bbox: Mapped[str] = mapped_column()  #: Mapped[list] = mapped_column(nullable=False)
    geometry = db.Column(Geometry(geometry_type='NONE'))
    properties = None

    def __init__(self, id, bbox, geometry, properties=None):
        self.id = id
        self.bbox = ''.join(str(x) for x in bbox)
        self.geometry = geometry
        self.properties = properties

    def get_path_from_id(self):
        s = str(self.id)
        id_path = '/data/' + s[:3] + '/' + s[3:6] + '/' + s[6:9]
        if len(s) > 9:
            id_path += '/' + s[9:]
        return os.environ.get('WHOSONFIRST_PATH') + id_path + '/' + s + '.geojson'

#
# class PropertySchema(PropertiesSchema, ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Shapefile
#         unknown = INCLUDE
#
#
# class FeatureSchema(FeatureSchema, ma.SQLAlchemyAutoSchema):
#     class Meta:
#         unknown = INCLUDE
#         type = Str(
#             default='Feature',
#         )
#         properties = Nested(
#             nested=PropertySchema,
#             required=True,
#         )
#
#
# class GeoJSONSchema(GeoJSONSchema, ma.SQLAlchemyAutoSchema):
#     class Meta:
#         unknown = INCLUDE
#         feature_schema = FeatureSchema
#
#
# geojson_schema = GeoJSONSchema()
# property_schema = PropertySchema()
# feature_schema = FeatureSchema()
# features_schema = FeatureSchema(many=True)
