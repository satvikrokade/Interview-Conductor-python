from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ------------------------------------------------------
# ENHANCED CORS FIX - Handles OPTIONS preflight
# ------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, list specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight for 1 hour
)

# ------------------------------------------------------
# Health Check
# ------------------------------------------------------
@app.get("/")
def root():
    return {"status": "healthy", "message": "InterviewGPT API is running"}

# ------------------------------------------------------
# Problems List
# ------------------------------------------------------
problems = [
    {
        "id": 1,
        "title": "Two Sum",
        "description": "Find two numbers that add up to target.",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "signature": "def two_sum(nums, target):",
        "starter_code": "def two_sum(nums, target):\n    pass",
        "tests": [
            {"input": ([2,7,11,15], 9), "expected": [0,1]},
            {"input": ([3,2,4], 6), "expected": [1,2]}
        ]
    },
    {
        "id": 2,
        "title": "Reverse String",
        "description": "Write a function that reverses a string. The input string is given as an array of characters.",
        "difficulty": "Easy",
        "companies": ["Google", "Amazon"],
        "signature": "def reverse_string(s):",
        "starter_code": "def reverse_string(s):\n    pass",
        "tests": [
            {"input": (["h","e","l","l","o"],), "expected": ["o","l","l","e","h"]},
            {"input": (["H","a","n","n","a","h"],), "expected": ["h","a","n","n","a","H"]}
        ]
    },
    {
        "id": 3,
        "title": "Valid Palindrome",
        "description": "Given a string s, return true if it is a palindrome, or false otherwise.",
        "difficulty": "Easy",
        "companies": ["Facebook", "Microsoft"],
        "signature": "def is_palindrome(s):",
        "starter_code": "def is_palindrome(s):\n    pass",
        "tests": [
            {"input": ("A man, a plan, a canal: Panama",), "expected": True},
            {"input": ("race a car",), "expected": False}
        ]
    },
    {
        "id": 4,
        "title": "Maximum Subarray",
        "description": "Given an integer array nums, find the subarray with the largest sum, and return its sum.",
        "difficulty": "Medium",
        "companies": ["Amazon", "Microsoft", "Google"],
        "signature": "def max_subarray(nums):",
        "starter_code": "def max_subarray(nums):\n    pass",
        "tests": [
            {"input": ([-2,1,-3,4,-1,2,1,-5,4],), "expected": 6},
            {"input": ([1],), "expected": 1},
            {"input": ([5,4,-1,7,8],), "expected": 23}
        ]
    },
    {
        "id": 5,
        "title": "Binary Search",
        "description": "Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.",
        "difficulty": "Easy",
        "companies": ["Google", "Amazon", "Facebook"],
        "signature": "def binary_search(nums, target):",
        "starter_code": "def binary_search(nums, target):\n    pass",
        "tests": [
            {"input": ([-1,0,3,5,9,12], 9), "expected": 4},
            {"input": ([-1,0,3,5,9,12], 2), "expected": -1}
        ]
    }
]

@app.get("/problems")
def get_problems():
    """Get all coding problems"""
    return problems

@app.get("/problems/{problem_id}")
def get_problem(problem_id: int):
    """Get a specific problem by ID"""
    problem = next((p for p in problems if p["id"] == problem_id), None)
    if not problem:
        return {"error": "Problem not found"}
    return problem

class CodeRequest(BaseModel):
    problem_id: int
    code: str

@app.post("/submit")
def submit(req: CodeRequest):
    """Submit code for a problem and run tests"""
    problem = next((p for p in problems if p["id"] == req.problem_id), None)
    if not problem:
        return {"error": "Problem not found"}
    
    # Extract function name
    func_name = problem["signature"].split("(")[0].replace("def ", "").strip()
    
    # Execute the submitted code safely
    local_vars = {}
    try:
        exec(req.code, {}, local_vars)
    except Exception as e:
        return {"error": f"Syntax Error: {str(e)}"}
    
    func = local_vars.get(func_name)
    if not func:
        return {"error": f"Function `{func_name}` not found in your code"}
    
    results = []
    passed_all = True
    
    for i, test in enumerate(problem["tests"]):
        args = test["input"]
        expected = test["expected"]
        try:
            got = func(*args)
            ok = got == expected
            if not ok:
                passed_all = False
        except Exception as e:
            got = f"Error: {str(e)}"
            ok = False
            passed_all = False
        
        results.append({
            "test_number": i + 1,
            "input": args,
            "expected": expected,
            "got": got,
            "passed": ok
        })
    
    return {
        "passed": passed_all,
        "total_tests": len(problem["tests"]),
        "passed_tests": sum(1 for r in results if r["passed"]),
        "test_results": results
    }

# ------------------------------------------------------
# For local testing
# ------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
