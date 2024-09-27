import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI()
app.include_router(router)
app.add_middleware(
 CORSMiddleware,
 allow_origins=["http://localhost:5173"], # Add your frontend origin here
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
 )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

