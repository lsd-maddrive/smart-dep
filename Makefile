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

mg-init:	## Create environment for migration - do it only once
	python3 db/migration_manager.py db init --directory db/migrations

mg-migrate:	## Generate version-file in /migrations/versions
	python3 db/migration_manager.py db migrate --directory db/migrations

mg-migrate-msg:	## Generate version-file with message. Usage make mg-migrate-msg msg=''
	python3 db/migration_manager.py db migrate -m $(msg) --directory db/migrations

mg-upgrade:	## Apply the migration to the database
	python3 db/migration_manager.py db upgrade --directory db/migrations

# mg-docker:
