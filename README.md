# djangoTemplate

Tener en cuenta:

- Tutorial hecho el 2/10/2019
- Free tier de AWS
- Ubuntu 18.04
- Python 3
- Nginx
- Host Name [.tk](http://www.dot.tk). También revisar Freenom.
- [Documentación de Django, Nginx y Gunicorn](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
## 1 Creando el servido en AWS (EC2, Ubuntu)

### 1.1 Crear la instancia

1. Asumiendo que tenemos cuenta de AWS vamos a la [consola de AWS](https://console.aws.amazon.com/?nc2=h_m_mc)
2. Cliqueamos la instancia EC2
3. Creamos una instancia con "Launch Instance"
4. Seleccionamos la opción de Ubuntu 18.04
5. Escogemos el free tier (asuimendo que estamos desarrollando, en caso contrario ver un tutorial de aws)
6. Hacemos click en "Review and Launch"
7. Luego en "Launch". Esto te permitirá crear una 'key' para conectarse, que se ve en el siguiente punto

### 1.2 Crear y usar una key

1. Escoger 'Create a new key pair' y escribir un nombre para ella (por ejemplo tu típico username)
2. Cliquear en 'Download Key Pair'. Esto va a descargar la llave que luego servirá para conectarse al servidor desde tu computador
3. Cliquear en 'Launch Instances'
4. Ahora hay que esperar a que se cree la instancia. Para verla cliqueamos en 'View Instances'

### 1.3 Conectar al servidor

1. Una vez dentro de las intancias escogemos la que creamos. Y apretamos "Actions" y "Connect". Nos dirás las instrucciones para conectarse pero basicamente hay usar los siguientes comandos en la carpeta donde esté el archivo .pem (recomiendo copiar y pegar las instrucciones desde AWS):

    ```cmd
    chmod 400 nombre.pem
    ssh -i "nombre.pem" ubuntu@servidorQueTeDaran.compute.amazonaws.com
    ```

2. Escribir 'yes' y ya estamos dentro del servidor
3. (posiblemente no funcione después de crear IP elástica)

### 1.4.1 Crear Ip elástica (devuelta a la consola AWS)

Esto permite que si se modifica tu ip del servidor, no se tenga que reconfigurar el DNS de tu Host Name que crearemos más adelante.

1. En la barra de la consola ir a 'Elastic IPs'
2. Luego click en 'Allocate new adress'
3. 'Allocate'
4. Una vez creados volvemos a la pestaña inicial y vemos que se creo el IP elástico. Ahora cliqueamos en 'Actions' > 'Associate Adress'.
5. Seleccionamos la instancia y luego su IP.
6. Y aceptamos la asociación -> 'Associate'.

### 1.4.2 Conectar al servidor tras crear IP elática

1. Dentro de la carpeta que contiene el archivo .pem ahora podemos conectarnos con el siguiente comando

    ```cmd
    ssh -i "nombre.pem" ubuntu@ip-elastica
    ```

2. Escribir 'yes' y ya estamos dentro del servidor

3. (REALIZABLE LUEGO DE TENER HOST) Similarmente se puede conectar con el host:

    ```cmd
    ssh -i "nombre.pem" ubuntu@nombre-pagina.tk
    ```

### 1.5 Modificar grupos de seguridad

Esto permitirá poder conectarse al servidor en el puerto 80 y 8000 para testearlo. Además el puerto https 443.

1. En la barra de la consola ir a 'Security Groups'
2. Escoger la que se creo recientemente  e ir 'Actions' > 'Edit inbound rules'
3. 'Add rule'. Seleccionar type: HTTP (y deja el resto predeterminado).
4. Similarmente con HTTPS. 0.0.0.0/0, ::/8
5. Luego se agregar otra regla. Esta la dejamos en Type:'Custom TCP Rule' y cambiamos lo siguiente. Port Range: 8000 . Luego 'Save'.

## 2 Crear Host Name

1. Vamos a [dot.net](http://www.dot.tk)
2. Buscando un nombre que queramos y vemos si está disponible
3. Cliqueamos en 'Cosíguelo Ahora' y luego en 'Finalizar Compra'
4. Hacemos click en 'Continue'
5. Nos pedirá luego crear cuenta y/o rellenar información. Entonces  creamos una cuenta
6. Terminamos la orden (nos llegará un mail)

### 2.1 Ocupar DNS del Host Name

1. Como teníamos que crear una cuenta en Freenom, iniciamos sesión y vamos a 'Services' > 'My Domains'
2. Escogemos el dominio creado y hacemos click en 'Manage Domain'
3. Hacemos click en la pestaña 'Manage Freenom DNS'
4. Creamos dos 'Records':
    1. Name: vacío,  Type: A, TTL: Como viene (3600 en mi caso), Target: la ip elástica que definimos arriba.
    2. Name: WWW, Type: CNAME, TTL: lo mismo (3600), target: nombre-de-tu-dominio.extension (es el nombre de tu dominio y extesión, por ejemplo: mipagina.tk)
5. Verificar que se creó el Host Name a través de [Cuál es mi IP](https://whatismyipaddress.com/hostname-ip). Debes ingresar tu dominio y ver si retorna tu IP elástica.

## 3 Creando la app en el servidor

Estas son las variables que dependen de la implementación. Cambiar en todos los comandos y archivos que sea necesario.

**djangoTemplante** = nombre de la carpeta contenedora del proyecto

**myproject** = nombre del proyecto

**myprojectuser** = nombre del usuario de postgres

**password** = contraseña del usuario de postgres

**myprojectenv** = nombre del ambiente pip

**ubuntu** = nombre de usuario de la computadora

### 3.0 Clonamos el repo

```cmd
git clone https://github.com/jfbahamondes/djangoTemplate.git
```

Entramos a la carpeta y removemos .git

```cmd
cd djangoTemplate
rm -r .git
```

De esta manera podemos luego crear un nuevo repo para controlar las versiones del proyecto.

### 3.1 Instalación de paquetes de los repositorios de Ubuntu

```cmd
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
```

### 3.2 Crear PostgreSQL Base de Datos y Usuario

```cmd
sudo -u postgres psql
```

#### Luego en psql

Crear base de datos:

```psql
CREATE DATABASE myproject;
```

Crear Usuario con contraseña:

```psql
CREATE USER myprojectuser WITH PASSWORD 'password';
```

Definir utf-8 porque django lo espera. Bloqueamos lecturas no confirmadas. Y cambiamos la zona horaria.

```psql
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
```

Le damos privilegios de administrador a nuestra base de datos y salimos

```psql
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
\q
```

### 3.3 Instalamos dependencias de Python (virtual env)

```cmd
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
```

Dentro de la carpeta entonces creamos el ambiente y lo activamos

```cmd
virtualenv myprojectenv
source myprojectenv/bin/activate
```

#### Instalamos las dependencias entonces (se ocupa pip para pip y pip3 en el env)

```cmd
pip install django gunicorn psycopg2
```

#### Modificamos settings.py

Como ya tenemos un dominio, podemos agregarlo a la lista ALLOWED_HOSTS de django. De esta manera podremos luego probarla completamente subida.

```cmd
nano myproject/settings.py
```

#### Corremos las migraciones, y creamos un superuser

Migraciones

```cmd
python3 manage.py makemigrations
python3 manage.py migrate
```

Super Usuario

```cmd
python3 manage.py createsuperuser
```

Archivos estáticos

```cmd
python3 manage.py collectstatic
```

### 3.4 Permitir puerto 8000 y correr la app

```cmd
sudo ufw allow 8000
```

Probamos el servidor

```cmd
python3 manage.py runserver 0.0.0.0:8000
```

Chequear en [http://server_domain_or_IP:8000](http://localhost:8000)

Probamos el servidor análogamente con gunicorn

```cmd
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

Si todo está bien nos salimos del ambiente con el siguiente comando

```cmd
deactivate
```

## 4 Crear Gunicorn systemd Service File

Como el template viene con el archivo necesario, lo pueden modificar para adaptar o si tienen la configuración por defecto, sólo mover. Dentro de la carpeta donde se encuentre el archivo **gunicorn.service** ejecutar:

```cmd
sudo mv gunicorn.service /etc/systemd/system/gunicorn.service
```

Ahora podemos comenzar el servicio Gunicorn. Estos comandos deberían crear un archivo .sock en la carpeta del projecto:

```cmd
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

En caso de algún **error** se puede chequear los logs de Gunicorn con el comando:

```cmd
sudo journalctl -u gunicorn
```

Si se hace algún cambio (puede ser para corregir un error por ejemplo) del archivo  */etc/systemd/system/gunicorn.service* se puede reiniciar el proceso de Gunicorn:

```cmd
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

## 5 Configure Nginx de Proxy Pass a Gunicorn

Como el template viene con el archivo necesario, lo pueden modificar para adaptar o si tienen la configuración por defecto, sólo cambiar una línea y mover. Dentro de la carpeta donde se encuentre el archivo **myprojectNginx** ejecutar:

```cmd
nano myprojectNginx
```

**Cambiar la linea de *server_name***, donde se modifica *server_domain_or_IP* a cambio de tus Ips o Dominios, separados por una cosa. Luego se mueve el archivo:

```cmd
sudo mv myprojectNginx /etc/nginx/sites-available/myproject
```

Se activa ahora el sitio con la siguiente línea:

```cmd
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

En caso de algún **error** se puede chequear la configuración con el comando:

```cmd
sudo nginx -t
```

Si es que no hay errores se puede empezar el servicio con el comando:

```cmd
sudo systemctl restart nginx
```

Se abren los puertos necesarios de Nginx y se borra el 8000 de desarrollo.

```cmd
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

LISTO! En caso de algún error con Nginx se puede ver los últimos errores:

```cmd
sudo tail -F /var/log/nginx/error.log
```

### Finalmente

Si se cambia la app de Django

```cmd
sudo systemctl restart gunicorn
```

Si se cambia la configuración de Nginx, reiniciarla:

```cmd
sudo nginx -t && sudo systemctl restart nginx
```

## 6 Certificado HTTPS

### 6.1 Agregar Certbot PPP

```cmd
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
```

### 6.2 Instalar Certbot

```cmd
sudo apt-get install certbot python-certbot-nginx
```

### 6.3 Correr y modificar nginx con Cerbot

```cmd
sudo certbot --nginx
```

### 6.4 Renovar automáticamente el certificado

```cmd
sudo certbot renew --dry-run
```
