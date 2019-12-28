# Tarea 2

# Actividad 1
comandos:
docker-compose up //levanta arquitectura cliente servidor con 2 clientes
docker attach [CONTAINER] // Se conecta a la terminal del container especificado (en este caso la de python que esta en ejecucion)

docker-compose run [CONTAINER] //Para crear un nuevo cliente en un nuevo container que se conectara al servidor ya creado


# Actividad 2

Para levantar la arquitectura se debe usar el comando "docker-compose up", esto levanta el broker encargado de almacenar las colas de RabbitMQ, el servidor que se encarga del redireccionamiento de los mensajes, y dos clientes iniciales.

Para acceder a la consola de cada cliente predeterminado se deben abrir terminales distintas y escribir el comando "docker attach client1" y "docker attach client2", de esta manera se puede comenzar a interactuar en las consolas de cada cliente y realizar las acciones requeridas.

Para agregar nuevos clientes, en una nueva terminal se debe usar el comando "docker-compose run client1" para cada cliente nuevo. Esto creará automaticamente un nuevo cliente y abrirá la consola intectiva correspondiente.
