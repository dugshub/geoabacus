import bz2
import json
import os
import sqlite3
from pathlib import Path
import dotenv
import requests
from config import basedir

dotenv.load_dotenv()

wof_dir = f'{basedir}/{os.environ.get("WOF_DB_DIRECTORY")}'
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
    os.rename(largest_db, f'{basedir}/{os.environ.get("WOF_SQLITE_PATH")}')
    print(f'{basedir}/{os.environ.get("WOF_SQLITE_PATH")}')

def main():
    get_wof_dbs()
    create_wof_lookup()

if __name__ == '__main__':
    main()

