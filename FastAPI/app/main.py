""" FastAPI """

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
from helpers.api_key_auth import get_api_key
from routes.author_route import author_router
from routes.article_route import article_route
from config.database import database as connection  # type: ignore


@asynccontextmanager
async def manage_lifespan(_app: FastAPI):
    """
    Manage the lifespan of the FastAPI application.

    Args:
        _app (FastAPI): The FastAPI application.

    Yields:
        None
    """
    if connection.is_closed():
        connection.connect()
    try:
        yield
    finally:
        if not connection.is_closed():
            connection.close()


app = FastAPI(
    title="Implementación de Pylint y PEP8",
    version="2.0",
    contact={
        "name": "Mariana and Alejandro",
        "url": "https://github.com/Mariana1010P/ImplementacionPylintBlack",
    },
    lifespan=manage_lifespan,
)


@app.get("/")
def read_root():
    """
    Redirects to the Swagger UI documentation.
    """
    return RedirectResponse(url="/docs")


app.include_router(
    author_router, prefix="/authors", tags="authors", dependencies=[Depends(get_api_key)]
)


app.include_router(
    article_route, prefix="/articles", tags="articles",dependencies=[Depends(get_api_key)]
)
