goworking-mesas
===

Sistema para controle das mesas do Go Working da Fábrica do Futuro.

Copyright (c) 2019 Iuri Guilherme, Fábrica do Futuro

v 0.1
---

Data de entrega: Sexta Feira, 06 de dezembro de 2019

### Escopo

* Ethiele deve conseguir visualizar as mesas do goworking;
* Ethiele deve conseguir visualizar quais cadeiras estão ocupadas, por quem, de que empresa;
* Ethiele deve conseguir editar informações sobre cadeiras, pessoas, empresas;

v 0.2
---

Data de entrega: Sexta Feira, 12 de dezembro de 2019

* Todos cadastros funcionando (habitantes e empresas, além de espaços, mesas e cadeiras);
* Atualizar dados não está funcionando corretamente. Para alterar informações é necessário recadastrar;

Instruções
---

Na eventualidade de algum dia alguém ler as instruções de instalação.  

### git

Clonar o repositório com o código fonte.  

    git clone https://notabug.org/fabricadofuturo/goworking-mesas.git

### Preparar Python e Flask

Eu uso *pipenv*. Como instalar pipenv está fora do escopo deste guia.  

    mkdir instance
    cp default_config.py instance/config.py
    cp default_env .env

Editar os arquivos `.env` e `instance/config.py` com os dados de configuração
do Flask, do SQLAlchemy, do WTForms, etc.  

O mínimo necessário é definir os dados do banco de dados. Por exemplo, no 
arquivo *.env*:  

    DATABASE_URL=mysql+pymysql://usuario:senha@localhost/goworking

    user@server:goworking-mesas$ pipenv install

### Banco de dados

É possível usar qualquer tipo de sistema gerenciador de banco de dados que 
funcione com o Flask SQL Alchemy. Estas instruções são para usar MariaDB:  

#### Instalar MariaDB Server

MariaDB é a versão GPL do MySQL.  
No debian: `sudo apt install mariadb-server`;  

#### Alterar usuário e senha

Alterar o arquivo de criação do banco de dados localizado em *doc/mysql.sql*:

    CREATE DATABASE goworking DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin;
    GRANT ALL PRIVILEGES ON goworking.* to usuario@'localhost' IDENTIFIED BY 'senha';

Mudar "usuario" para algum nome de usuário e "senha" para alguma senha.

#### Rodar script de criação

Acessar o mariadb-client, copiar e colar os comandos ou rodar o script.

No debian: `sudo mysql`

    MariaDB [(none)]> SOURCE doc/mysql.sql;
    Query OK, 1 row affected (0.001 sec)
    
    Query OK, 0 rows affected (0.001 sec)
    
    MariaDB [(none)]> SHOW DATABASES;
    +--------------------+
    | Database           |
    +--------------------+
    | goworking          |
    | information_schema |
    | mysql              |
    | performance_schema |
    +--------------------+
    4 rows in set (0.001 sec)

Se o que tiver disponível for um PHPMyAdmin ou coisa parecida, descobrir como é 
o jeito difícil de colar estes comandos simples nesse sistema complicado.  

#### flask-migrate

    user@server:goworking-mesas$ pipenv run flask db init
    Loading .env environment variables...
    user@server:goworking-mesas$ pipenv run flask db upgrade
    Loading .env environment variables...
    INFO  [alembic.runtime.migration] Context impl MySQLImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> fead50b08d21, empty message
    INFO  [alembic.runtime.migration] Running upgrade fead50b08d21 -> dc7d560eee94, empty message

### gunicorn

Eu uso systemd.  

Tem um arquivo do systemd de exemplo em *doc/gunicorn-goworking.service*.  

    user@server:goworking-mesas$ sudo cp gunicorn-goworking.service /lib/systemd/system/
    user@server:goworking-mesas$ sudo systemctl enable gunicorn-goworking.service
    user@server:goworking-mesas$ sudo systemctl start gunicorn-goworking.service

### Nginx

Arquivo de exemplo em *doc/goworking.conf*.  

    user@server:goworking-mesas$ sudo cp doc/goworking.conf /etc/nginx/sites-available/
    user@server:goworking-mesas$ pushd /etc/nginx/sites-enabled
    user@server:/etc/nginx/sites-enabled$ sudo ln -s ../sites-available/goworking.conf
    user@server:/etc/nginx/sites-enabled$ popd
    user@server:goworking-mesas$ sudo nginx -t
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful
    user@server:goworking-mesas$ sudo systemctl -l reload nginx.service

