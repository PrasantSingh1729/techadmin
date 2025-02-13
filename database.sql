create database if not exists Movie_Booking; 

drop table if exists Booking; 
drop table if exists Schedule; 
drop table if exists Theater; 
drop table if exists Movie; 
drop table if exists User;

use Movie_Booking; 

create table User( 
email_address VARCHAR(50) primary key, 
user_name VARCHAR(50) not null, 
mobile_number BIGINT(10) unique not null, 
date_of_birth DATE not null, 
password VARCHAR(50) not null, 
security_question VARCHAR(50) not null, 
security_answer VARCHAR(50) not null, 
role enum("admin", "tech_admin", "user") default "user" 
)engine='InnoDB';

insert into User (email_address, user_name,mobile_number, date_of_birth, password, security_question, security_answer, role) 
values("Raj@gmail.com", "Raj", 1234567898,"1994-12-02","xyz123", "Where is your favorite place to vacation?", "Ooty", "user"); 
Insert into User (email_address, user_name,mobile_number, date_of_birth, password, security_question, security_answer, role) 
values("Ram@gmail.com", "Ram",234567899, "1998-01-01","xyz124", "What was the name of your favorite pet?", "Dog","user"); 
insert into User (email_address, user_name,mobile_number, date_of_birth, password, security_question, security_answer, role) 
values("Mary@gmail.com", "Mary", 1234567891, "1990-12-08","xyz128", "What was the name of your favorite pet?", "Cat", "user"); 
insert into User (email_address, user_name,mobile_number, date_of_birth, password, security_question, security_answer, role) 
values("Sham@gmail.com", "Sham", 1234567896, "1990-12-12", "xyz125", "What is your favorite food?", "Chicken", "admin"); 
insert into User (email_address, user_name,mobile_number, date_of_birth, password, security_question, security_answer, role) 
values("balaji123@gmail.com", "Balaji", 9834567891, "1992-01-18", "bal128", "What was the name of your favorite pet?", "Cat","admin"); 
insert into User (email_address, user_name,mobile_number, date_of_birth, password, security_question, security_answer, role) 
values("Peter@gmail.com", "Peter", 1234567894, "1990-03-14", "xyz126", "What city were you born in?", "Bangalore", "tech_admin"); 
insert into User (email_address, user_name,mobile_number, date_of_birth, password, security_question, security_answer, role) 
values("John@gmail.com","John", 1234567892, "1990-07-23","xyz127", "Where is your favorite place to vacation?", "Mysore", "tech_admin"); 


create table Movie( 
movie_name varchar(50) primary key, 
language enum("English", "Hindi", "Kannada", "Tamil", "Telugu", "Malayalam") not null, 
category enum("Comedy", "Action", "Horror") not null, 
release_date date not null 
)engine='InnoDB'; 


insert into Movie (movie_name, language, category, release_date) 
values("DDL", "Hindi", "Action", "2020-12-10"); 
insert into Movie (movie_name, language, category, release_date)
values ("Bahubali", "Tamil", "Horror", "2020-10-13"); 
insert into Movie (movie_name, language, category, release_date)
values("Dhoom", "Telugu", "Comedy", "2020-12-14"); 
insert into Movie (movie_name, language, category, release_date)
values("Gangaster", "Kannada", "Action", "2020-12-15"); 
insert into Movie (movie_name, language, category, release_date)
values("Penguin", "Malayalam", "Action", "2020-10-15");

create table Theater( 
theater_name varchar(58) primary key, 
owner_email varchar(50) not null, 
show_time varchar(58) default "10AM to 1PM, 2PM to 5PM, 6PM to 9PM" not null, 
seat_capacity integer not null, 
price_per_ticket float not null, 
foreign key(owner_email) references User (email_address)) engine='InnoDB';

#yyyy-mm-dd 2022-12-10 

insert into Theater (theater_name, owner_email, seat_capacity, price_per_ticket) 
values ("Nataraj", "Ram@gmail.com", 100, 100); 
insert into Theater (theater_name, owner_email, seat_capacity, price_per_ticket) 
values ("Rocky", "Peter@gmail.com",100,200); 
insert into Theater (theater_name, owner_email, seat_capacity, price_per_ticket) 
values ("Madhubala", "John@gmail.com",100,300); 
insert into Theater (theater_name, owner_email, seat_capacity, price_per_ticket) 
values ("Star", "Ram@gmail.com",100,400); 
insert into Theater (theater_name, owner_email, seat_capacity, price_per_ticket) 
values ("C3Cinema", "Peter@gmail.com",100,400);

create table Schedule 
( 
schedule_id integer primary key auto_increment, 
theater_name varchar(50) not null, 
movie_name varchar(50) not null, 
start_date date not null, 
end_date date not null, 
foreign key(theater_name) references Theater(theater_name), 
foreign key(movie_name) references Movie(movie_name) 
)engine=innodb auto_increment=101; 

insert into Schedule (theater_name,movie_name, start_date, end_date) 
values("Nataraj", "DDL", "2023-02-18","2023-02-24"); 
insert into Schedule (theater_name,movie_name, start_date, end_date) 
values ("Rocky", "Dhoom", "2023-02-11", "2023-02-25"); 
insert into Schedule (theater_name,movie_name, start_date, end_date) 
values ("Madhubala", "Bahubali", "2023-01-13","2823-02-01"); 
insert into Schedule (theater_name,movie_name, start_date,end_date) 
values("Star", "Penguin", "2023-01-25", "2023-02-12"); 
insert into Schedule (theater_name,movie_name, start_date, end_date) 
values ("C3Cinema", "DDL", "2023-01-13", "2023-02-01");