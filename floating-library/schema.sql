drop table if exists book;
drop table if exists book_update;
drop table if exists review;

create table book (
	id integer primary key autoincrement,

	url text unique not null,
	title text not null,
	author text not null,
	chapter_count integer not null,

	date_added timestamp not null,
	date_updated timestamp not null
);

create table book_update (
	id integer primary key autoincrement,
	book_id integer not null,

	added_chapters integer not null,

	date_added timestamp not null,

	foreign key (book_id) references book (id)
);

create table review (
	id integer primary key autoincrement,
	book_id integer not null,

	rating integer not null,
	body text not null,

	date_added timestamp not null,
	date_updated timestamp not null,

	foreign key (book_id) references book (id)
);

