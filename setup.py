import bz2
import json
import os
import shutil
import sqlite3
import subprocess
import time

import dotenv
import requests
import yaml
from sqlalchemy import text, select

import app.wof as wof
from app import app, db
from app.models import createShapefile, Locality, Shapefile
from config import basedir

dotenv.load_dotenv(dotenv_path='.env_dev')

wof_dir = f'{os.environ.get("WOF_DB_DIRECTORY")}'
wof_sqlite_path = f'{os.environ.get("WOF_DB_DIRECTORY")}'
sqlite_db_path = f"{basedir}/databases/{os.environ.get('SQLITE_DATABASE_NAME')}"
provided_cities = yaml.safe_load(open('locality_configs.yml'))['reporting_market']


def get_wof_download_links():
    download_url = os.environ.get('WOF_DOWNLOAD_LINK')
    countries = json.loads(os.environ.get('WOF_COUNTRIES'))

    country_data = []
    for country in countries:
        url = download_url % country
        filename = f'{wof_dir}{url.split('/')[-1]}'
        temp_data = {"country": country, "url": url, "filename": filename}
        country_data.append(temp_data)

    return country_data


def get_wof_dbs():
    if not os.path.exists('wof_datasets'):
        os.makedirs('wof_datasets')

    country_data = get_wof_download_links()
    for country in country_data:
        print(f'Downloading {country["country"]} data... please wait')
        r = requests.get(country['url'], allow_redirects=True)
        with open(country['filename'], 'wb+') as f:
            f.write(r.content)
            print(f'Download complete. Extracting File.')

        with bz2.open(filename=country['filename'], mode="rb") as f:
            # Decompress data from file
            content = f.read()
            dbfile = country['filename'][:country['filename'].rfind('.bz2')]
            with open(dbfile, 'wb') as f:
                f.write(content)
                os.remove(country['filename'])
                print(f'Finished extracting file and removing zip.')


def create_wof_lookup():
    # iterate through the dbs and create a sorted list of tuples based on file size
    # This will allow us to add all values from the smaller dbs into the largest db

    dbs = [os.path.join(wof_dir, file) for file in os.listdir(wof_dir) if file.endswith(".db")]
    dbs = sorted(list(zip([os.path.getsize(dbs[idx]) for idx, path in enumerate(dbs)], dbs)))

    largest_db = dbs[-1][1]
    for db_size, db_path in dbs:
        if db_path == largest_db:
            continue
        con = sqlite3.connect(f"{largest_db}")
        con.execute(f"ATTACH '{db_path}' as dba")

        con.execute("BEGIN")
        for row in con.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
            combine = "INSERT INTO " + row[1] + " SELECT * FROM dba." + row[1]
            print(combine)
            con.execute(combine)
        con.commit()
        con.execute("detach database dba")

        print(f'Finished adding {db_path} records into {largest_db}.')
        print(f'Removing {db_path}.')
        os.remove(db_path)
    os.rename(largest_db, f'{os.environ.get("WOF_SQLITE_PATH")}')


def initialize_db():
    print('Initializing database... Running "Flask db init"')
    subprocess.run(["flask db init"], shell=True)

    print('Replacing default env.py migration script with GeoAlchemy2 compatible version')
    shutil.copyfile(f'setup/env_template.py', f'migrations/env.py')

    with app.app_context():
        print('Initializing geospatial capabilities on database')
        query = text('SELECT InitSpatialMetaData();')
        db.session.execute(query)

    print('Running "flask db migrate"')
    subprocess.run(["flask db migrate"], shell=True)

    print('Running "flask db upgrade"')
    subprocess.run(["flask db upgrade"], shell=True)


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


def _load_placetypes(filtered_placetypes=('country', 'region',  'county')):
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


def load_database():
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
    _load_placetypes(filtered_placetypes=('country', 'region'))#, 'county'))
    print(f'Completed in {'%.2f' % (time.time() - lap2)} seconds')
    print(f'Database loading complete! Total time: {'%.2f' % (time.time() - start_time)}')


def remove_db_files():
    if os.path.exists(sqlite_db_path):
        os.remove(sqlite_db_path)

    if os.path.exists('migrations'):
        shutil.rmtree('migrations')


def clean_install():
    remove_db_files()
    start_time = time.time()

    if not os.path.exists(wof_sqlite_path):
        print('Creating WOF database')
        get_wof_dbs()
        download_time = time.time() - start_time
        print(f'Completed downloads in {'%.2f' % (download_time)} seconds')
        create_wof_lookup()
        extraction_time = time.time() - download_time
        print(f'Completed creating singular wof lookup db in {'%.2f' % (extraction_time)} seconds')
    initialize_db()
    load_database()
    print(f'Completed initial setup in {'%.2f' % (time.time() - start_time)} seconds!')


def main():
    if not os.path.exists(sqlite_db_path):
        print('Performing Fresh Install')
        clean_install()

    else:
        print('Database found - skipping rebuild step. Performing db upgrade.')
        subprocess.run(["flask db upgrade"], shell=True)


if __name__ == '__main__':
    main()
