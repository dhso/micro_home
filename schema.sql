drop table if exists plugins;
create table plugins (
  id integer primary key autoincrement,
  name text not null,
  desc text not null,
  status integer not null default 0,
  author text not null,
  version text not null
);
