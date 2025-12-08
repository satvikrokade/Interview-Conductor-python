import React, { useEffect, useState } from "react";

export default function App() {
  // Always use backend URL (Render)
  const API_BASE = "https://interview-conductor-python.onrender.com";

  const [problems, setProblems] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [selected, setSelected] = useState(null);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState(null);
  const [companyFilter, setCompanyFilter] = useState("All");
  const [difficultyFilter, setDifficultyFilter] = useState("All");
  const [query, setQuery] = useState("");
  const [solvedMap, setSolvedMap] = useState(
    () => JSON.parse(localStorage.getItem("solvedMap") || "{}")
  );
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProblems();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [problems, companyFilter, difficultyFilter, query, solvedMap]);

  useEffect(() => {
    localStorage.setItem("solvedMap", JSON.stringify(solvedMap));
  }, [solvedMap]);

  async function fetchProblems() {
    try {
      const res = await fetch(API_BASE + "/problems");

      if (!res.ok) {
        console.error("Backend returned error:", res.status);
        return;
      }

      const data = await res.json();

      const order = { Easy: 0, Medium: 1, Hard: 2 };

      data.sort(
        (a, b) =>
          (order[a.difficulty] || 0) -
            (order[b.difficulty] || 0) ||
          a.title.localeCompare(b.title)
      );

      setProblems(data);
      if (data.length) setSelected(data[0]);
    } catch (error) {
      console.error("Fetch failed:", error);
    }
  }

  function applyFilters() {
    let out = [...problems];

    if (companyFilter !== "All")
      out = out.filter((p) => p.companies?.includes(companyFilter));

    if (difficultyFilter !== "All")
      out = out.filter((p) => p.difficulty === difficultyFilter);

    if (query.trim())
      out = out.filter(
        (p) =>
          p.title.toLowerCase().includes(query.toLowerCase()) ||
          p.description.toLowerCase().includes(query.toLowerCase())
      );

    out.sort((a, b) => (solvedMap[a.id] ? 1 : 0) - (solvedMap[b.id] ? 1 : 0));

    setFiltered(out);
  }

  function pickProblem(p) {
    setSelected(p);
    setCode(p.starter_code || `${p.signature}\n    pass`);
    setOutput(null);
  }

  async function runCode() {
    if (!selected) return;

    setLoading(true);
    setOutput(null);

    try {
      const resp = await fetch(API_BASE + "/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ problem_id: selected.id, code }),
      });

      const data = await resp.json();

      setOutput(data);

      if (data.passed) {
        setSolvedMap((prev) => ({ ...prev, [selected.id]: true }));
      }
    } catch (err) {
      setOutput({ error: String(err) });
    }

    setLoading(false);
  }

  const companies = ["All", ...new Set(problems.flatMap((p) => p.companies || []))];
  const difficulties = ["All", "Easy", "Medium", "Hard"];

  return (
    <div className="min-h-screen p-6 bg-auroraBg text-gray-200">
      <div className="max-w-7xl mx-auto grid grid-cols-12 gap-6">

        {/* SIDEBAR */}
        <aside className="col-span-4 card p-4 shadow-xl">
          <h2 className="text-xl font-semibold mb-4 bg-aurora bg-clip-text text-transparent">
            InterviewGPT Problems
          </h2>

          {/* Filters */}
          <div className="flex gap-2 mb-3">
            <select
              className="flex-1 p-2 rounded bg-[#1a1a24] border border-[#2a2a33]"
              value={companyFilter}
              onChange={(e) => setCompanyFilter(e.target.value)}
            >
              {companies.map((c) => (
                <option key={c}>{c}</option>
              ))}
            </select>

            <select
              className="p-2 rounded bg-[#1a1a24] border border-[#2a2a33]"
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
            >
              {difficulties.map((d) => (
                <option key={d}>{d}</option>
              ))}
            </select>
          </div>

          {/* Search */}
          <input
            className="w-full p-2 mb-3 rounded bg-[#1a1a24] border border-[#2a2a33]"
            placeholder="Search problems..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          {/* Problem List */}
          <div className="max-h-[65vh] overflow-y-auto space-y-2">
            {filtered.map((p) => (
              <button
                key={p.id}
                onClick={() => pickProblem(p)}
                className={`w-full p-3 rounded text-left bg-[#1b1b25] hover:bg-[#252533] transition 
                  ${selected?.id === p.id ? "ring-2 ring-aurora1 bg-[#2d2d3a]" : ""}`}
              >
                <div className="font-medium">{p.title}</div>
                <div className="text-xs opacity-75">
                  {p.difficulty} • {p.companies?.join(", ")}
                </div>
              </button>
            ))}
          </div>
        </aside>

        {/* MAIN PANEL */}
        <main className="col-span-8 space-y-4">
          <div className="card p-4">
            {selected ? (
              <>
                <h1 className="text-3xl font-bold bg-aurora bg-clip-text text-transparent">
                  {selected.title}
                </h1>

                <p className="mt-2 text-sm opacity-80">{selected.description}</p>

                <div className="grid grid-cols-2 gap-4 mt-4">

                  {/* Code Editor */}
                  <div>
                    <label className="text-sm font-semibold">Code Editor</label>

                    <textarea
                      value={code}
                      onChange={(e) => setCode(e.target.value)}
                      rows={16}
                      className="w-full mt-2 p-3 rounded bg-[#1b1b25] border border-[#2a2a33] font-mono text-xs"
                    />

                    <div className="flex gap-3 mt-3">
                      <button
                        onClick={runCode}
                        disabled={loading}
                        className="px-4 py-2 rounded bg-aurora hover:opacity-90 text-black font-semibold"
                      >
                        {loading ? "Running..." : "Run Code"}
                      </button>

                      <button
                        onClick={() =>
                          setCode(selected.starter_code || selected.signature)
                        }
                        className="px-4 py-2 rounded bg-[#252533]"
                      >
                        Reset
                      </button>
                    </div>
                  </div>

                  {/* Output */}
                  <div>
                    <label className="text-sm font-semibold">Output</label>
                    <div className="mt-2 p-3 rounded bg-[#1b1b25] border border-[#2a2a33] min-h-[250px] text-sm overflow-auto">
                      {!output && <p className="opacity-50">Run your code to see output...</p>}

                      {output?.error && (
                        <pre className="text-red-400">{output.error}</pre>
                      )}

                      {output?.test_results && (
                        <ul className="space-y-1">
                          {output.test_results.map((t, i) => (
                            <li key={i} className={t.ok ? "text-green-400" : "text-red-400"}>
                              {t.ok
                                ? "Passed"
                                : `Failed — expected ${JSON.stringify(
                                    t.expected
                                  )}, got ${JSON.stringify(t.got)}`}
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>

                </div>
              </>
            ) : (
              <p>Select a problem to start coding.</p>
            )}
          </div>
        </main>

      </div>
    </div>
  );
}
