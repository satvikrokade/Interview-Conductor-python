from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import traceback

app = FastAPI()

# ---------------------------------------------------------
# CORS FIX (Required for Cloudflare Pages)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow your Cloudflare frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# PROBLEM DATABASE (20 Problems)
# ---------------------------------------------------------

problems = [

    # ---------- TCS Problems (10) ----------
    {
        "id": 1,
        "title": "Sum of Digits",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Return the sum of all digits in an integer.",
        "signature": "def solve(n):",
        "starter_code": "def solve(n):\n    # write code\n    pass",
        "tests": [
            {"input": 123, "output": 6},
            {"input": 905, "output": 14},
        ]
    },
    {
        "id": 2,
        "title": "Reverse String",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Return the reversed string.",
        "signature": "def solve(s):",
        "starter_code": "def solve(s):\n    pass",
        "tests": [
            {"input": "hello", "output": "olleh"},
            {"input": "TCS", "output": "SCT"},
        ]
    },
    {
        "id": 3,
        "title": "Check Prime",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Determine if a number is prime.",
        "signature": "def solve(n):",
        "starter_code": "def solve(n):\n    pass",
        "tests": [
            {"input": 7, "output": True},
            {"input": 12, "output": False},
        ]
    },
    {
        "id": 4,
        "title": "Fibonacci Number",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Return nth Fibonacci number.",
        "signature": "def solve(n):",
        "starter_code": "def solve(n):\n    pass",
        "tests": [
            {"input": 5, "output": 5},
            {"input": 7, "output": 13},
        ]
    },
    {
        "id": 5,
        "title": "Factorial",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Return factorial of n.",
        "signature": "def solve(n):",
        "starter_code": "def solve(n):\n    pass",
        "tests": [
            {"input": 5, "output": 120},
            {"input": 1, "output": 1},
        ]
    },
    {
        "id": 6,
        "title": "Count Vowels",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Count vowels in a string.",
        "signature": "def solve(s):",
        "starter_code": "def solve(s):\n    pass",
        "tests": [
            {"input": "hello", "output": 2},
            {"input": "TCS", "output": 0},
        ]
    },
    {
        "id": 7,
        "title": "Check Palindrome",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Check if string is palindrome.",
        "signature": "def solve(s):",
        "starter_code": "def solve(s):\n    pass",
        "tests": [
            {"input": "level", "output": True},
            {"input": "world", "output": False},
        ]
    },
    {
        "id": 8,
        "title": "Greatest of Three Numbers",
        "difficulty": "Easy",
        "companies": ["TCS"],
        "description": "Return greatest of three numbers.",
        "signature": "def solve(a, b, c):",
        "starter_code": "def solve(a, b, c):\n    pass",
        "tests": [
            {"input": [2, 5, 1], "output": 5},
            {"input": [9, 9, 3], "output": 9},
        ]
    },
    {
        "id": 9,
        "title": "Armstrong Number",
        "difficulty": "Medium",
        "companies": ["TCS"],
        "description": "Check if number is Armstrong.",
        "signature": "def solve(n):",
        "starter_code": "def solve(n):\n    pass",
        "tests": [
            {"input": 153, "output": True},
            {"input": 123, "output": False},
        ]
    },
    {
        "id": 10,
        "title": "Anagram Check",
        "difficulty": "Medium",
        "companies": ["TCS"],
        "description": "Check if two strings are anagram.",
        "signature": "def solve(a, b):",
        "starter_code": "def solve(a, b):\n    pass",
        "tests": [
            {"input": ["listen", "silent"], "output": True},
            {"input": ["hello", "world"], "output": False},
        ]
    },

    # ---------- Capgemini Problems (10) ----------
    {
        "id": 11,
        "title": "Second Largest",
        "difficulty": "Easy",
        "companies": ["Capgemini"],
        "description": "Find the second largest element.",
        "signature": "def solve(arr):",
        "starter_code": "def solve(arr):\n    pass",
        "tests": [
            {"input": [1, 5, 2, 9], "output": 5},
            {"input": [10, 20, 30], "output": 20},
        ]
    },
    {
        "id": 12,
        "title": "Remove Duplicates",
        "difficulty": "Easy",
        "companies": ["Capgemini"],
        "description": "Remove duplicates from list while maintaining order.",
        "signature": "def solve(arr):",
        "starter_code": "def solve(arr):\n    pass",
        "tests": [
            {"input": [1,2,2,3], "output": [1,2,3]},
        ]
    },
    {
        "id": 13,
        "title": "Check Sorted",
        "difficulty": "Easy",
        "companies": ["Capgemini"],
        "description": "Check if list is sorted.",
        "signature": "def solve(arr):",
        "starter_code": "def solve(arr):\n    pass",
        "tests": [
            {"input": [1,2,3], "output": True},
            {"input": [3,1,2], "output": False},
        ]
    },
    {
        "id": 14,
        "title": "Binary Search",
        "difficulty": "Medium",
        "companies": ["Capgemini"],
        "description": "Implement binary search.",
        "signature": "def solve(arr, target):",
        "starter_code": "def solve(arr, target):\n    pass",
        "tests": [
            {"input": [[1,2,3,4], 3], "output": 2},
        ]
    },
    {
        "id": 15,
        "title": "Matrix Sum",
        "difficulty": "Medium",
        "companies": ["Capgemini"],
        "description": "Return sum of matrix elements.",
        "signature": "def solve(matrix):",
        "starter_code": "def solve(matrix):\n    pass",
        "tests": [
            {"input": [[1,2],[3,4]], "output": 10},
        ]
    },
    {
        "id": 16,
        "title": "Count Words",
        "difficulty": "Easy",
        "companies": ["Capgemini"],
        "description": "Return number of words in a string.",
        "signature": "def solve(s):",
        "starter_code": "def solve(s):\n    pass",
        "tests": [
            {"input": "hello world", "output": 2},
        ]
    },
    {
        "id": 17,
        "title": "Find Missing Number",
        "difficulty": "Medium",
        "companies": ["Capgemini"],
        "description": "Given 1..n find missing number.",
        "signature": "def solve(arr, n):",
        "starter_code": "def solve(arr, n):\n    pass",
        "tests": [
            {"input": [[1,2,4,5], 5], "output": 3},
        ]
    },
    {
        "id": 18,
        "title": "Longest Word",
        "difficulty": "Easy",
        "companies": ["Capgemini"],
        "description": "Return longest word in string.",
        "signature": "def solve(s):",
        "starter_code": "def solve(s):\n    pass",
        "tests": [
            {"input": "I love programming", "output": "programming"},
        ]
    },
    {
        "id": 19,
        "title": "Sum of Array",
        "difficulty": "Easy",
        "companies": ["Capgemini"],
        "description": "Return sum of array.",
        "signature": "def solve(arr):",
        "starter_code": "def solve(arr):\n    pass",
        "tests": [
            {"input": [1,2,3], "output": 6},
        ]
    },
    {
        "id": 20,
        "title": "Find Duplicates",
        "difficulty": "Medium",
        "companies": ["Capgemini"],
        "description": "Return repeated elements in array.",
        "signature": "def solve(arr):",
        "starter_code": "def solve(arr):\n    pass",
        "tests": [
            {"input": [1,2,2,3,3], "output": [2,3]},
        ]
    },
]

# ---------------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------------
class CodeInput(BaseModel):
    problem_id: int
    code: str

# ---------------------------------------------------------
# RETURN PROBLEMS
# ---------------------------------------------------------
@app.get("/problems")
def get_problems():
    return problems

# ---------------------------------------------------------
# EXECUTE SUBMITTED CODE
# ---------------------------------------------------------
@app.post("/submit")
def submit_code(payload: CodeInput):
    problem = next((p for p in problems if p["id"] == payload.problem_id), None)
    if not problem:
        return {"error": "Problem not found"}

    results = []

    for test in problem["tests"]:
        try:
            # prepare environment
            local_env = {}
            exec(payload.code, {}, local_env)

            func = local_env.get("solve")
            if not func:
                return {"error": "Function 'solve' not found in your code"}

            inp = test["input"]
            if isinstance(inp, list):
                output = func(*inp)
            else:
                output = func(inp)

            ok = output == test["output"]

            results.append({
                "ok": ok,
                "expected": test["output"],
                "got": output
            })

        except Exception as e:
            return {"error": traceback.format_exc()}

    return {
        "passed": all(r["ok"] for r in results),
        "test_results": results
    }
