from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
import uvicorn

from routes.game import game_router
from routes.user import user_router
from routes.security import security_router

app = FastAPI(openapi_url='/api/openapi.json')
app.include_router(game_router)
app.include_router(user_router)
app.include_router(security_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Coinche Corner Backend API Documentation")


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()


@app.exception_handler(KeyError)
async def value_error_exception_handler(request: Request, exc: KeyError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
