create table entity(
  entity_id varchar(255) not null primary key,
  name varchar(255) not null,
  type varchar(255) not null,
  wikipedia_url varchar(255),
  image varchar(255),
  short_description varchar(255),
  detailed_description varchar(255),
  url varchar(255)
);

create table source(
  source_id varchar(255) not null primary key,
  name varchar(255) not null,
  url varchar(255),
  language char(2) not null,
  country char(2),
  description varchar(255),
  category varchar(255)
);

create table article(
  title varchar(255) not null,
  description varchar(255) not null,
  url varchar(255) not null,
  image_url varchar(255),
  source_id varchar(255) not null,
  datetime_published datetime not null,
  authors varchar(255),
  primary key(title, source_id, datetime_published),
  foreign key(source_id) references source(source_id)
    on update cascade
    on delete cascade
);

create table mention(
  entity_id varchar(255) not null,
  name varchar(255) not null,
  article_title varchar(255),
  source_id varchar(255) not null,
  datetime_published datetime,
  sentiment_score real not null,
  sentiment_magnitude real not null,
  salience real not null,
  primary key(entity_id, article_title, source_id, datetime_published),
  foreign key(entity_id) references entity(entity_id)
    on update cascade
    on delete cascade,
  foreign key(article_title, source_id, datetime_published)
    references article(title, source_id, datetime_published)
    on update cascade
    on delete cascade
);

create or replace view favorite_sources
  as select * from source
     where source_id ='abc-news'
      or source_id = 'associated-press'
      or source_id = 'bbc-news'
      or source_id = 'bloomberg'
      or source_id = 'breitbart-news'
      or source_id = 'business-insider'
      or source_id = 'buzzfeed'
      or source_id = 'cbc-news'
      or source_id = 'cbs-news'
      or source_id = 'cnbc'
      or source_id = 'cnn'
      or source_id = 'daily-mail'
      or source_id = 'financial-times'
      or source_id = 'fox-news'
      or source_id = 'msnbc'
      or source_id = 'nbc-news'
      or source_id = 'politico'
      or source_id = 'the-economist'
      or source_id = 'the-huffington-post'
      or source_id = 'the-new-york-times'
      or source_id = 'the-wall-street-journal'
      or source_id = 'the-washington-post'
      or source_id = 'usa-today';
