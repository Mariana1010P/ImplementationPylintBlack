""" article_route.py"""

from fastapi import APIRouter, Body, HTTPException
from peewee import IntegrityError
from schemas.article import Article
from services.article_service import ArticleService

article_router = APIRouter()


@article_router.get("/articles")
def get_articles():
    """
    Retrieve all articles.
    """
    try:
        articles = ArticleService.get_all_articles()
        return {"articles": articles}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@article_router.get("/article/{article_id}")
def get_article_by_id(article_id: int):
    """
    Retrieve a specific article by ID.
    """
    try:
        article = ArticleService.get_article_by_id(
            article_id
        ) 
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@article_router.post("/article")
def create_article(article: Article = Body(...)):
    """
    Create a new article.
    """
    try:
        article_data = ArticleService.create_article(
            title=article.title,
            author_id=article.author_id,
            content=article.content,
            published_date=article.published_date,
        )
        return article_data
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@article_router.put("/article/{article_id}")
def update_article(article_id: int, article_data: Article = Body(...)):
    """
    Update a specific article by ID.
    """
    try:
        updated_article = ArticleService.update_article(
            article_id=article_id,
            title=article_data.title,
            content=article_data.content,
            author_id=article_data.author_id,
            published_date=article_data.published_date,
        )
        return {"message": "Article updated", "article": updated_article}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@article_router.delete("/article/{article_id}")
def delete_article(article_id: int):
    """
    Delete a specific article by ID.
    """
    try:
        if not ArticleService.delete_article(article_id):
            raise HTTPException(status_code=404, detail="Article not found")
        return {"detail": "Article deleted successfully"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
