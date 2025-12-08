from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI()

# ------------------------------------------------------
# CORS FIX (required for Cloudflare Pages frontend)
# ------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow ALL origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------
# Problem definitions
# ------------------------------------------------------
problems = [
    {
        "id": 1,
        "title": "Two Sum",
        "description": "Return indices of two numbers that add up to target.",
        "difficulty": "Easy",
        "companies": ["Google", "Amazon"],
        "signature": "def two_sum(nums, target):",
        "starter_code": "def two_sum(nums, target):\n    pass",
        "tests": [
            {"input": ([2,7,11,15], 9), "expected": [0,1]},
            {"input": ([3,2,4], 6), "expected": [1,2]}
        ]
    },
    # (your added problems go here)
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

    signature = problem["signature"]
    tests = problem["tests"]

    full_code = req.code + "\nresult = " + signature.split("(")[0] + "("

    try:
        local_vars = {}
        exec(req.code, {}, local_vars)
    except Exception as e:
        return {"error": str(e)}

    results = []
    passed = True

    for t in tests:
        inp = t["input"]
        expected = t["expected"]

        try:
            func = local_vars[signature.split("(")[0]]
            got = func(*inp)
            ok = got == expected
            if not ok:
                passed = False
        except Exception as e:
            got = str(e)
            ok = False
            passed = False

        results.append({"input": inp, "expected": expected, "got": got, "ok": ok})

    return {"passed": passed, "test_results": results}
