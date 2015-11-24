drop table if exists user;
create table user (
	email text primary key,
	password text not null,
	reg_type integer not null,
	name text not null,
	sex_type integer not null,
	code text
);
drop table if exists teacherCode;
create table teacherCode (
	email text primary key,
	student_code text not null,
	parent_code text not null
);
drop table if exists notice;
create table notice(
	email text primary key,
	num integer not null,
	title text not null,
	content text not null,
	time text not null,
	isSignNeed integer not null
);
drop table if exists token;
create table token(
	email text primary key,
	token text not null
);
