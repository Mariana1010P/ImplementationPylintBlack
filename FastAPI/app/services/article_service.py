"""
Module that provides service functionality for managing articles in the database.
"""

from peewee import DoesNotExist, IntegrityError  # type: ignore
from config.database import ArticleModel

class ArticleService:
    """
    Service class for handling business logic related to articles.

    Methods:
        create_article(title: str, author: int, category: str, content: str, published_date: datetime.datetime, status: str, updated_date: datetime.datetime) -> ArticleModel
        update_article(article_id: int, **kwargs) -> ArticleModel
        delete_article(article_id: int) -> bool
        get_article_by_id(article_id: int) -> ArticleModel
        get_all_articles() -> list
    """

    @staticmethod
    def create_article(title: str, author: int, category: str, content: str, published_date: datetime.datetime, status: str, updated_date: datetime.datetime) -> ArticleModel:
        """
        Creates a new article in the database.

        Args:
            title (str): The title of the article.
            author (int): The ID of the author.
            category (str): The category of the article.
            content (str): The content of the article.
            published_date (datetime.datetime): The date the article was published.
            status (str): The status of the article.
            updated_date (datetime.datetime): The date the article was last updated.

        Returns:
            ArticleModel: The created article.

        Raises:
            ValueError: If any data validation fails.
            IntegrityError: If there's an integrity error during creation.
        """
        try:
            return ArticleModel.create(
                title=title, author=author, category=category, content=content,
                published_date=published_date, status=status, updated_date=updated_date
            )
        except IntegrityError as exc:
            raise ValueError(f"Failed to create article: {exc}") from exc

    @staticmethod
    def update_article(article_id: int, **kwargs) -> ArticleModel:
        """
        Updates an article in the database.

        Args:
            article_id (int): The ID of the article to update.
            **kwargs: The fields to update.

        Returns:
            ArticleModel: The updated article.

        Raises:
            ValueError: If any data validation fails.
            DoesNotExist: If no article with the given ID exists.
            IntegrityError: If there's an integrity error during update.
        """
        try:
            article = ArticleModel.get(ArticleModel.id == article_id)
            for key, value in kwargs.items():
                setattr(article, key, value)
            article.save()
            return article
        except DoesNotExist:
            raise ValueError(f"No article found with ID: {article_id}")
        except Exception as exc:
            raise RuntimeError(f"Error updating article: {exc}") from exc

    @staticmethod
    def delete_article(article_id: int) -> bool:
        """
        Deletes an article from the database.

        Args:
            article_id (int): The ID of the article to delete.

        Returns:
            bool: True if the article was deleted, False otherwise.

        Raises:
            DoesNotExist: If no article with the given ID exists.
        """
        try:
            article = ArticleModel.get(ArticleModel.id == article_id)
            article.delete_instance()
            return True
        except DoesNotExist:
            return False
        except Exception as exc:
            raise RuntimeError(f"Error deleting article: {exc}") from exc

    @staticmethod
    def get_article_by_id(article_id: int) -> ArticleModel:
        """
        Retrieves an article by ID.

        Args:
            article_id (int): The ID of the article to retrieve.

        Returns:
            ArticleModel: The article with the given ID.

        Raises:
            DoesNotExist: If no article with the given ID exists.
        """
        try:
            return ArticleModel.get(ArticleModel.id == article_id)
        except DoesNotExist:
            return None
        except Exception as exc:
            raise RuntimeError(f"Error retrieving article: {exc}") from exc

    @staticmethod
    def get_all_articles() -> list:
        """
        Retrieves all articles from the database.

        Returns:
            list: A list of all articles.
        """
        try:
            return list(ArticleModel.select())
        except Exception as exc:
            raise RuntimeError(f"Error retrieving articles: {exc}") from exc
