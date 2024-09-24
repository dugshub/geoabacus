from flask import render_template
from sqlalchemy import select

from app import app, db
from app.models import Neighbourhood, Locality, feature_schema, feature_collection,placetype_schema,placetypes_schema


def geojson_from_placetype_list(placetype_list=[],string=True):
    with app.app_context():
        placetype_dicts = [feature_schema.dump(placetype.to_geojson()) for placetype in placetype_list]

        feature_set = {"features": placetype_dicts}
        if string:
            geojson_export = feature_collection.dump(feature_set)
        else:
            geojson_export = feature_collection.dump(feature_set)

        return geojson_export


def get_neighbourhoods_from_locality(locality_id=101735835,string=True):
    with app.app_context():
        locality = db.session.get(Locality, locality_id)
        neighbourhoods = locality.neighbourhoods
        return geojson_from_placetype_list(neighbourhoods,string)


def get_all_neighbourhoods(string=True):
    with app.app_context():
        neighbourhoods = db.session.scalars(select(Neighbourhood)).all()
        neighbourhoods = geojson_from_placetype_list(neighbourhoods,string)

        return neighbourhoods

def get_all_localities(string=True):
    with app.app_context():
        localities = db.session.scalars(select(Locality)).all()
        return placetypes_schema.dump(localities)