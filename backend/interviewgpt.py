from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS FIX - Allow Cloudflare Frontend + Localhost
origins = [
    "http://localhost:5173",
    "https://*.pages.dev",   # All Cloudflare Pages URLs
    "https://interview-conductor-python.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (safest for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example problems route
@app.get("/problems")
def get_problems():
    return [
        {"id": 1, "title": "Two Sum", "difficulty": "Easy", "companies": ["TCS"]},
        {"id": 2, "title": "Reverse Number", "difficulty": "Easy", "companies": ["Capgemini"]},
    ]

@app.post("/submit")
def submit_code(data: dict):
    return {
        "passed": True,
        "test_results": [{"ok": True}]
    }

@app.get("/")
def home():
    return {"message": "Backend running!"}

if __name__ == "__main__":
    uvicorn.run("interviewgpt:app", host="0.0.0.0", port=10000)
