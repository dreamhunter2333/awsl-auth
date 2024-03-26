import os
import logging
import uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse

from router.auth_router import router as auth_router
from router.info_router import router as info_router
from router.user_router import router as user_router


_logger = logging.getLogger(__name__)

app = FastAPI(title="Awsl Auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(info_router)
app.include_router(user_router)

if os.path.exists("dist"):

    NON_INDEX_PATH = ["/api", "/docs", "/openapi.json"]
    ASSETS_PATH = "/assets"
    ASSETS_SUFFIX = [".js", ".css", ".png", ".jpg", ".jpeg", ".svg", ".ico"]
    static = StaticFiles(directory="dist")

    class StaticMiddleware:
        def __init__(self, app, *args, **kwargs) -> None:
            self.app = app

        async def __call__(self, scope, receive, send) -> None:
            if scope["type"] != "http":
                await self.app(scope, receive, send)
                return
            req_path = scope.get("path", "/")
            if req_path.startswith(ASSETS_PATH) or any(
                req_path.endswith(suffix)
                for suffix in ASSETS_SUFFIX
            ):
                await static(scope, receive, send)
                return
            await self.app(scope, receive, send)

    async def read_index(request: Request):
        return FileResponse(
            "dist/index.html",
            headers={"Cache-Control": "no-cache"}
        )

    @app.middleware("http")
    async def index_middleware(request: Request, call_next):
        if not any(
            request.url.path.startswith(path)
            for path in NON_INDEX_PATH
        ):
            return await read_index(request)
        else:
            return await call_next(request)

    app.add_middleware(StaticMiddleware)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return PlainTextResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=f"Internal Server Error: {exc}",
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
