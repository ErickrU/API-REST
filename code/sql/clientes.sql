drop table if exists clientes;

create table clientes(
	id_cliente integer primary key autoincrement,
	nombre varchar(80) not null,
	email varchar(80) not null
);

insert into clientes(nombre, email) values ("Erick","Erick@gmail.com");
insert into clientes(nombre, email) values ("Yael","yael@gmail.com");
insert into clientes(nombre, email) values ("michelle","michelle@gmail.com");
