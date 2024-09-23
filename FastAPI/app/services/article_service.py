import datetime
from peewee import DoesNotExist, IntegrityError
from config.database import ArticleModel

class ArticleService:
    @staticmethod
    def create_article(
        title: str, author_id_article: int, content: str,
        published_date: datetime.datetime,  
    ) -> ArticleModel:
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
        try:
            article = ArticleModel.get(ArticleModel.article_id == article_id)
            for key, value in kwargs.items():
                setattr(article, key, value)
            article.save()
            return article
        except DoesNotExist:
            raise ValueError(f"No article found with ID: {article_id}")
        except IntegrityError as exc:
            raise ValueError(f"Failed to update article: {exc}") from exc

    @staticmethod
    def delete_article(article_id: int) -> bool:
        try:
            article = ArticleModel.get(ArticleModel.article_id == article_id)
            article.delete_instance()
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def get_article_by_id(article_id: int) -> ArticleModel:
        try:
            return ArticleModel.get(ArticleModel.article_id == article_id)
        except DoesNotExist:
            return None

    @staticmethod
    def get_all_articles() -> list:
        try:
            query = ArticleModel.select()
            print(query.sql())  # Esto imprime la consulta generada
            return list(query)
        except Exception as exc:
            raise RuntimeError(f"Error retrieving articles: {exc}") from exc
