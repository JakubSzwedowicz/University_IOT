Having postgres installed: https://www.tutorialspoint.com/postgresql/postgresql_environment.htm


# Setting up the database for the first time
1. Delete existing database:
```dropdb userauthorization```
2. Create database:  
```createdb -O postgres userauthorization```
3. Now load .ddl file to database
`psql -U postgres -d userauthorization < ProjectDesign.ddl`
In case of an error here [read](https://stackoverflow.com/questions/69676009/psql-error-connection-to-server-on-socket-var-run-postgresql-s-pgsql-5432):
4