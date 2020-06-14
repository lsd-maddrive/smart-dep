.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

#-------------------------------------------------
# Control services via docker-compose
#-------------------------------------------------

dc-build:	## Build services (docker-compose)
	docker-compose -p local build

dc-daemon:	## Run services in detached mode
	docker-compose -p local up -d

dc-down:	## Stop and remove containers (docker-compose)
	docker-compose -p local down

dc-pull:	## Pulls an image associated with a service (in docker-compose.yml), but does not start containers.
	docker-compose -p local pull $(IMAGE)

dc-restart:	## Restarts all stopped and running services
	docker-compose -p local restart

dc-start:	## Starts existing containers for a service
	docker-compose -p local start

dc-status:	## List containers (docker-compose)
	docker-compose -p local ps

dc-stop:	## Stop running containers without removing them
	docker-compose -p local stop

dc-up:		## Builds, (re)creates, starts, and attaches to containers for a service
	docker-compose -p local up

#-------------------------------------------------
# Control migrations
#-------------------------------------------------

DB:=postgresql+psycopg2://admin:admin@localhost:5432/smart_dep
mgr-container:				## Build container
	docker build -t flask_migrations:latest -f db/Dockerfile .

mgr-migrate: mgr-container	## Make migrations
	docker run -v ${CURDIR}/db/migrations:/app/migrations \
				-e DB_URI=${DB} --network="host" \
				flask_migrations:latest \
				python3 migration_manager.py db migrate

mgr-upgrade: mgr-container	## Just upgrade DB
	docker run -v ${CURDIR}/db/migrations:/app/migrations \
				-e DB_URI=${DB} --network="host" \
				flask_migrations:latest \
				python3 migration_manager.py db upgrade

mgr-full: mgr-container mgr-migrate mgr-upgrade		## Full processing
