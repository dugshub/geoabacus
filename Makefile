IMAGE_NAME=geoabacus
TAG=latest

SQLITE_DATABASE_PATH=abacus.db

##MOUNTS###
WOF_DATASET_MOUNT=/Users/dug/projects/geoabacus/wofdata/wof
SQLITE_DATABASE_MOUNT=/Users/dug/projects/geoabacus/wofdata/abacus

WHOSONFIRST_PATH=/Users/dug/projects/WhosOnFirstData/whosonfirst-data-admin-ca
WOF_COUNTRIES='["CA","US"]'
WOF_DOWNLOAD_LINK=https://data.geocode.earth/wof/dist/sqlite/whosonfirst-data-admin-%s-latest.db.bz2
WOF_DB_DIRECTORY=wof_datasets/
WOF_SQLITE_PATH=wof_datasets/wof.db

.PHONY: build-image
build-image:
	echo "building image" && \
	docker build \
		--no-cache \
		-f ./Dockerfile \
		-t ${IMAGE_NAME}:${TAG} . \

rebuild-db:
	python setup.py

.PHONY: docker-run
docker-run:
	docker run --name ${IMAGE_NAME} \
		-d \
		-p 8000:8000 \
		-v ${WOF_DATASET_MOUNT}:/${WOF_DB_DIRECTORY} \
		-v ${SQLITE_DATABASE_MOUNT}:/${SQLITE_DATABASE_PATH} \
		--env SQLITE_DATABASE_PATH=${SQLITE_DATABASE_PATH} \
		--env WHOSONFIRST_PATH=${WHOSONFIRST_PATH} \
		--env WOF_COUNTRIES=${WOF_COUNTRIES} \
		--env WOF_DOWNLOAD_LINK=${WOF_DOWNLOAD_LINK} \
		--env WOF_DB_DIRECTORY=${WOF_DB_DIRECTORY} \
		--env WOF_SQLITE_PATH=${WOF_SQLITE_PATH} \
		--rm ${IMAGE_NAME}:${TAG} \
