drop table if exists user;
create table user (
	email text primary key,
	password text not null,
	reg_type integer not null,
	name text not null,
	sex_type integer not null,
	profile_image DEFAULT 'profile_images/default.png',
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
	email text not null,
	num integer not null,
	title text not null,
	content text not null,
	time text not null,
	isSignNeed integer not null,
	isImportant integer not null,
	PRIMARY KEY(email, num)
);
drop table if exists assignment;
create table assignment(
	email text not null,
	num integer not null,
	title text not null,
	content text not null,
	time text not null,
	start_date text not null,
	end_date text not null,
	isImportant integer not null,
	PRIMARY KEY(email, num)
);
drop table if exists memory;
create table memory(
	email text not null,
	num integer not null,
	content text not null,
	image text,
	time text not null,
	PRIMARY KEY(email, num)
);
drop table if exists sign;
create table sign(
	email_teacher text not null,
	num integer not null,
	email_parent text not null,
	signImage text not null,
	PRIMARY KEY(email_teacher, num, email_parent)
);
drop table if exists token;
create table token(
	email text primary key,
	token text not null
);
