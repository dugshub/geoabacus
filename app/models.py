from typing import Tuple

import geojson as gj
from geoalchemy2.types import Geometry
from marshmallow import EXCLUDE
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter
from shapely.geometry import shape
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app import db, ma


class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.Str
    })


class Shapefile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    placetype: Mapped[str]
    bbox: Mapped[str] = mapped_column()  #: Mapped[list] = mapped_column(nullable=False)
    geometry: Mapped[Geometry] = mapped_column(Geometry(geometry_type='GEOMETRY'))

    __mapper_args__ = {
        "polymorphic_on": "placetype",
    }

class Neighbourhood(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"),primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "neighbourhood",
    }
class Locality(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"),primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "locality",
    }

class County(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"),primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "county",
    }

class Region(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"),primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "region",
    }

class Country(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"),primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "country",
    }
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
