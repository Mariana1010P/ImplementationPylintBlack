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
        author_id_article (int): Author of the article, foreign key extending to author.
        published_date (datetime): Date when the article was published.
    """

    article_id: int
    title: str
    content: str
    author_id_article: int  
    published_date: datetime
