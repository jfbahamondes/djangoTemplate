# djangoTemplate

## VARIABLES

myproject = nombre del proyecto
myprojectuser = nombre del usuario de postgres
password = contraseña del usuario de postgres

### 0 Clonamos el repo

```cmd
git clone https://github.com/jfbahamondes/djangoTemplate.git
```

### 1 Instalación de paquetes de los repositorios de Ubuntu

```cmd
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
```

### 2 Crear PostgreSQL Base de Datos y Usuario

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

### 3 Instalamos dependencias de Python (virtual env)

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

#### 4 Permitir puerto 8000

```cmd
sudo ufw allow 8000
```

Probamos el servidor

```cmd
python3 manage.py runserver 0.0.0.0:8000
```

Chequear en [http://server_domain_or_IP:8000](http://localhost:8000)
