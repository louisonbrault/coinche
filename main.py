from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
import uvicorn

from routes.game import game_router
from routes.user import user_router
from routes.security import security_router

app = FastAPI()
app.include_router(game_router)
app.include_router(user_router)
app.include_router(security_router)
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(KeyError)
async def value_error_exception_handler(request: Request, exc: KeyError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
