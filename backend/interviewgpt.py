from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ------------------------------------------------------
# GLOBAL CORS FIX
# ------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    }
]

@app.get("/problems")
def get_problems():
    return problems

class CodeRequest(BaseModel):
    problem_id: int
    code: str

@app.post("/submit")
def submit(req: CodeRequest):
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
        return {"error": str(e)}

    func = local_vars.get(func_name)
    if not func:
        return {"error": f"Function `{func_name}` not found in your code"}

    results = []
    passed_all = True

    for test in problem["tests"]:
        args = test["input"]
        expected = test["expected"]

        try:
            got = func(*args)
            ok = got == expected
            if not ok:
                passed_all = False
        except Exception as e:
            got = str(e)
            ok = False
            passed_all = False

        results.append({
            "input": args,
            "expected": expected,
            "got": got,
            "ok": ok
        })

    return {
        "passed": passed_all,
        "test_results": results
    }
