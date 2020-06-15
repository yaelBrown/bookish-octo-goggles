create database CNG;

use CNG;

create table overview (
	id int primary key not null, 
	npcs json not null, 
	activities json not null, 
	reporting_machines json not null
);