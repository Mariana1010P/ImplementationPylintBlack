"""
This module contains the definition of the Author class,
which represents an author schema using Pydantic.

The Author class includes attributes such as author_id, name, and affiliation.
"""

from pydantic import BaseModel


class Author(BaseModel):
    """
    Schema representing an Author.

    Attributes:
        author_id (int): Unique identifier for the author.
        name (str): Name of the author.
        affiliation (str): Affiliation of the author.
    """

    author_id: int
    name: str
    affiliation: str
