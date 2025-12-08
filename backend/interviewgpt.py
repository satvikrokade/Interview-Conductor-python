from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# STEP 1: Add CORS middleware FIRST (before any routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
)

# STEP 2: Add global OPTIONS handler
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    return JSONResponse(
        content={"status": "ok"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Root endpoint
@app.get("/")
async def root():
    return {"status": "running", "message": "InterviewGPT API is live"}

# Problems data
problems = [
    {
        "id": "p1",
        "title": "Two Sum",
        "difficulty": "Easy",
        "companies": ["TCS", "Infosys", "Cognizant"],
        "description": "Return indices of two numbers such that they add up to target.",
        "signature": "def two_sum(nums, target):",
        "starter_code": "def two_sum(nums, target):\n    # your code here\n    pass",
        "tests": [
            {"input": "[2,7,11,15], 9", "output": "[0,1]"},
            {"input": "[3,2,4], 6", "output": "[1,2]"}
        ]
    },
    {
        "id": "p2",
        "title": "Reverse List",
        "difficulty": "Easy",
        "companies": ["Infosys", "Wipro"],
        "description": "Given a list, return it reversed.",
        "signature": "def reverse_list(arr):",
        "starter_code": "def reverse_list(arr):\n    # your code here\n    pass",
        "tests": [
            {"input": "[1,2,3,4,5]", "output": "[5,4,3,2,1]"},
            {"input": "[]", "output": "[]"}
        ]
    },
    {
        "id": "p3",
        "title": "Check Palindrome String",
        "difficulty": "Easy",
        "companies": ["TCS", "Capgemini"],
        "description": "Return True if string is palindrome.",
        "signature": "def is_palindrome(s):",
        "starter_code": "def is_palindrome(s):\n    # your code here\n    pass",
        "tests": [
            {"input": "\"racecar\"", "output": "true"},
            {"input": "\"hello\"", "output": "false"}
        ]
    },
    {
        "id": "p4",
        "title": "Move Zeroes",
        "difficulty": "Medium",
        "companies": ["Cognizant", "Infosys"],
        "description": "Move all zeroes to the end while maintaining order.",
        "signature": "def move_zeroes(nums):",
        "starter_code": "def move_zeroes(nums):\n    # your code here\n    pass",
        "tests": [
            {"input": "[0,1,0,3,12]", "output": "[1,3,12,0,0]"},
            {"input": "[0]", "output": "[0]"}
        ]
    },
    {
        "id": "p5",
        "title": "Count Characters",
        "difficulty": "Easy",
        "companies": ["Wipro", "TCS"],
        "description": "Count frequency of each character in string.",
        "signature": "def char_count(s):",
        "starter_code": "def char_count(s):\n    # your code here\n    pass",
        "tests": [
            {"input": "\"aabb\"", "output": "{\"a\":2,\"b\":2}"},
            {"input": "\"abc\"", "output": "{\"a\":1,\"b\":1,\"c\":1}"}
        ]
    }
]

@app.get("/problems")
async def get_problems():
    """Get all problems"""
    return JSONResponse(
        content=problems,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.get("/problems/{problem_id}")
async def get_problem(problem_id: str):
    """Get specific problem"""
    problem = next((p for p in problems if p["id"] == problem_id), None)
    if not problem:
        return JSONResponse(
            content={"error": "Problem not found"},
            status_code=404,
            headers={"Access-Control-Allow-Origin": "*"}
        )
    return JSONResponse(
        content=problem,
        headers={"Access-Control-Allow-Origin": "*"}
    )

class CodeSubmission(BaseModel):
    problem_id: str
    code: str

@app.post("/submit")
async def submit_code(submission: CodeSubmission):
    """Submit code for testing"""
    problem = next((p for p in problems if p["id"] == submission.problem_id), None)
    
    if not problem:
        return JSONResponse(
            content={"success": False, "error": "Problem not found"},
            headers={"Access-Control-Allow-Origin": "*"}
        )
    
    # Extract function name
    func_name = problem["signature"].split("(")[0].replace("def ", "").strip()
    
    # Execute user code
    namespace = {}
    try:
        exec(submission.code, namespace)
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": f"Code error: {str(e)}"},
            headers={"Access-Control-Allow-Origin": "*"}
        )
    
    user_func = namespace.get(func_name)
    if not user_func:
        return JSONResponse(
            content={"success": False, "error": f"Function '{func_name}' not found"},
            headers={"Access-Control-Allow-Origin": "*"}
        )
    
    return JSONResponse(
        content={
            "success": True,
            "message": "Code submitted successfully",
            "problem_id": submission.problem_id
        },
        headers={"Access-Control-Allow-Origin": "*"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
