from geoalchemy2.types import Geometry
from marshmallow import EXCLUDE
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter
from shapely.geometry import shape
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app import db, ma
import geojson


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


class ShapefileSchema(ma.SQLAlchemyAutoSchema):
    # geometry = fields.Method("_get_geometry")
    class Meta:
        model = Shapefile
        unknown = EXCLUDE
        model_converter = GeoConverter


class Neighbourhood(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"), primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "neighbourhood",
    }


class Locality(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"), primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "locality",
    }


class County(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"), primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "county",
    }


class Region(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"), primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "region",
    }


class Country(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"), primary_key=True)
    name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "country",
    }


def createShapefile(shapefile):
    id = shapefile.id
    placetype = shapefile.properties.get('wof:placetype')
    bbox = "".join(str(shapefile.bbox))
    geometry = shape(shapefile.geometry).wkt

    match placetype:
        case 'locality':
            return Locality(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                name=shapefile.properties.get('wof:name')
            )

        case 'neighbourhood':
            return Neighbourhood(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                name=shapefile.properties.get('wof:name')
            )
        case 'county':
            return County(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                name=shapefile.properties.get('wof:name')
            )
        case 'region':
            return Region(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                name=shapefile.properties.get('wof:name')
            )
        case 'country':
            return Country(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                name=shapefile.properties.get('wof:name')
            )


shapefile_schema = ShapefileSchema()
shapefiles_schema = ShapefileSchema(many=True)
