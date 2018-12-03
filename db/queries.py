"""
queries.py

Contians DB info and SQL queries declarations
"""

CLOUDSQL_CONNECTION_NAME = 'news-vis:us-central1:news-database'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'news-VIS'

INSERT_ARTICLES = '''
insert ignore into article values (%s, %s, %s, %s, %s, %s, %s)
'''

INSERT_SOURCE = '''
insert ignore into source (source_id, name, url, language, country,
                           description, category)
       values (%s, %s, %s, %s, %s, %s, %s)
'''

INSERT_ENTITIES = '''
insert ignore into entity values (%s, %s, %s, %s, %s, %s, %s, %s)
'''

INSERT_MENTIONS = '''
insert ignore into mention values (%s, %s, %s, %s, %s, %s, %s, %s)
'''

GET_NEW_KG_ENTITIES = '''
select entity_id
from entity
where image is null
      and short_description is null
      and detailed_description is null
      and url is null
      and name != entity_id
'''

UPDATE_NEW_KG_ENTITY = '''
update entity
set name = %s,
    image = %s,
    short_description = %s,
    detailed_description = %s,
    url = %s
where entity_id = %s
'''

GET_TOP_MENTIONS_COUNT_ALL = '''
select m.entity_id, e.name, count(m.entity_id)
from mention m join entity e on (m.entity_id = e.entity_id)
    join favorite_sources s on (m.source_id = s.source_id)
where m.entity_id != e.name
group by m.entity_id
order by count(m.entity_id) desc
limit {}
'''

GET_TOP_MENTIONS_SUM = '''
select m.entity_id, e.name, sum(m.salience)
from mention m join entity e on (m.entity_id = e.entity_id)
    join favorite_sources s on (m.source_id = s.source_id)
where m.datetime_published > '{}'
    and m.entity_id != e.name
group by m.entity_id
order by sum(m.salience) desc
limit {}
'''

GET_TOP_MENTIONED_WITH_COUNT = '''
select m1.entity_id, e.name, count(m1.entity_id)
from mention m1 join mention m2
  on (m1.article_title = m2.article_title
      and m1.source_id = m2.source_id
      and m1.datetime_published = m2.datetime_published)
  join entity e on (m1.entity_id = e.entity_id)
where m2.entity_id = '{}' and m1.entity_id != m2.entity_id
  and m1.source_id = '{}' and m1.source_id = m2.source_id
group by m1.entity_id
order by count(m1.entity_id) desc
limit {}
'''

GET_TOP_MENTIONED_WITH_SUM = '''
select m1.entity_id, e.name, sum(m1.salience)
from mention m1 join mention m2
  on (m1.article_title = m2.article_title
      and m1.source_id = m2.source_id
      and m1.datetime_published = m2.datetime_published)
  join entity e on (m1.entity_id = e.entity_id)
  join favorite_sources s on (m1.source_id = s.source_id)
where m2.entity_id = '%s' and m1.entity_id != m2.entity_id
      and m1.datetime_published > '%s'
group by m1.entity_id
order by sum(m1.salience) desc
limit %s
'''

GET_ARTICLES_BY_ENTITY = '''
select a.*, s.name
from article a join favorite_sources s on (a.source_id = s.source_id)
     join mention m on (a.title = m.article_title and
                        a.source_id = m.source_id and
                        a.datetime_published = m.datetime_published)
where m.entity_id = '{}' and m.datetime_published > '{}' and a.image_url != ''
order by m.salience desc
limit {}
'''

GET_ENTITIES_BY_ARTICLE = '''
select e.entity_id, e.name, e.type, e.wikipedia_url, m.sentiment_score,
       m.sentiment_magnitude, m.salience
from mention m join entity e on (m.entity_id = e.entity_id)
where m.article_title = '{}' and m.source_id = '{}'
order by m.salience desc
'''

GET_SOURCES = '''
select source_id, name from source
'''

TOP_ENTITIES_BY_SOURCE = '''
select e.*, avg(m.sentiment_score), avg(m.sentiment_magnitude),
       avg(m.salience), sum(m.salience)
from mention m join favorite_sources s on (s.source_id = m.source_id)
    join entity e on (e.entity_id = m.entity_id)
where m.source_id = '{}' and datetime_published > '{}'
group by m.entity_id
order by sum(m.salience)
'''

SOURCES_BY_ENTITY = '''
select s.name, avg(m.sentiment_score), avg(m.sentiment_magnitude),
       avg(m.salience), sum(m.salience), count(m.entity_id)
from mention m join favorite_sources s on (s.source_id = m.source_id)
    join entity e on (e.entity_id = m.entity_id)
where m.entity_id = '{}' and datetime_published > '{}'
group by m.source_id
order by sum(m.salience)
'''

CREATE_TABLE_ENTITY = '''
create table entity(
  entity_id varchar(255) not null primary key,
  name varchar(255) not null,
  type varchar(255) not null,
  wikipedia_url varchar(255),
  image varchar(255),
  short_description varchar(255),
  detailed_description varchar(255),
  url varchar(255)
)
'''

CREATE_TABLE_SOURCE = '''
create table source(
  source_id varchar(255) not null primary key,
  name varchar(255) not null,
  url varchar(255) not null,
  language char(2) not null,
  country char(2),
  description varchar(255),
  category varchar(255)
)
'''

CREATE_TABLE_ARTICLE = '''
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
)
'''

CREATE_TABLE_MENTION = '''
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
'''

CREATE_FAVORITE_SOURCES = '''
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
      or source_id = 'usa-today'
'''

POS_SENTIMENT_BY_SOURCE_AND_ENTITY = """
select avg(sentiment_score), avg(sentiment_magnitude), count(*)
from mention
where entity_id = '{}' and source_id = '{}' and sentiment_score > 0
"""
"""
select avg(sentiment_score), avg(sentiment_magnitude), count(*)
from mention
where entity_id = '/m/0cqt90' and source_id = 'cnn' and sentiment_score > 0
"""

NEG_SENTIMENT_BY_SOURCE_AND_ENTITY = """
select avg(sentiment_score), avg(sentiment_magnitude), count(*)
from mention
where entity_id = '{}' and source_id = '{}' and sentiment_score < 0
"""

NEUTRAL_SENTIMENT_BY_SOURCE_AND_ENTITY = """
select avg(sentiment_magnitude), count(*)
from mention
where entity_id = '{}' and source_id = '{}' and sentiment_score = 0
"""

GET_TOTAL_ARTICLES_FROM_SOURCE = """
select count(*) from article where source_id = '{}'
"""
