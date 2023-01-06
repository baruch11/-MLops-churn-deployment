# PROXY SQL CONNEXION :

#### Download Cloud SQL Auth proxy according to your setup

https://cloud.google.com/sql/docs/postgres/sql-proxy#install

copy cloud_sql_proxy in a location in your $PATH (for e.g. ~/bin )

### Command lines :

1 - `make proxy-start`

##### Open a new terminal :

2 - `make postgres-connexion`

##### To shut postgres

3 - `exit` or `\q`

##### To terminate running instance

4 - `make proxy-kill`








