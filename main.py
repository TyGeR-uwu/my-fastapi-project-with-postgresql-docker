import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host=settings.host, port=settings.port)