FROM python:3.12-bookworm
LABEL authors="dug"
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN apt-get update && apt-get install -y \
    libsqlite3-mod-spatialite
COPY app app
COPY migrations migrations
COPY shapes.py config.py setup.py boot.sh wof.db ./
RUN chmod a+x boot.sh

ENV FLASK_APP=shapes.py
ENV DATABASE_NAME=abacus
ENV SQLITE_DATABASE_PATH=/${DATABASE_NAME}.db
ENV WHOSONFIRST_PATH=/Users/dug/projects/WhosOnFirstData/whosonfirst-data-admin-ca
ENV MAPBOX_MAP_ID=""
ENV WOF_COUNTRIES=["CA","US"]
ENV WOF_DOWNLOAD_LINK=https://data.geocode.earth/wof/dist/sqlite/whosonfirst-data-admin-%s-latest.db.bz2
ENV WOF_DB_DIRECTORY=""
ENV WOF_SQLITE_PATH=${WOF_DB_DIRECTORY}wof.db

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]