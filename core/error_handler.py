from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# Ejemplo: manejador para HTTPException (errores típicos de FastAPI)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "path": str(request.url)
        },
    )

# Ejemplo: manejador genérico para excepciones no controladas
async def generic_exception_handler(request: Request, exc: Exception):
    # Podés loguear aquí exc con logging.error(exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Ocurrió un error inesperado.",
            "type": str(type(exc).__name__),
        },
    )
