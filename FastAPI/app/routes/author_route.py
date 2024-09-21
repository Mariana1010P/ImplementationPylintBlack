"""
author_route.py

This module defines the API endpoints for handling authors.
"""

from fastapi import APIRouter, Body, HTTPException
from schemas.author import Author
from services.author_service import AuthorService  # type: ignore

author_router = APIRouter()
# pylint: disable=no-value-for-parameter


@author_router.get("/authors")
def get_all_authors():
    """
    Retrieves all authors from the database.

    Returns:
        list: A list of all authors.

    Raises:
        ValueError: If the author_id is invalid.
        DoesNotExist: If no author with the given ID exists.
    """
    try:
        authors = AuthorService.get_all_authors()
        return {"authors": authors}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@author_router.get("/authors/{author_id}")
def get_author_by_id(author_id: int):
    """
    Retrieves an author by ID.

    Args:
        author_id (int): The ID of the author to retrieve.

    Returns:
        AuthorModel: The author with the given ID.

    Raises:
        ValueError: If the author_id is invalid.
        DoesNotExist: If no author with the given ID exists.
    """
    try:
        author = AuthorService.get_author_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving the author"
        ) from exc


@author_router.post("/authors")
def create_author(author: Author = Body(...)):
    """
    Creates a new author.

    Args:
        name (str): The name of the author.
        affiliation (str): The affiliation of the author.

    Returns:
        AuthorModel: The created author.

    Raises:
        ValueError: If any data validation fails.
        IntegrityError: If there's an integrity error during creation.
    """
    try:
        author_instance = AuthorService.create_author(
            name=author.name, affiliation=author.affiliation
        )
        return {"message": "Author created", "author": author_instance}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the author"
        ) from exc


@author_router.put("/authors/{author_id}")
def update_author(author_id: int, author: Author = Body(...)):
    """
    Updates an author.

    Args:
        author_id (int): The ID of the author to update.
        name (str): The new name of the author.
        affiliation (str): The new affiliation of the author.

    Returns:
        AuthorModel: The updated author.

    Raises:
        ValueError: If any data validation fails.
        DoesNotExist: If no author with the given ID exists.
        IntegrityError: If there's an integrity error during update.

    """
    try:
        updated_author = AuthorService.update_author(
            author_id, name=author.name, affiliation=author.affiliation
        )
        if not updated_author:
            raise HTTPException(status_code=404, detail="Author not found")
        return {"message": "Author updated", "author": updated_author}
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the author"
        ) from exc


@author_router.delete("/authors/{author_id}")
def delete_author(author_id: int):
    """
    Delete an author by ID.

    Args:
        author_id (int): The ID of the author to delete.

    Returns:
        dict: A dictionary containing a success message.
    """
    try:
        success = AuthorService.delete_author(author_id)
        if not success:
            raise HTTPException(status_code=404, detail="Author not found")
        return {"message": "Author deleted"}
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the author"
        ) from exc
