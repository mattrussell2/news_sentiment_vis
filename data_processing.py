"""
data_processing.py

Take json objects and insert into database
"""

def article_row_from_article_object(article):
    """
    Args: article is a dictionary with the following keys:

    source - abc, cnn, etc
    author - name(s) of author(s)
    title - title of article
    description - brief description of article
    url - url of article
    urlToImage - honestly not sure
    publishedAt - date & time of publication
    content - slightly longer version of article text
    --------------------
    fulltext - the fulltext object from the call to newspaper3k
    ------------------------
    IBM_sentiment - the result of a call to IBM language API
    GOOGLE_sentiment - the result of a call to GOOGLE language API
    AYLIEN_sentiment - the result of a call to AYLIEN textapi API
    ------------------------

    Returns a row for an article in the db
    """
    title = article['title']
    description = article['description']
    url = article['url']
    image_url = article['urlToImage']
    source_id = article['source']['id']
    datetime_published = article['publishedAt']
    authors = article['author']

    return [title, description, url, image_url, source_id,
            datetime_published, authors]

def mention_rows_from_article_object(article):
    """
    Args: article is a dictionary with the following keys:

    source - abc, cnn, etc
    author - name(s) of author(s)
    title - title of article
    description - brief description of article
    url - url of article
    urlToImage - honestly not sure
    publishedAt - date & time of publication
    content - slightly longer version of article text
    --------------------
    fulltext - the fulltext object from the call to newspaper3k
    ------------------------
    IBM_sentiment - the result of a call to IBM language API
    GOOGLE_sentiment - the result of a call to GOOGLE language API
    AYLIEN_sentiment - the result of a call to AYLIEN textapi API
    ------------------------

    Returns rows for mentions in the db
    """
    if type(article["GOOGLE_sentiment"]) == str:
        return []

    rows = []
    for entity in article["GOOGLE_sentiment"].entities:
        if "mid" in entity.metadata.keys():
            entity_id = entity.metadata["mid"]
        else:
            entity_id = entity.name
        name = entity.name
        article_title = article["title"]
        source_id = article["source"]["id"]
        datetime_published = article['publishedAt']
        sentiment_score = entity.sentiment.score
        sentiment_magnitude = entity.sentiment.magnitude
        salience = entity.salience
       
        rows.append([entity_id, name, article_title, source_id,
                     datetime_published, sentiment_score,
                     sentiment_magnitude, salience])

    return rows

def entity_rows_from_article_object(article):
    """
    Args: article is a dictionary with the following keys:

    source - abc, cnn, etc
    author - name(s) of author(s)
    title - title of article
    description - brief description of article
    url - url of article
    urlToImage - honestly not sure
    publishedAt - date & time of publication
    content - slightly longer version of article text
    --------------------
    fulltext - the fulltext object from the call to newspaper3k
    ------------------------
    IBM_sentiment - the result of a call to IBM language API
    GOOGLE_sentiment - the result of a call to GOOGLE language API
    AYLIEN_sentiment - the result of a call to AYLIEN textapi API
    ------------------------

    Returns rows for entities in the db
    """
    if type(article["GOOGLE_sentiment"]) == str:
        return []

    rows = []
    for entity in article["GOOGLE_sentiment"].entities:
        if "mid" in entity.metadata.keys():
            entity_id = entity.metadata["mid"]
            wikipedia_url = entity.metadata["wikipedia_url"]
        else:
            entity_id = entity.name
            wikipedia_url = None
        name = entity.name
        entity_type = entity.type

        rows.append([entity_id, name, entity_type, wikipedia_url,
                     None, None, None, None])

    return rows

def source_row_from_article_object(article):
    """
    Args: article is a dictionary with the following keys:

    source - abc, cnn, etc
    author - name(s) of author(s)
    title - title of article
    description - brief description of article
    url - url of article
    urlToImage - honestly not sure
    publishedAt - date & time of publication
    content - slightly longer version of article text
    --------------------
    fulltext - the fulltext object from the call to newspaper3k
    ------------------------
    IBM_sentiment - the result of a call to IBM language API
    GOOGLE_sentiment - the result of a call to GOOGLE language API
    AYLIEN_sentiment - the result of a call to AYLIEN textapi API
    ------------------------

    Returns rows for entities in the db
    """

    source_id = article["source"]["id"]
    name = article["source"]["name"]
    url = ""
    language = "en"

    return [source_id, name, url, language, None, None, None]
