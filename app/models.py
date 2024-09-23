import geojson
from geoalchemy2.shape import to_shape
from geoalchemy2.types import Geometry
from marshmallow import EXCLUDE
from marshmallow import fields
from marshmallow.fields import List
from marshmallow_geojson import PropertiesSchema, FeatureSchema, GeoJSONSchema, FeatureCollectionSchema
from marshmallow_geojson.examples import GEOJSON_FEATURE_COLLECTION
from marshmallow_sqlalchemy import ModelConverter
from marshmallow_sqlalchemy.fields import Nested
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

    def to_geojson(self):
        properties = {
            "id": self.id,
            "name": self.name,
            "placetype": self.placetype,
        }

        return geojson.Feature(geometry=to_shape(self.geometry), properties=properties)


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


class ShapePropertySchema(PropertiesSchema):
    name = fields.Str()
    id = fields.Integer()
    placetype = fields.Str()

    class Meta:
        unknown = EXCLUDE


class ShapeFeatureSchema(FeatureSchema):
    type = fields.Str(default="Feature")
    properties = Nested(
        nested=ShapePropertySchema,
        required=True,
    )

    class Meta:
        unknown = EXCLUDE


class MyGeoJSONSchema(GeoJSONSchema):
    feature_schema = ShapeFeatureSchema(many=True)


#
# class GeoJSONSchema(GeoJSONSchema, ma.SQLAlchemyAutoSchema):
#     class Meta:
#         unknown = INCLUDE
#         feature_schema = FeatureSchema
#
#
class MyFeatureCollectionSchema(FeatureCollectionSchema):
    type = fields.Str(default="FeatureCollection")

    features = List(
        Nested(ShapeFeatureSchema()),
        required=True,
        metadata=dict(example=GEOJSON_FEATURE_COLLECTION["features"]),
    )

geojson_schema = MyGeoJSONSchema()
property_schema = ShapePropertySchema()

feature_schema = ShapeFeatureSchema()


# features_schema = FeatureSchema(many=True)

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

feature_collection = MyFeatureCollectionSchema()
shapefile_schema = ShapefileSchema()
shapefiles_schema = ShapefileSchema(many=True)
