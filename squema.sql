drop table if exists products;
create table products(
    store_date datetime DEFAULT CURRENT_TIMESTAMP,
    product_id int primary key,
    title text not null,
    price real,
    available text,
    current_difference real
);
drop table if exists history;
create table history(
	rowid int primary key,
	product_id int,
	last_date datetime DEFAULT CURRENT_TIMESTAMP,
	price real,
    available text not null
);
