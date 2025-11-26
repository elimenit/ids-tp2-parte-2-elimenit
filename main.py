from fastapi import FastAPI, HTTPException
from dependencies.dpd import init_dependencias
from routers.routers import routers
from core import error_handler
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_dependencias()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # SvelteKit dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, error_handler.http_exception_handler)
app.add_exception_handler(Exception, error_handler.generic_exception_handler)
