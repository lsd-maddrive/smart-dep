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





