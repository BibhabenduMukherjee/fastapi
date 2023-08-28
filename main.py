import uvicorn
from os import getenv

port = int(getenv("PORT", default=8000))
if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=port, reload=True)
