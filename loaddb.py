import time

import yaml
from sqlalchemy import select

import app.wof as wof
from app import app, db
from app.models import Shapefile, Locality, createShapefile

provided_cities = yaml.safe_load(open('locality_configs.yml'))['reporting_market']


def _load_supplied_cities():
    print('Loading cities from the list in the config file')
    wof_ids = []
    for city in provided_cities:
        wof_ids.append(city['id'])
    wof_ids = tuple(wof_ids)
    wof_items = wof.from_ids(wof_ids)

    with app.app_context() as session:
        query = select(Shapefile.id)
        existing_cities = db.session.scalars(query).all()
        for wof_item in wof_items:
            if wof_item.id not in existing_cities:
                db.session.add(createShapefile(wof_item))
        db.session.commit()


def _load_related_neighbourhoods(cities=None):
    print('Loading neighbourhoods for the provided cities')
    with app.app_context() as session:
        if cities is None:
            cities = db.session.scalars(select(Locality)).all()
            for city in cities:
                shapefiles = wof.get_related_placetypes(wof_ids=(city.id, ''),
                                                        placetypes=(
                                                            'neighbourhood', ''))
                for shapefile in shapefiles:
                    db.session.add(createShapefile(shapefile))
                db.session.commit()


def _load_placetypes(filtered_placetypes=('country', 'region', 'county')):
    print(f'Loading remaining placetypes: {filtered_placetypes} ')

    print('Gathering the Geojson files from the WhosOnFirst Database')
    shapefiles = wof.get_by_placetype(filtered_placetypes)
    print(f'Collected {len(shapefiles)} shapefiles. Preparing to load to the database')

    with app.app_context():
        count_shapefiles = len(shapefiles)
        for idx, shapefile in enumerate(shapefiles):
            db.session.add(createShapefile(shapefile))
        print(f'Created {count_shapefiles} Shapefile Objects. Saving to db. \nThis may take a while...')
        db.session.commit()


if __name__ == '__main__':
    start_time = time.time()
    with app.app_context():
        db.drop_all()
        db.create_all()
    _load_supplied_cities()
    lap1 = time.time()
    print(f'Completed in {'%.2f' % (lap1 - start_time)} seconds')
    _load_related_neighbourhoods()
    lap2 = time.time()
    print(f'Completed in {'%.2f' % (lap2 - start_time)} seconds')
    _load_placetypes(filtered_placetypes=('country', 'region', 'county'))
    print(f'Completed in {'%.2f' % (time.time() - lap2)} seconds')
    print(f'Database loading complete! Total time: {'%.2f' % (time.time() - start_time)}')
