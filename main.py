# main.py
from fastapi import FastAPI
from config.settings import setup_cors, setup_logging
from apis import bloat_controller
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="GitHub Release Bloat API",
    description="An API for tracking GitHub release artifact size changes over time.",
    version="1.0.0",
)

setup_cors(app)
logger = setup_logging()

app.include_router(bloat_controller.router, prefix="/api/v1")

@app.on_event("startup")
def customize_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="GitHub Release Bloat API",
        version="1.0.0",
        description="An API for tracking GitHub release artifact size changes over time.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "github-token",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"ApiKeyAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
