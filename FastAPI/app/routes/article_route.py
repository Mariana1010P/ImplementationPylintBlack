from typing import List
from fastapi import APIRouter, Body, HTTPException
from peewee import DoesNotExist, IntegrityError
from schemas.article import Article
from services.article_service import ArticleService

article_route = APIRouter()

@article_route.get("/articles")
def get_all_articles():
    """
    Retrieves all articles from the database.

    Returns:
        list: A list of all articles.
    """
    try:
        articles = ArticleService.get_all_articles()
        return {"articles": articles}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@article_route.get("/articles/{article_id}")
def get_article_by_id(article_id: int):
    """
    Retrieves an article by ID.

    Args:
        article_id (int): The ID of the article to retrieve.

    Returns:
        ArticleModel: The article with the given ID.
    """
    try:
        article = ArticleService.get_article_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"article": article}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@article_route.post("/articles")
def create_article(article: Article = Body(...)):
    """
    Creates a new article.

    Args:
        title (str): The title of the article.
        content (str): The content of the article.
        author_id_article (int): The author ID associated with the article.
        published_date (datetime): The date the article was published.

    Returns:
        ArticleModel: The created article.
    """
    try:
        article_instance = ArticleService.create_article(
            title=article.title,
            author_id_article=article.author_id_article,
            content=article.content,
            published_date=article.published_date
        )
        return {"message": "Article created", "article": article_instance}
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(exc)}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
        
@article_route.put("/article/{article_id}", response_model=Article)
def update_article(article_id: int, article_data: Article):
    """
    Updates an article.
    ...
    """
    try:
        article_update_data = article_data.dict(exclude_unset=True)
        article_update_data.pop('article_id', None)  # Elimina article_id del diccionario

        updated_article = ArticleService.update_article(article_id, **article_update_data)
        return Article.from_orm(updated_article)
    except ValueError:
        raise HTTPException(status_code=404, detail="Article not found")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Error de integridad: " + str(e))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc



@article_route.delete("/articles/{article_id}")
def delete_article(article_id: int):
    """
    Deletes an article by ID.

    Args:
        article_id (int): The ID of the article to delete.

    Returns:
        dict: A dictionary containing a success message.
    """
    try:
        success = ArticleService.delete_article(article_id)
        if not success:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"message": "Article deleted"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
