import json
import random
import tempfile
import time
import ast
import importlib.util
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

PROBLEM_BANK = [
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

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.loops = 0
        self.max_loops = 0

    def visit_For(self, node):
        self.loops += 1
        self.max_loops = max(self.max_loops, self.loops)
        self.generic_visit(node)
        self.loops -= 1

    def visit_While(self, node):
        self.loops += 1
        self.max_loops = max(self.max_loops, self.loops)
        self.generic_visit(node)
        self.loops -= 1

def estimate_complexity(code):
    try:
        tree = ast.parse(code)
    except:
        return "Syntax Error"

    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)

    if analyzer.max_loops == 0:
        return "O(1) or O(n)"
    if analyzer.max_loops == 1:
        return "O(n)"
    if analyzer.max_loops == 2:
        return "O(n^2)"
    return f"O(n^{analyzer.max_loops})"

def run_and_check(func_name, code, tests):
    results = []
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        path = f.name

    spec = importlib.util.spec_from_file_location("usercode", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        return [{"ok": False, "error": str(e)}]

    func = getattr(mod, func_name, None)
    if func is None:
        return [{"ok": False, "error": "Function not found"}]

    for t in tests:
        inp = t["input"]
        expected = json.loads(t["output"])

        try:
            res = func(eval(inp))
            results.append({"ok": res == expected, "got": res, "expected": expected})
        except Exception as e:
            results.append({"ok": False, "error": str(e)})

    return results

app = FastAPI()

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSubmission(BaseModel):
    problem_id: str
    code: str

@app.get("/problems")
def get_all_problems():
    return PROBLEM_BANK

@app.post("/submit")
def submit_code(body: CodeSubmission):
    problem = next((p for p in PROBLEM_BANK if p["id"] == body.problem_id), None)
    if not problem:
        return {"error": "Problem not found"}

    func_name = problem["signature"].split()[1].split("(")[0]

    start_time = time.time()
    results = run_and_check(func_name, body.code, problem["tests"])
    passed = all(r.get("ok") for r in results)
    exec_time = time.time() - start_time

    return {
        "passed": passed,
        "test_results": results,
        "analysis": {
            "complexity": estimate_complexity(body.code),
            "time": exec_time
        }
    }
