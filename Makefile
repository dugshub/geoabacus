IMAGE_NAME=geoabacus
TAG=latest

build:
	docker build -t ${IMAGE_NAME}:${TAG} .

rebuild-db:
	python setup.py

run:
	docker run ;\
	--name geoabacus ;\
	-e SQLITE_DATABASE_PATH=abacus.db ;\
	-e WHOSONFIRST_PATH=/Users/dug/projects/WhosOnFirstData/whosonfirst-data-admin-ca ;\
	-e WOF_COUNTRIES=["CA","US"] ;\
	-e WOF_DOWNLOAD_LINK=https://data.geocode.earth/wof/dist/sqlite/whosonfirst-data-admin-%s-latest.db.bz2 ;\
	-e WOF_DB_DIRECTORY=wof_datasets/ ;\
	-e WOF_SQLITE_PATH=wof_datasets/wof.db ;\
	  -p 8000:8000 ;\

