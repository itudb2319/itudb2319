up:
	docker-compose up

down:
	docker-compose down

down-volumes:
	docker-compose down -v

rmi:
	docker image rm itudb2319-app postgres rabbitmq:3-management

rm-app:
	docker image rm itudb2319-app

rm-db:
	docker image rm postgres

rm-rabbitmq:
	docker image rm rabbitmq:3-management