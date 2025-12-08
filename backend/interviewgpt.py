from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# ==========================
# ✅ FIXED CORS (Required for Cloudflare Pages)
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# MODELS
# ==========================

class CodeRequest(BaseModel):
    problem_id: int
    code: str

# ==========================
# DUMMY PROBLEMS (You can expand later)
# ==========================

problems_data = [
    {
        "id": 1,
        "title": "Sum of Two Numbers",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Return the sum of two numbers.",
        "signature": "def solve(a, b):",
        "starter_code": "def solve(a, b):\n    return a + b",
    },
    {
        "id": 2,
        "title": "Reverse String",
        "difficulty": "Easy",
        "companies": ["Capgemini"],
        "description": "Return the reversed string.",
        "signature": "def solve(s):",
        "starter_code": "def solve(s):\n    return s[::-1]",
    }
]

# ==========================
# ROUTES
# ==========================

@app.get("/")
def home():
    return {"message": "Backend running correctly!"}

@app.get("/problems")
def get_problems():
    return problems_data

@app.post("/submit")
def submit_code(req: CodeRequest):
    return {
        "passed": True,
        "test_results": [{"ok": True}]
    }

# Local run (ignored by Render)
if __name__ == "__main__":
    uvicorn.run("interviewgpt:app", host="0.0.0.0", port=10000)
