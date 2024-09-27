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
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.wof as wof
from app import db, ma
from config import placetype_hierarchy


class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.Str
    })


class Shapefile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    placetype: Mapped[str]
    bbox: Mapped[str] = mapped_column()  #: Mapped[list] = mapped_column(nullable=False)
    geom_type: Mapped[str] = mapped_column()
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
    hierarchy_parent_id: Mapped[int] = mapped_column(ForeignKey("locality.id"), nullable=True)

    locality = relationship('Locality', back_populates='neighbourhoods',
                            foreign_keys='Neighbourhood.hierarchy_parent_id')
    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "neighbourhood",
    }


class Locality(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"), primary_key=True)
    name: Mapped[str]
    hierarchy_parent_id: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=True)
    region = relationship('Region', back_populates='localities',
                          foreign_keys='Locality.hierarchy_parent_id')

    neighbourhoods = relationship("Neighbourhood", back_populates="locality",
                                  foreign_keys='Neighbourhood.hierarchy_parent_id')  # , lazy='selectin')

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
    hierarchy_parent_id: Mapped[int] = mapped_column(ForeignKey("country.id"), nullable=True)
    country = relationship('Country', back_populates='regions',
                           foreign_keys='Region.hierarchy_parent_id')

    localities = relationship("Locality", back_populates="region",
                              foreign_keys='Locality.hierarchy_parent_id')
    __mapper_args__ = {
        "polymorphic_on": "placetype",
        "polymorphic_identity": "region",
    }


class Country(Shapefile):
    id: Mapped[int] = mapped_column(ForeignKey("shapefile.id"), primary_key=True)
    name: Mapped[str]

    regions = relationship("Region", back_populates="country",
                           foreign_keys='Region.hierarchy_parent_id')
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
features_schema = FeatureSchema(many=True)


def createShapefile(shapefile):
    id = shapefile.id
    placetype = shapefile.properties.get('wof:placetype')
    bbox = "".join(str(shapefile.bbox))
    geom_type = shapefile.geometry.get('type')
    geometry = shapefile.geometry
    if geom_type == 'Point' and shapefile.properties.get('wof:geom_alt'):
            wof.from_ids(wof_ids=[id],include_alt_geom=True)
            geometry = shape(wof.from_ids(wof_ids=[id],include_alt_geom=True)[0].geometry).wkt
    else:
        geometry = shape(shapefile.geometry).wkt
    hierarchy = shapefile.properties.get('wof:hierarchy')[0]  # by deafault, we use the first hierarchy.

    # The following sets the 'parent layer' for the placetype in question. This is based on the hierarchy defined
    # in the config and .env file. This definition is necessary as these shapes do not have a defined hierchial order
    # (there are many correct answers).

    # The function finds the current layer eg. Neighbourhood in the hierarchy_tuple and takes the prior value in the
    # list. The list is ordered from top to bottom wrt lineage. (eg. Country = idx 0)

    if placetype in placetype_hierarchy and placetype_hierarchy.index(placetype) != 0:
        parent_layer = min(
            placetype_hierarchy[placetype_hierarchy.index(shapelayer) - 1] for shapelayer in placetype_hierarchy if
            shapelayer == placetype)
        parent_id = min(val for (key, val) in hierarchy.items() if parent_layer in key)

    match placetype:
        case 'locality':
            return Locality(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                geom_type=geom_type,
                name=shapefile.properties.get('wof:name'),
                hierarchy_parent_id=parent_id,
            )

        case 'neighbourhood':
            return Neighbourhood(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                geom_type=geom_type,
                name=shapefile.properties.get('wof:name'),
                hierarchy_parent_id=parent_id,
            )
        case 'county':
            return County(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                geom_type=geom_type,
                name=shapefile.properties.get('wof:name')
            )
        case 'region':
            return Region(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                geom_type=geom_type,
                name=shapefile.properties.get('wof:name'),
                hierarchy_parent_id=parent_id,
            )
        case 'country':
            return Country(
                id=id,
                placetype=placetype,
                bbox=bbox,
                geometry=geometry,
                geom_type=geom_type,
                name=shapefile.properties.get('wof:name')
            )



feature_collection = MyFeatureCollectionSchema()
features_collection = MyFeatureCollectionSchema(many=True)
shapefile_schema = ShapefileSchema()
shapefiles_schema = ShapefileSchema(many=True)

placetype_schema = ShapePropertySchema()
placetypes_schema = ShapePropertySchema(many=True)