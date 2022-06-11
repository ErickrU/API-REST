# SQLITE3

Script for clientes database

```
drop table if exists clientes;
create table clientes(
	id_cliente integer primary key autoincrement,
	nombre varchar(80) not null,
	email varchar(80) not null
);
insert into clientes(nombre, email) values ("Erick","Erick@gmail.com");
insert into clientes(nombre, email) values ("Yael","yael@gmail.com");
insert into clientes(nombre, email) values ("Michelle","Michelle@gmail.com");
```

The structure for `SQL` sentences are the same

Create a database base from a script

    sqlite3 clientes.sqlite < clientes.sql

select a databse

    sqlite3 clientes.sqlite

all of these commands can be used after select a database

```
.show
.schema
.tablle
.save FILE
.mode column|list|csv
.header ON|OFF
.read script.sql
.header
.dump
.quit
```

You can consult [The official documentation of sqlite3](https://www.sqlite.org/docs.html) for more commands and examples.