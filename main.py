import uvicorn
from dotenv import load_dotenv
load_dotenv()
import os
port = int(os.getenv("PORT", default=8000))
if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=port, reload=True)