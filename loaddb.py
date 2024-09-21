from app import app, db
from app.models import Shapefile, Locality, shapefile_schema
import app.wof as wof
import geojson
from shapely.geometry import shape
from geoalchemy2.shape import to_shape
from sqlalchemy import text, select
import yaml

cities = yaml.safe_load(open('locality_configs.yml'))['reporting_market']

wof_ids = []

for city in cities:
    wof_ids.append(city['id'])
wof_ids = tuple(wof_ids)
wof_items = wof.from_ids(wof_ids)

with app.app_context() as session:

    with app.app_context() as session:
        query = select(Shapefile.id)
        existing_cities = db.session.scalars(query).all()

        for wof_item in wof_items:
            if wof_item.id not in existing_cities:
                db.session.add(
                    Locality(
                        id=wof_item.id,
                        name=wof_item.name,
                        placetype=wof_item.placetype,
                        geometry=shape(geojson.loads(wof_item.geojson).geometry).wkt,
                        bbox="".join(str(geojson.loads(wof_item.geojson).bbox))
                    )
                )
        db.session.commit()

