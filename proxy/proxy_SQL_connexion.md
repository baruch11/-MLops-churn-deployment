# PROXY SQL CONNEXION :

#### Download Cloud SQL Auth proxy according to your setup

https://cloud.google.com/sql/docs/postgres/sql-proxy

### Command lines :

1 - `make proxy-start`

##### Open a new terminal :

2 - `psql "host=localhost port=5432 sslmode=disable dbname=postgres user=coyotta-2022-group-1"`

##### To shut postgres

3 - `exit`

##### To terminate running instance

4 - `make proxy-kill`







