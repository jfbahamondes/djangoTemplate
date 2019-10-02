# djangoTemplate

Tener en cuenta:

- Tutorial hecho el 2/10/2019
- Free tier de AWS
- Ubuntu 18.04
- Python 3
- Nginx
- Host Name [.tk](http://www.dot.tk). También revisar Freenom.

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

## 3 Creando la app

**myproject** = nombre del proyecto

**myprojectuser** = nombre del usuario de postgres

**password** = contraseña del usuario de postgres

### 3.0 Clonamos el repo

```cmd
git clone https://github.com/jfbahamondes/djangoTemplate.git
```

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

Creamos carpeta del proyecto y entramos

```cmd
mkdir ~/myproject
cd ~/myproject
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
