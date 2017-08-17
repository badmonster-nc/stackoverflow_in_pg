# Installation à partir des source sur Centos 7

Pour l'exemple, je veux installer une base de données postgresql 9.6.3 sur Centos 7\
Pg sera installé dans /opt/pgsql/9.6\
Mes données (PGDATA) seront dans /opt/pgsql/9.6/data\
Mes logs (PGLOG) seront dans /opt/pgsql/9.6/logs

### step 1: Télécharger les sources de postgresql
download link: https://ftp.postgresql.org/pub/source/v9.6.3/postgresql-9.6.3.tar.bz2

### step 2: Installer les pacquets nécessaires
```bash
yum install -y bison-devel readline-devel zlib-devel openssl-devel
yum groupinstall -y 'Development Tools'
```

### step 3: Création de l'utilistateur postgres avec pour homedir /opt/pgsql
```bash
sudo useradd -d /opt/pgsql -m -r -s /bin/bash postgres
```

### step 4: Déplacer les sources de postgres dans /opt/pgsql/src
```bash
sudo mkdir -p /opt/pgsql/src
sudo mv postgresql-9.6.3.tar.bz2 /opt/pgsql/src/postgresql-9.6.3.tar.bz2
sudo chown -R postgres:postgres /opt/pgsql/
```
### step 5: Se connecter avec l'utilisateur postgres
```bash
sudo su - postgres
```

### step 6: Exporter les variables PATH, LD\_LIBRARY, PGDATA, PGLOG dans  .bashrc_profile
```bash
#config postgres
export PATH=/opt/pgsql/9.6/bin:$PATH
export LD_LIBRARY_PATH=/opt/pgsql/9.6/lib:$LD_LIBRARY_PATH
export PGDATA=/opt/pgsql/9.6/data
export PDLOG=/opt/pgsql/9.6/data/serverlog
```
> You can these lines in your own .bashrc_profile 

### step 7: Décompresser les source postgresql
```bash
cd src/
tar -xvjf postgresql-9.6.3.tar.bz2 
```

### step 8: Installer pg à partir des sources
```bash
cd postgresql-9.6.3/
./configure --prefix /opt/pgsql/9.6
make
make install
```

### step 9: Initialiser la base pg
```bash
initdb -D $PGDATA -U postgres
```

### step 10: Paramétrage du service postgres pour le démarrage au boot

```bash
#avec un compte with a root/sudoer
sudo cp ~postgres/src/postgresql-9.6.3/contrib/start-scripts/linux /etc/init.d/postgresql
sudo chmod +x /etc/init.d/postgresql
```
modifier les variables prefix,PGDATA,PGUSER and PGLOG dans /etc/init.d/postgresql:
```bash
# Installation prefix
prefix=/opt/pgsql/9.6

# Data directory
PGDATA="/opt/pgsql/9.6/data"

# Who to run the postmaster as, usually "postgres".  (NOT "root")
PGUSER=postgres

# Where to keep a log file
PGLOG="$PGDATA/serverlog"
```

### step 11: démarrage du service
```bash
sudo chkconfig postgresql
sudo service postgresql start
```

### step 12: Tester de se connecter à la basel
```bash
sudo su - postgres
psql
```
> If you add this 
> `export PATH=/opt/pgsql/9.6/bin:$PATH`
> in your .bashrc, your can connect to postgres without change user like this\
> psql -U postgres 

### step 13 (facultatif): Installation de pgadmin4
```bash
sudo yum install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm
sudo yum install -y pgadmin4
```