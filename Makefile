.DEFAULT_GOAL := help

help:           
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

#-------------------------------------------------
# Control services via docker-compose
#-------------------------------------------------

dc-build:	## Build services (docker-compose)
	docker-compose build 

dc-daemon:	## Run services in detached mode 
	docker-compose up -d 

dc-down:	## Stop and remove containers (docker-compose)	
	docker-compose down 

dc-pull:	## Pulls an image associated with a service (in docker-compose.yml), but does not start containers.
	docker-compose pull $(IMAGE)

dc-restart:	## Restarts all stopped and running services
	docker-compose restart

dc-start:	## Starts existing containers for a service
	docker-compose start 

dc-status:	## List containers (docker-compose)
	docker-compose ps 

dc-stop:	## Stop running containers without removing them
	docker-compose stop 

dc-up:		## Builds, (re)creates, starts, and attaches to containers for a service
	docker-compose up 

#-------------------------------------------------
# Control migrations 
#-------------------------------------------------

mg-init:	## Create environment for migration - do it only once
	python3 shared/migration_manager.py db init

mg-migrate:	## Generate version-file in /migrations/versions
	python3 shared/migration_manager.py db migrate 

mg-migrate-msg:	## Generate version-file with message. Usage make mg-migrate-msg msg=''	
	python3 shared/migration_manager.py db migrate -m $(msg)

mg-upgrade:
	python3 shared/migration_manager.py db upgrade 