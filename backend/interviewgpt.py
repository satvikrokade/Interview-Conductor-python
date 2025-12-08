from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess
import tempfile
import json

app = FastAPI()

# -----------------------------
# ⭐ CORS FIX (Cloudflare Pages)
# -----------------------------
origins = [
    "http://localhost:5173",
    "https://interview-conductor-python.pages.dev",
    "https://bc5cee83.interview-conductor-python.pages.dev",
    "https://interview-conductor-python.onrender.com",
    "*",  # allow all during testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # You can replace "*" with specific domains later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 📌 Example Problems
# -----------------------------
problems = [
    {
        "id": 1,
        "title": "Two Sum",
        "description": "Given an array of numbers, return indices of two numbers that add up to a target.",
        "difficulty": "Easy",
        "companies": ["Google", "Amazon"],
        "signature": "def two_sum(nums, target):",
        "starter_code": "def two_sum(nums, target):\n    # Write your code here\n    pass",
        "tests": [
            {"input": ([2, 7, 11, 15], 9), "expected": [0, 1]},
            {"input": ([3, 2, 4], 6), "expected": [1, 2]},
        ],
    },
    {
        "id": 2,
        "title": "Reverse String",
        "description": "Return the reverse of the input string.",
        "difficulty": "Easy",
        "companies": ["Microsoft"],
        "signature": "def reverse_string(s):",
        "starter_code": "def reverse_string(s):\n    return s[::-1]",
        "tests": [
            {"input": ("hello",), "expected": "olleh"},
            {"input": ("abc",), "expected": "cba"},
        ],
    }
]

# -----------------------------
# 📌 GET /problems
# -----------------------------
@app.get("/problems")
def get_problems():
    return problems


# -----------------------------
# 📌 POST /submit → Run code
# -----------------------------
@app.post("/submit")
def submit_code(data: dict):
    problem_id = data.get("problem_id")
    code = data.get("code")

    problem = next((p for p in problems if p["id"] == problem_id), None)
    if not problem:
        return {"error": "Problem not found"}

    results = []

    # Run user code for each test case
    for test in problem["tests"]:
        expected = test["expected"]
        inp = test["input"]

        python_code = f"""
{code}

result = {problem['signature'].split("(")[0]}(*{repr(inp)})
print(result)
"""

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
                tmp.write(python_code.encode("utf-8"))
                tmp.flush()

                output = subprocess.check_output(["python3", tmp.name], stderr=subprocess.STDOUT, timeout=3)
                output = output.decode().strip()

                try:
                    output_val = json.loads(output)
                except:
                    output_val = eval(output)

                ok = output_val == expected

                results.append({
                    "ok": ok,
                    "expected": expected,
                    "got": output_val
                })

        except subprocess.CalledProcessError as e:
            return {"error": e.output.decode()}

        except subprocess.TimeoutExpired:
            return {"error": "Execution timed out"}

    passed = all(r["ok"] for r in results)

    return {
        "passed": passed,
        "test_results": results
    }


# -----------------------------
# ⭐ RUN LOCALLY
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("interviewgpt:app", host="0.0.0.0", port=8000, reload=True)
