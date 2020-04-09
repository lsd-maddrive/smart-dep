# .DEFAULT_GOAL := help

up:
	docker-compose up 

stop:
	docker-compose stop 

down:
	docker-compose down 

daemon:
	docker-compose up -d 