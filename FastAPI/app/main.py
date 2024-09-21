""" FastAPI """

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.responses import RedirectResponse
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
        "name": "Mariana",
        "url": "https://github.com/Mariana1010P/ImplementacionPylintBlack",
        "email": "mariana1010.pe@gmail.com",
    },
    lifespan=manage_lifespan,  # Mueve la función aquí
)


@app.get("/")
def read_root():
    """
    Redirects to the Swagger UI documentation.
    """
    return RedirectResponse(url="/docs")