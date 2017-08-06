#Ubuntu from source on Ubuntu 16.04
For this example, I want to install postgresql 9.6.3 on xubuntu 16.04.
I want install pg in /opt/pgsql/9.6
my data is here: /opt/pgsql/9.6/data
my logs are here: /opt/pgsql/9.6/logs

###step 1:Download postgres source 
download link: https://ftp.postgresql.org/pub/source/v9.6.3/postgresql-9.6.3.tar.bz2

###step 2: Install require package
`sudo apt install -y build-essential libreadline-dev zlib1g-dev flex bison libxml2-dev libxslt-dev libssl-dev libsystemd-dev`

###step 3: Create user postgres with homedir in /opt/pgsql
`sudo useradd -d /opt/pgsql -m -r -s /bin/bash postgres`

###step 4: move pg source in homedir's postgres user
```
sudo mkdir -p /opt/pgsql/src
sudo mv postgresql-9.6.3.tar.bz2 /opt/pgsql/src/postgresql-9.6.3.tar.bz2
sudo chown -R postgres:postgres /opt/pgsql/
```
###step 5: connect to postgres user
sudo su - postgres 

###step 6: add export variables in .bashrc
```
#config postgres
export PATH=/opt/pgsql/9.6/bin:$PATH
export LD_LIBRARY_PATH=/opt/pgsql/9.6/lib:$LD_LIBRARY_PATH
export PGDATA=/opt/pgsql/9.6/data
export PDLOG=/opt/pgsql/9.6/logs/serverlog
```
> You can these lines in your own .bashrc 

###step 7: uncompress pg source
```
cd src/
tar -xvjf postgresql-9.6.3.tar.bz2 
```

###step 8: Install pg from source
```
cd postgresql-9.6.3/
./configure --prefix /opt/pgsql/9.6 --with-systemd
make
make install
```

###step 9: init pg database
`initdb -D $PGDATA -U postgres`

###step 10: service settings for starting pg on boot

```bash
#with a root/sudoer user
sudo cp ~postgres/src/postgresql-9.6.3/contrib/start-scripts/linux /etc/init.d/postgresql
sudo chmod +x /etc/init.d/postgresql
```
Edit variable prefix,PGDATA,PGUSER and PGLOG in /etc/init.d/postgresql:
```bash
# Installation prefix
prefix=/opt/pgsql/9.6

# Data directory
PGDATA="/opt/pgsql/9.6/data"

# Who to run the postmaster as, usually "postgres".  (NOT "root")
PGUSER=postgres

# Where to keep a log file
PGLOG="$prefix/logs/serverlog"
```

###step 11: start service
```bash
sudo update-rc.d postgresql defaults
sudo systemctl start postgresql
```

###step 12: test to connect to your database
```bash
sudo su - postgres
psql
```
> If you add this 
> export PATH=/opt/pgsql/9.6/bin:$PATH
> in your .bashrc, your can connect to postgres without change user like this
> psql -U postgres 