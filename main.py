import os
import uvicorn

from fastapi import FastAPI

from api.auth import router as auth_router
from api.profile import router as profile_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(profile_router)

# Starting the server
port = os.environ.get("PORT", 8080)
print(f"Listening to http://0.0.0.0:{port}")
uvicorn.run(app, host='0.0.0.0',port=port)