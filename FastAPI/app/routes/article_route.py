""" article_route.py"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from peewee import IntegrityError
from schemas.article import Article
from services.article_service import ArticleService

article_router = APIRouter()


class ArticleUpdate(BaseModel):
    """
    Schema for updating an existing article.
    """

    title: Optional[str] = None
    content: Optional[str] = None
    author_id: Optional[int] = None
    published_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None


@article_router.get("/articles", response_model=List[Article])
def get_articles():
    """
    Retrieve all articles.
    """
    try:
        articles = ArticleService.get_all_articles()  # Cambiado para usar el servicio
        return [Article.from_orm(article) for article in articles]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@article_router.get("/article/{article_id}", response_model=Article)
def get_article(article_id: int):
    """
    Retrieve a specific article by ID.
    """
    try:
        article = ArticleService.get_article_by_id(
            article_id
        )  # Cambiado para usar el servicio
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return Article.from_orm(article)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@article_router.post("/article", response_model=Article)
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
        return Article.from_orm(article_data)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@article_router.put("/article/{article_id}", response_model=Article)
def update_article(article_id: int, article_data: ArticleUpdate):
    """
    Update a specific article by ID.
    """
    try:
        article_update_data = article_data.dict(exclude_unset=True)
        updated_article = ArticleService.update_article(
            article_id, **article_update_data
        )
        return Article.from_orm(updated_article)
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
