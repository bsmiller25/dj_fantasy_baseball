# dj_fantasy_baseball

A Django fantasy baseball platform using the [python gameday module](https://github.com/panzarino/mlbgame).

## INSTALLATION and SETUP

1) Clone this repo locally.  
2) Copy .env_template to .env and fill in the variables.  
3) Set up Postgres  
-- Steps for local version assuming you have Postgresql installed:  
a) Connect to psql with a role that can create users.  
b) Create a role with name and password that match you .env: `CREATE ROLE db_user CREATEDB LOGIN PASSWORD 'db_password'`  
c) Edit your pg_hba.conf local portion so your db_user can login with a password. Example:  
```
# "local" is for Unix domain socket connections only
local   all             db_user                                 md5
local   all             all                                     peer
```  
d) Restart Postgres: `sudo service postgresql restart`  
e) Connect as db_user `psql postgres -U db_user` and create database `CREATE DATABASE db_name;`

