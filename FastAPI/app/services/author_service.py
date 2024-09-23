"""
Module that provides service functionality for managing authors in the database.
"""

from peewee import DoesNotExist, IntegrityError  # type: ignore
from config.database import AuthorModel


class AuthorService:
    """
    Service class for handling business logic related to authors.

    Attributes:
        author_repository (AuthorRepository): The repository used to interact with the database.

    Methods:
        create_author(author_id: int, name: str, affiliation: str)
        update_author(author_id: int, name: str, affiliation: str)
        delete_author(author_id: int)
        get_author_by_id(author_id: int)
        get_all_authors()

    Raises:
        ValueError: If any data validation fails.
        IntegrityError: If there's an integrity error during creation.
        DoesNotExist: If no author with the given ID exists.
        runtimeError: If there's an error during the operation.
    """

    @staticmethod
    def create_author(name: str, affiliation: str) -> AuthorModel:
        """
        Creates a new author in the database.

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
            return AuthorModel.create(name=name, affiliation=affiliation)
        except IntegrityError as exc:
            raise ValueError(f"Failed to create author: {exc}") from exc

    @staticmethod
    def update_author(author_id: int, name: str, affiliation: str) -> AuthorModel:
        """
        Updates an author in the database.

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
            author = AuthorModel.get(AuthorModel.author_id == author_id)
            author.name = name
            author.affiliation = affiliation
            author.save()
            return author
        except DoesNotExist:
            return None
        except Exception as exc:
            raise RuntimeError(f"Error al actualizar el autor: {exc}") from exc

    @staticmethod
    def delete_author(author_id: int) -> bool:
        """
        Deletes an author from the database.

        Args:
            author_id (int): The ID of the author to delete.

        Raises:
            DoesNotExist: If no author with the given ID exists.
        """
        try:
            author = AuthorModel.get(AuthorModel.author_id == author_id)
            author.delete_instance()
            return True
        except DoesNotExist:
            return False
        except Exception as exc:
            raise RuntimeError(f"Error al eliminar el autor: {exc}") from exc

    @staticmethod
    def get_author_by_id(author_id: int) -> AuthorModel:
        """
        Retrieves an author by ID.

        Args:
            author_id (int): The ID of the author to retrieve.

        Returns:
            AuthorModel: The author with the given ID.

        Raises:
            DoesNotExist: If no author with the given ID exists.
        """
        try:
            return AuthorModel.get(AuthorModel.author_id == author_id)
        except DoesNotExist:
            return None
        except Exception as exc:
            raise RuntimeError(f"Error al obtener el autor: {exc}") from exc

    @staticmethod
    def get_all_authors() -> list:
        """
        Retrieves all authors from the database.

        Returns:
            list: A list of all authors.
        """
        try:
            return list(AuthorModel.select())
        except Exception as exc:
            raise RuntimeError(f"Error al obtener autores: {exc}") from exc
