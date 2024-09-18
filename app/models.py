from typing import Tuple

import geojson as gj
from geoalchemy2.types import Geometry
from marshmallow import EXCLUDE
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter
from shapely.geometry import shape
from sqlalchemy.orm import Mapped, mapped_column

from app import db, ma


class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.Str
    })


class Shapefile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    parent: Mapped[int]
    placetype: Mapped[str]
    name: Mapped[str]
    bbox: Mapped[str]
    bbox: Mapped[str] = mapped_column()  #: Mapped[list] = mapped_column(nullable=False)
    geometry: Mapped[Geometry] = mapped_column(Geometry(geometry_type='GEOMETRY'))


class ShapefileSchema(ma.SQLAlchemyAutoSchema):

    #geometry = fields.Method("_get_geometry")

    class Meta:
        model = Shapefile
        unknown = EXCLUDE
        model_converter = GeoConverter




def from_geojson(wof):
    bbox = wof.bbox
    properties = wof.properties
    geometry = shape(wof.geometry).wkt
    id = wof.id


shapefile_schema = ShapefileSchema()
shapefiles_schema = ShapefileSchema(many=True)
