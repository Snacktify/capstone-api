import uvicorn
from fastapi import FastAPI
from api.auth import router as auth_router
from api.profile import router as profile_router
from api.predict import router as predict_router
from api.snackvidia import router as snackvidia_router

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(predict_router)
app.include_router(snackvidia_router)

@app.get("/")
def index():
    return "Hi, welcome to the snacktify API"

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "http://34.128.89.110:8080",
    "https://storage.googleapis.com/static-website-snacktify/Landing.html"

    # Tambahkan asal lainnya yang diperlukan
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)