from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Allow frontend hosted on Cloudflare Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load problems from JSON file
with open("problems.json", "r") as f:
    PROBLEMS = json.load(f)


@app.get("/")
def home():
    return {"status": "Backend running successfully!"}


@app.get("/problems")
def get_problems():
    return PROBLEMS


@app.post("/submit")
def submit_code(payload: dict):
    problem_id = payload["problem_id"]
    code = payload["code"]

    problem = next((p for p in PROBLEMS if p["id"] == problem_id), None)
    if not problem:
        return {"error": "Invalid problem ID"}

    results = []
    global_namespace = {}

    # Compile user code
    try:
        exec(code, global_namespace)
    except Exception as e:
        return {"error": str(e)}

    func_name = problem["signature"].split("(")[0].replace("def", "").strip()
    func = global_namespace.get(func_name)

    if not func:
        return {"error": f"Function '{func_name}' not found in code"}

    passed_all = True

    for t in problem["tests"]:
        try:
            expr = f"func({t['input']})"
            user_output = eval(expr, {"func": func})

            expected = json.loads(
                t["output"]
                .replace("true", "true")
                .replace("false", "false")
            )
        except Exception as e:
            results.append({"ok": False, "expected": t["output"], "got": str(e)})
            passed_all = False
            continue

        ok = (str(user_output) == str(expected))
        if not ok:
            passed_all = False

        results.append({
            "ok": ok,
            "expected": expected,
            "got": user_output
        })

    return {"passed": passed_all, "test_results": results}
