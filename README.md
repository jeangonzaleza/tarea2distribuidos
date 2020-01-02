# Tarea 2 - Distribuidos

### Integrantes:
-Christopher Gilbert 201573597-2\
-Jean González 201573517-4

## Actividad 1

Para levantar la arquitectura del chat desarrollado se debe utilizar el comando ``docker-compose up``, esto levantara el servidor y 2 clientes.

Para poder realizar el envio de mensajes es necesario conectarse a la consola de alguno de los clientes y para ello se utiliza el comando ``docker attach [Container]``
donde "Container" debe ser reemplazado por "cliente1" o "cliente2" en caso de utilizar los clientes que se levantaron con el servidor.

En caso de necesitar un cliente nuevo, es posible crear uno nuevo utilizando el comando ``docker-compose run cliente1``. Con esto el cliente recibira su id que correspondera al primer mensaje que imprime para luego desplegar el menu para elegir una acción.

Para el envio de mensajes de los 2 clientes creados juntos con el servidor es necesario prestar atencion a la consola donde fue ejecutado el comando ``docker-compose up`` ya que es ahi donde se imprimira inicialmente los mensajes a los clientes y por lo tanto el mensaje de asignacion de id.


## Actividad 2

Para levantar la arquitectura se debe usar el comando ``docker-compose up``, esto levanta el broker encargado de almacenar las colas de RabbitMQ, el servidor que se encarga del redireccionamiento de los mensajes, y dos clientes iniciales.

Si el Broker de RabbitMQ no está disponible, ya sea por algun error o porque aún no termina de iniciar el levantamiento, el servidor y los clientes fallarán a la hora de intentar conectarse, tras esto esperan cinco segundos y vuelven a intentarlo hasta que se logre entablar comunicación con RabbitMQ, esto se hace puesto que el broker se demora en iniciar cuando se levanta por primera vez con ``docker-compose up``.

Para acceder a la consola de cada cliente predeterminado se deben abrir terminales distintas y escribir el comando ``docker attach client1`` y ``docker attach client2``, de esta manera se puede comenzar a interactuar en las consolas de cada cliente y realizar las acciones requeridas.

Para agregar nuevos clientes, en una nueva terminal se debe usar el comando ``docker-compose run client1`` para cada cliente nuevo. Esto creará automaticamente un nuevo cliente y abrirá la consola intectiva correspondiente.
