"""
schemas/article.py

This module defines the Pydantic model for an Article.
"""

from datetime import datetime
from pydantic import BaseModel


class Article(BaseModel):
    """
    Schema representing an Article.

    Attributes:
        article_id (int): Unique identifier for the article.
        title (str): Title of the article.
        content (str): Content of the article.
        author_id_article (int): Author of the article, foreing key extends to author.
        published_date (datetime): Date when the article was published.
        updated_date (datetime): Date when the article was last updated.

    """

    article_id: int
    title: str
    content: str
<<<<<<< HEAD
    author_id_article: int  
    published_date: datetime.datetime
=======
    author_id: int
    published_date: datetime
>>>>>>> 5331605b3de1975bfaf5390da51ace02236e0cd6
