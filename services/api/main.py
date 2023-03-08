from time import sleep

from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from fastapi import HTTPException

from db.client import BaseManager
from services.api.utils import ORJSONResponse
from services.api.v1.qa.endpoints import router


app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url="/core/public/v1/docs",
    openapi_url="/core/public/v1/openapi.json",
)
app.add_middleware(BrotliMiddleware)

app.include_router(router, prefix="/qa", tags=["qa"])


@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    headers = getattr(exc, "headers", None)

    return ORJSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
        headers=headers or None,
    )


@app.on_event("startup")
async def startup():
    sleep(25)  # HACK do not repeat in production: wait for singlestore to set up
    BaseManager.db_client.connect()
