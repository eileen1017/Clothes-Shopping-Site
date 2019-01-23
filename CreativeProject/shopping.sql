create database Shopping2;

use Shopping2;

create table users (  userid mediumint unsigned not null auto_increment,  firstname varchar(32) not null, lastname varchar(32) not null, email varchar(255) not null, password VARCHAR(255) not null, primary key (userid),  unique key email (email) ) engine = InnoDB default character set = utf8 collate = utf8_general_ci;

create table items (  item_id mediumint unsigned not null auto_increment,  itemname varchar(32) not null, item_picture varchar(32) not null, item_type enum('f','m') not null,  item_price mediumint unsigned not null, primary key (item_id) ) engine = InnoDB default character set = utf8 collate = utf8_general_ci;

insert into items (itemname,item_type,item_price, item_picture) values ('Purple Long Sleeve Shirt','m',30,'/maleClothes/1m.jpeg');
insert into items (itemname,item_type,item_price, item_picture) values ('Jeans Long Sleeve Shirt','m',60,'/maleClothes/2m.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Red Short Sleeve Polo','m',20,'/maleClothes/3m.jpeg');
insert into items (itemname,item_type,item_price, item_picture) values ('Green Long Sleeve Jacket','m',100,'/maleClothes/4m.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Black Cool Jacket','m',150,'/maleClothes/5m.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Black Sports Jacket','m',120,'/maleClothes/6m.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Black Leather Jacket','m',170,'/maleClothes/7m.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Blue Coach Jacket','m',120,'/maleClothes/8m.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Brown Winter Jacket','m',112,'/maleClothes/9m.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('White Winter Jacket','m',104,'/maleClothes/10m.jpg');

insert into items (itemname,item_type,item_price, item_picture) values ('Black Beautiful Leather Jacket','f',200,'/femaleClothes/1f.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Black Stylish Leather Jacket','f',300,'/femaleClothes/2f.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Black Beautiful Dress','f',400,'/femaleClothes/3f.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Blue Dress From China','f',305,'/femaleClothes/4f.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Light Blue Dress','f',285,'/femaleClothes/5f.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Beautiful Colorful Dress','f',130,'/femaleClothes/6f.jpeg');
insert into items (itemname,item_type,item_price, item_picture) values ('Black OL Dress','f',203,'/femaleClothes/7f.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('White Dress For School Girl','f',80,'/femaleClothes/8f.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Black Formal Dress','f',98,'/femaleClothes/9f.jpg');
insert into items (itemname,item_type,item_price, item_picture) values ('Dress With Flowers','f',178,'/femaleClothes/10f.jpg');


create table cart(
 itemid mediumint unsigned not null,
 userid mediumint unsigned not null,
 quantity smallint unsigned not null,
 cartid smallint unsigned not null auto_increment,
 primary key (cartid),
 foreign key (userid) references users (userid),
 foreign key (itemid) references items (item_id)
) engine = InnoDB default character set = utf8 collate = utf8_general_ci;

create table wishlist(
 itemid mediumint unsigned not null,
 userid mediumint unsigned not null,
 wishid smallint unsigned not null auto_increment,
 primary key (wishid),
 foreign key (userid) references users (userid),
 foreign key (itemid) references items (item_id)
) engine = InnoDB default character set = utf8 collate = utf8_general_ci;

create table purchased(
 itemid mediumint unsigned not null,
 userid mediumint unsigned not null,
 quantity smallint unsigned not null,
 purchaseid smallint unsigned not null auto_increment,
 primary key (purchaseid)
) engine = InnoDB default character set = utf8 collate = utf8_general_ci;

create table friends(
 relationid mediumint unsigned not null auto_increment,
 userid mediumint unsigned not null,
 friend_email varchar(255) not null,
 primary key (relationid),
 foreign key (userid) references users (userid)
) engine = InnoDB default character set = utf8 collate = utf8_general_ci;

create table comments(
 itemid mediumint unsigned not null,
 userid mediumint unsigned not null,
 commenttext varchar(255) not null,
 commentid smallint unsigned not null auto_increment,
 primary key (commentid),
 foreign key (itemid) references items (item_id)
) engine = InnoDB default character set = utf8 collate = utf8_general_ci;





