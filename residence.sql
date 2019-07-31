
create table if not exists users (
    userid int not null AUTO_INCREMENT,
    first_name varchar(40) not null,
    last_name varchar(40),
    mobile int not null unique,
    passwd varchar(32) not null,     
    primary key (userid)
    );

create table if not exists residence(
    hostid int not null,
    placeid varchar(40) not null,
    person_for_each_place int not null,
    rent_for_each_place numeric(10,2) not null,
    shared_place boolean not null,
    short_description varchar(255),
    country varchar(80) not null,
    city varchar(80) not null,
    area varchar(80) not null,
    address varchar(255) not null,
    primary key (hostid,placeid),
    foreign key (hostid) REFERENCES users (userid)
    );

create table if not exists booked(
    hostid int not null,
    placeid varchar(40) not null,
    booked_from date not null,
    booked_to date not null,
    primary key (hostid,placeid,booked_from),
    foreign key (hostid) REFERENCES users (userid),
    
    foreign key (hostid,placeid) references residence(hostid,placeid)
    
    );

create table if not exists availability(
    hostid int not null,
    placeid varchar(40) not null,
    avail_from date not null,
    avail_to date not null,
    primary key (hostid,placeid,avail_from),
    foreign key (hostid) references users (userid),
    foreign key (hostid,placeid) references residence (hostid,placeid)
    
);
  
create table if not exists bookings(
    hostid int not null,
    placeid varchar(40) not null,
    fromo date  not null,
    too date not null,
    rent_per_day numeric(10,2) not null,
    total numeric(10,2),
    guestid int not null,
    primary key (hostid,placeid,fromo),
    foreign key(hostid) references users (userid),
    foreign key(guestid) references users (userid),
    foreign key (hostid,placeid) references residence (hostid,placeid)
    
);

