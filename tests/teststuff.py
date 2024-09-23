from sqlalchemy import select

from app import db,app
from app.models import Locality, Region, Neighbourhood, County, Country

with app.app_context():
    localities = db.session.scalars(select(Locality)).all()
    regions = db.session.scalars(select(Region)).all()
    counties = db.session.scalars(select(County)).all()
    countries = db.session.scalars(select(Country)).all()
    neighbourhoods = db.session.scalars(select(Neighbourhood)).all()

    for locality in localities:
        print(locality.name)

    for region in regions:
        print(region.name)

    for county in counties:
        print(county.name)

    for country in countries:
        print(country.name)

    for neighbourhood in neighbourhoods:
        print(neighbourhood.name)


