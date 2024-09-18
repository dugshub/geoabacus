from geoalchemy2.types import Geometry, Geography
from marshmallow import EXCLUDE
from shapely.geometry import shape
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from marshmallow_sqlalchemy import ModelConverter
from marshmallow import fields

from app import db, ma

class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.Str
    })

class Shapefile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    placetype: Mapped[str]
    parent: Mapped[int]
    geojson: Mapped[str]
    ##bbox: Mapped[str] = mapped_column()  #: Mapped[list] = mapped_column(nullable=False)
    geometry = mapped_column(Geometry(geometry_type='GEOMETRY'))

class ShapefileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shapefile
        unknown = EXCLUDE
        model_converter = GeoConverter
        load_instance = True




def from_geojson(wof):
    bbox = wof.bbox
    properties = wof.properties
    geometry = shape(wof.geometry).wkt
    id = wof.id
