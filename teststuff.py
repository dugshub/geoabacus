from sqlalchemy import select

from app import db,app
from app.models import Locality, Region, Neighbourhood, County, Country
import time

with app.app_context():
    print('Querying all objects')
    localities = db.session.scalars(select(Locality)).all()
    regions = db.session.scalars(select(Region)).all()
    counties = db.session.scalars(select(County)).all()
    countries = db.session.scalars(select(Country)).all()
    neighbourhoods = db.session.scalars(select(Neighbourhood)).all()

    print('Country Report:')
    for country in countries:
        print(f'{country.name}: has {len(country.regions)} regions')
        time.sleep(2)

    print('Locality Report:  Listing all localities and the count of neighbourhoods')
    for locality in localities:
        print(f'{locality.name}: has {len(locality.neighbourhoods)} neighbourhoods')
        time.sleep(0.2)

    print('Region Report:  Listing all regions and the count of localities')
    for region in regions:
        print(f'{region.name}: has {len(region.localities)} localities')
        time.sleep(0.2)

    print('Region Report:  Listing all counties')
    print('County Report:')
    for county in counties:
        print(county.name)
        time.sleep(0.05)



    for neighbourhood in neighbourhoods:
        print(neighbourhood.name)


