create table stock_day(
    day date primary key not null,
    mark int
)

create table stock_info(
    code int primary key not null,
    name varchar(50)
)

create table stock_vol(
    id integer primary key autoincrement,
    code int not null,
    day date not null,
    volume int,
    percent real
)