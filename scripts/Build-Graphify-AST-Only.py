"""
Build a code-only Graphify knowledge graph on Apex using ONLY deterministic Python.
Zero LLM tokens. Mimics SKILL.md Steps 1, 2, 3-Part-A, 3-Part-C, 4 — skips
Part B (semantic, the token hog) and Step 5+ (LLM labeling, optional).

Output: graphify-out/graph.json + graphify-out/GRAPH_REPORT.md

Usage:
  python Build-Graphify-AST-Only.py <apex-path>
"""
import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("usage: python Build-Graphify-AST-Only.py <apex-path>")
    sys.exit(1)

apex = Path(sys.argv[1]).resolve()
if not apex.is_dir():
    print(f"ERROR: not a directory: {apex}")
    sys.exit(1)

out = apex / "graphify-out"
out.mkdir(exist_ok=True)

# Persist scan root + python path so future `graphify update` re-uses it
(out / ".graphify_python").write_text(sys.executable)
(out / ".graphify_root").write_text(str(apex))

# Step 2 — detect
from graphify.detect import detect
print(f"Detecting files under {apex}...")
detection = detect(apex)
(out / ".graphify_detect.json").write_text(json.dumps(detection))
totals = detection.get("total_files", 0)
by_type = {k: len(v) for k, v in detection.get("files", {}).items() if v}
print(f"  total_files={totals}  by_type={by_type}  total_words={detection.get('total_words', 0):,}")

# Step 3 Part A — AST structural extraction
from graphify.extract import collect_files, extract
code_files = []
for f in detection.get("files", {}).get("code", []):
    p = Path(f)
    code_files.extend(collect_files(p) if p.is_dir() else [p])
print(f"Running AST extract on {len(code_files)} code files...")
if code_files:
    ast = extract(code_files, cache_root=apex)
else:
    ast = {"nodes": [], "edges": [], "input_tokens": 0, "output_tokens": 0}
(out / ".graphify_ast.json").write_text(json.dumps(ast, indent=2))
print(f"  AST: {len(ast['nodes'])} nodes, {len(ast['edges'])} edges")

# Step 3 Part B — SKIPPED (empty semantic, zero LLM)
empty_semantic = {"nodes": [], "edges": [], "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
(out / ".graphify_semantic.json").write_text(json.dumps(empty_semantic, indent=2))
print("  Semantic: SKIPPED (AST-only build, zero LLM cost)")

# Step 3 Part C — Merge AST + semantic (semantic is empty)
seen = {n["id"] for n in ast["nodes"]}
merged_nodes = list(ast["nodes"])
merged_edges = ast["edges"]
merged_extract = {
    "nodes": merged_nodes,
    "edges": merged_edges,
    "hyperedges": [],
    "input_tokens": 0,
    "output_tokens": 0,
}
(out / ".graphify_extract.json").write_text(json.dumps(merged_extract, indent=2))
print(f"  Extract merged: {len(merged_nodes)} nodes, {len(merged_edges)} edges")

# Step 4 — build graph, cluster, analyze, generate outputs
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json

G = build_from_json(merged_extract)
if G.number_of_nodes() == 0:
    print("ERROR: graph empty — AST extraction produced zero nodes. Check Apex code-file detection.")
    sys.exit(2)
print(f"Built graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

communities = cluster(G)
cohesion = score_all(G, communities)
tokens = {"input": 0, "output": 0}
gods = god_nodes(G)
surprises = surprising_connections(G, communities)
labels = {cid: f"Community {cid}" for cid in communities}
questions = suggest_questions(G, communities, labels)

report = generate(
    G, communities, cohesion, labels, gods, surprises,
    detection, tokens, str(apex),
    suggested_questions=questions,
)
(out / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
to_json(G, communities, str(out / "graph.json"))

analysis = {
    "communities": {str(k): v for k, v in communities.items()},
    "cohesion": {str(k): v for k, v in cohesion.items()},
    "gods": gods,
    "surprises": surprises,
    "questions": questions,
}
(out / ".graphify_analysis.json").write_text(json.dumps(analysis, indent=2), encoding="utf-8")

print()
print(f"DONE — graph.json @ {out / 'graph.json'}")
print(f"       GRAPH_REPORT.md @ {out / 'GRAPH_REPORT.md'}")
print(f"       {G.number_of_nodes()} nodes · {G.number_of_edges()} edges · {len(communities)} communities")
print(f"       AST-only build — zero LLM tokens spent")
