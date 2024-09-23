from typing import List, Optional
import datetime
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from peewee import DoesNotExist, IntegrityError
from schemas.article import Article 
from services.article_service import ArticleService

article_route = APIRouter()

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author_id_article: Optional[int] = None  # Cambiado aquí
    published_date: Optional[datetime.datetime] = None
    updated_date: Optional[datetime.datetime] = None

@article_route.get("/articles", response_model=List[Article])
def get_articles():
    try:
        articles = ArticleService.get_all_articles()
        return [
            Article(
                article_id=article.id,
                title=article.title,
                content=article.content,
                author_id_article=article.author_id_article.author_id if article.author_id_article else None,
                published_date=article.published_date
            ) for article in articles
        ]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@article_route.get("/article/{article_id}", response_model=Article)
def get_article(article_id: int):
    try:
        article = ArticleService.get_article_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return Article.from_orm(article)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@article_route.post("/article", response_model=Article)
def create_article(article: Article = Body(...)):
    try:
        article_data = ArticleService.create_article(
            title=article.title,
            author_id_article=article.author_id_article, 
            category=article.category,
            content=article.content,
            published_date=article.published_date,
            status=article.status,
            updated_date=article.updated_date
        )
        return Article.from_orm(article_data)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@article_route.put("/article/{article_id}", response_model=Article)
def update_article(article_id: int, article_data: ArticleUpdate):
    try:
        article_update_data = article_data.dict(exclude_unset=True)
        updated_article = ArticleService.update_article(article_id, **article_update_data)
        return Article.from_orm(updated_article)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@article_route.delete("/article/{article_id}")
def delete_article(article_id: int):
    try:
        if not ArticleService.delete_article(article_id):
            raise HTTPException(status_code=404, detail="Article not found")
        return {"detail": "Article deleted successfully"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
