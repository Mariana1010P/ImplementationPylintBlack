"""
This module configures and manages the database connection using Peewee ORM.
"""

import os
from dotenv import load_dotenv
from peewee import Model, MySQLDatabase, AutoField, CharField  # type: ignore

# Load environment variables from a .env file
load_dotenv()

# Configure the MySQL database connection
database = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
)


# pylint: disable=too-few-public-methods
class AuthorModel(Model):
    """
    AuthorModel class for representing the 'author' table in the database.

    Attributes:
        author_id (AutoField): The unique identifier for the author.
        name (CharField): The name of the author.
        affiliation (CharField): The affiliation of the author.
    """

    author_id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=False)
    affiliation = CharField(max_length=50, null=False, default="Sin afiliación")

    class Meta:
        """
        Meta class for the 'author' table in the database.

        Attributes:
            database (MySQLDatabase): The database connection used by the model.
            table_name (str): The name of the table in the database.
        """

        database = database
        table_name = "author"
