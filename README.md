# tarea2distribuidos

# Actividad 1
comandos:
docker-compose up //levanta arquitectura cliente servidor con 2 clientes
docker exec -it cliente1 bash //Crear un nuevo cliente que se conecta al servidor
docker attach [CONTAINER] // Se conecta a la terminal del container especificado (en este caso la de python que esta en ejecucion)

docker-compose run [CONTAINER] //Para crear un nuevo cliente en un nuevo container que se conectara al servidor ya creado


# Actividad 2
