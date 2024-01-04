up:
ifeq ($(DETACH),true)
	docker-compose up -d
else
	docker-compose up
endif


down:
	docker-compose down

down-volumes:
	docker-compose down -v

rmi:
	docker image rm web-app postgres rabbitmq:3-management

rm-app:
	docker image rm web-app

rm-db:
	docker image rm postgres

rm-rabbitmq:
	docker image rm rabbitmq:3-management
