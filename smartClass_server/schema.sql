drop table if exists user;
create table user (
	email text primary key,
	password text not null,
	reg_type integer not null,
	name text not null,
	sex_type integer not null
);
