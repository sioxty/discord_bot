from src.routes import router
import fastapi
import uvicorn

app = fastapi.FastAPI()

app.include_router(router)

if  __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)