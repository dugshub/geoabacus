from geojson import dump
from sqlalchemy import select

from app import app, db
from app.models import Neighbourhood, feature_schema, feature_collection

with app.app_context():
    neighbourhoods = db.session.scalars(select(Neighbourhood)).all()
    country = db.session.scalar(select(Neighbourhood))
    country2 = db.session.scalar(select(Neighbourhood))
    countries = [country, country2]
    countz = [feature_schema.dump(country.to_geojson()) for country in countries]

    neighz = [feature_schema.dump(neighbourhood.to_geojson()) for neighbourhood in neighbourhoods]
    print(neighz)
    final = {"features": countz}
    nei = {"features": neighz}

    final = feature_collection.dumps(final)
    n = feature_collection.dump(nei)
with open('myfile.geojson', 'w') as f:
    dump(n, f)
