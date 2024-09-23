import datetime
from peewee import DoesNotExist, IntegrityError
from config.database import ArticleModel

class ArticleService:
    @staticmethod
    def create_article(
        title: str, author_id_article: int, content: str,
        published_date: datetime.datetime,
    ) -> ArticleModel:
        """
        Creates a new article in the database.
        
        Args:
            title (str): The title of the article.
            author_id_article (int): The ID of the author related to the article.
            content (str): The content of the article.
            published_date (datetime.datetime): The publication date of the article.
        
        Returns:
            ArticleModel: The created article instance.
        """
        try:
            return ArticleModel.create(
                title=title,
                author_id_article=author_id_article,
                content=content,
                published_date=published_date,
            )
        except IntegrityError as exc:
            raise ValueError(f"Failed to create article: {exc}") from exc

    @staticmethod
    def update_article(article_id: int, **kwargs) -> ArticleModel:
        """
        Updates an existing article in the database.

        Args:
            article_id (int): The ID of the article to update.
            **kwargs: The fields to update for the article.

        Returns:
            ArticleModel: The updated article instance.
        
        Raises:
            ValueError: If no article is found with the given ID or if an update fails.
        """
        try:

            article = ArticleModel.get(ArticleModel.article_id == article_id)

            for key, value in kwargs.items():
                setattr(article, key, value)
            article.save()
            return article

        except DoesNotExist:
            raise ValueError(f"No article found with ID: {article_id}")
        except IntegrityError as exc:
            raise ValueError(f"Failed to update article due to integrity error: {exc}") from exc
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}") from e


    @staticmethod
    def delete_article(article_id: int) -> bool:
        """
        Deletes an article from the database.
        
        Args:
            article_id (int): The ID of the article to delete.
        
        Returns:
            bool: True if the article was successfully deleted, False otherwise.
        """
        try:
            article = ArticleModel.get(ArticleModel.article_id == article_id)
            article.delete_instance()
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def get_article_by_id(article_id: int) -> ArticleModel:
        """
        Retrieves an article by its ID from the database.
        
        Args:
            article_id (int): The ID of the article to retrieve.
        
        Returns:
            ArticleModel: The article instance, or None if not found.
        """
        try:
            return ArticleModel.get(ArticleModel.article_id == article_id)
        except DoesNotExist:
            return None

    @staticmethod
    def get_all_articles() -> list:
        """
        Retrieves all articles from the database.
        
        Returns:
            list: A list of all articles.
        """
        try:
            query = ArticleModel.select()
            return list(query)
        except Exception as exc:
            raise RuntimeError(f"Error retrieving articles: {exc}") from exc
