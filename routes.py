import yaml
from geoalchemy2 import functions
from sqlalchemy import select, text, func

from app import app, db, wof, models
from app.models import Locality, feature_schema, feature_collection, placetypes_schema, Neighbourhood, Shapefile


def geojson_from_placetype_list(placetype_list=[], string=True):
    with app.app_context():
        placetype_dicts = [feature_schema.dump(placetype.to_geojson()) for placetype in placetype_list]

        feature_set = {"features": placetype_dicts}
        if string:
            geojson_export = feature_collection.dump(feature_set)
        else:
            geojson_export = feature_collection.dump(feature_set)

        return geojson_export


def get_neighbourhoods_from_locality(locality_id=101735835, string=True):
    with app.app_context():
        locality = db.session.get(Locality, locality_id)
        neighbourhoods = locality.neighbourhoods
        return geojson_from_placetype_list(neighbourhoods, string)


def random_custom_pulls(string=True, excluded_shapes=['dug']):
    query = text('''
                select body from spr
                left join geojson on spr.id = geojson.id
                where spr.id in (select id from ancestors where ancestor_id = 101732987) and
                placetype = 'neighbourhood'
                ''')

    query = text('''
                select body from spr
                left join geojson on spr.id = geojson.id
                where spr.id in (select id from ancestors where ancestor_id = 102086957) and
                placetype = 'locality' and is_current
                    ''')

    query = text('''select body from spr
         left join geojson on spr.id = geojson.id
where spr.id in (select id from ancestors where ancestor_id = 101732987) and
      placetype = 'neighbourhood' and is_alt = 0  -- and is_current;
      ''')

    geojson_list = wof.from_query(query)
    placetypes = models.create_shapefiles(geojson_list, excluded_shapes)
    #  return placetypes

    geojsons = wof.get_related_placetypes(wof_ids=(102081111, ''), placetypes=('locality', ''))
    # placetypes = models.create_shapefiles(geojson_list)
    return geojson_from_placetype_list(placetypes)


def get_all_localities(string=True):
    with app.app_context():
        localities = db.session.scalars(select(Locality)).all()
        return placetypes_schema.dump(localities)


def from_ids():
    yam = yaml.safe_load(open('location_configs.yml'))
    wof_ids = []
    for market in yam['reporting_market']:
        if market.get('localities_as_neighbourhoods'):
            wof_ids += [value for key, value in market['localities_as_neighbourhoods'].items() if
                        market.get('localities_as_neighbourhoods')]
    geojson_files = wof.from_ids(wof_ids)
    placetype_list = models.create_shapefiles(geojson_files)
    return geojson_from_placetype_list(placetype_list)


def get_all_neighbourhoods():
    with app.app_context():
        neighbourhoods = db.session.scalars(select(Neighbourhood)).all()
        return geojson_from_placetype_list(neighbourhoods)


def map_point(lon, lat):
    point = functions.ST_Point(lon, lat)
    with app.app_context():
        query = (
            select(Shapefile.id)
            .where(
                    func.ST_Contains(Shapefile.geometry, point)
            )
        )
        results = db.session.scalars(query)
        return [result for result in results]

def map_points(points: [tuple()]):
    return [map_point(point[0], point[1]) for point in points]
