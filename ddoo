IMAGE_NAME =geoabacus
TAG=latest
build:
    docker build -t geoabacus:latest . \

run:
    docker run \
        --name geoabacus \
          -e FLASK_APP=shapes.py \
          -e DATABASE_NAME=abacus \
          -e SQLITE_DATABASE_PATH=/abacus.db \
          -e WHOSONFIRST_PATH=/Users/dug/projects/WhosOnFirstData/whosonfirst-data-admin-ca \
          -e MAPBOX_MAP_ID="" \
          -e WOF_COUNTRIES='["CA","US"]' \
          -e WOF_DOWNLOAD_LINK=https://data.geocode.earth/wof/dist/sqlite/whosonfirst-data-admin-%s-latest.db.bz2 \
          -e WOF_DB_DIRECTORY="" \
          -e WOF_SQLITE_PATH=/wof.db \

          -p 8000:8000 \
