from __future__ import annotations
import argparse, json, sys
from pathlib import Path

# allow running without install
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seal.graph import open_product, save, load, add_candidate, project, compile_questions, try_seal, status, refresh_effects
from seal.vein import suggest_next, snapshot
from seal.ukdl_subset import dump as ukdl_dump, parse as ukdl_parse, validate_text, UkdlSubsetError
from seal.board import write_board, board_model
from seal.mint_heuristic import mint
from seal.emit import emit_context_md, emit_aplus_passport, emit_codegen_stub

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="seal", description="SEAL — no seal, no advance")
    sub = p.add_subparsers(dest="cmd", required=True)

    o = sub.add_parser("open", help="Open a gap pack for a product idea")
    o.add_argument("--id", required=True)
    o.add_argument("--idea", required=True)
    o.add_argument("--pack", default="edtech.foundation")
    o.add_argument("--out", type=Path, required=True)

    s = sub.add_parser("status", help="Show open/blocked/sealed gaps")
    s.add_argument("--graph", type=Path, required=True)

    c = sub.add_parser("fill", help="Add a candidate for a gap")
    c.add_argument("--graph", type=Path, required=True)
    c.add_argument("--gap", required=True)
    c.add_argument("--by", default="human")
    c.add_argument("--json", help="JSON value")
    c.add_argument("--text", help="String value")
    c.add_argument("--file", type=Path, help="Read JSON or text file")

    st = sub.add_parser("strike", help="Project+compile+mint+try seal a candidate")
    st.add_argument("--graph", type=Path, required=True)
    st.add_argument("--gap", required=True)
    st.add_argument("--candidate", required=True)
    st.add_argument("--provider", default="heuristic")

    e = sub.add_parser("effect", help="Run a ready effect")
    e.add_argument("--graph", type=Path, required=True)
    e.add_argument("--id", required=True)
    e.add_argument("--out-dir", type=Path, required=True)

    n = sub.add_parser("next", help="Vein-ranked next open gaps (sealed transitions only)")
    n.add_argument("--graph", type=Path, required=True)
    n.add_argument("--limit", type=int, default=5)

    v = sub.add_parser("vein", help="Show Vein edge weights")
    v.add_argument("--graph", type=Path, required=True)

    d = sub.add_parser("dump", help="Dump Seal Graph as SEAL UKDL subset (.seal.ukdl)")
    d.add_argument("--graph", type=Path, required=True)
    d.add_argument("--out", type=Path, help="Write file; default stdout")

    ld = sub.add_parser("load-ukdl", help="Parse SEAL UKDL subset (rejects L3–L5 kinds)")
    ld.add_argument("--file", type=Path, required=True)
    ld.add_argument("--out", type=Path, help="Write partial graph JSON")
    ld.add_argument("--validate-only", action="store_true")

    b = sub.add_parser("board", help="Render Gap Board HTML (destroys AF Studio parade)")
    b.add_argument("--graph", type=Path, required=True)
    b.add_argument("--out", type=Path, required=True)
    b.add_argument("--no-ukdl", action="store_true")

    bj = sub.add_parser("board-json", help="Gap Board model as JSON")
    bj.add_argument("--graph", type=Path, required=True)

    args = p.parse_args(argv)

    if args.cmd == "open":
        g = open_product(args.id, args.idea, args.pack)
        save(g, args.out)
        print(json.dumps(status(g), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "load-ukdl":
        text = args.file.read_text(encoding="utf-8")
        if args.validate_only:
            print(json.dumps(validate_text(text), ensure_ascii=False, indent=2))
            return 0 if validate_text(text)["ok"] else 2
        try:
            partial = ukdl_parse(text)
        except UkdlSubsetError as e:
            print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        if args.out:
            args.out.write_text(json.dumps(partial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"ok": True, "path": str(args.out), "gaps": len(partial.get("gaps", {})), "seals": len(partial.get("seals", {}))}, indent=2))
        else:
            print(json.dumps(partial, ensure_ascii=False, indent=2))
        return 0

    g = load(args.graph)

    if args.cmd == "status":
        print(json.dumps(status(g), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "fill":
        if args.json:
            value = json.loads(args.json)
        elif args.file:
            raw = args.file.read_text(encoding="utf-8")
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                value = raw.strip()
        elif args.text:
            value = args.text
        else:
            print("need --text, --json, or --file", file=sys.stderr)
            return 2
        cid = add_candidate(g, args.gap, value, by=args.by)
        save(g, args.graph)
        print(cid)
        return 0

    if args.cmd == "strike":
        state = project(g, args.gap, args.candidate)
        questions = compile_questions(g["gaps"][args.gap])
        if args.provider.startswith("heuristic"):
            answers = mint(state, questions)
            provider = "heuristic:v0"
        elif args.provider.startswith("typesafe"):
            import os
            import subprocess
            mint_js = Path(__file__).resolve().parent / "mint_typesafe.mjs"
            payload = json.dumps({"state": state, "questions": questions}, ensure_ascii=False)
            env = dict(os.environ)
            node_path = env.get("NODE_PATH") or env.get("TYPESAFE_NODE_PATH")
            if node_path:
                env["NODE_PATH"] = node_path
            cwd = env.get("TYPESAFE_CWD") or str(Path.cwd())
            proc = subprocess.run(
                ["node", str(mint_js)],
                input=payload.encode("utf-8"),
                capture_output=True,
                cwd=cwd,
                env=env,
            )
            if proc.returncode != 0:
                print(proc.stderr.decode() or proc.stdout.decode(), file=sys.stderr)
                return 3
            out = json.loads(proc.stdout.decode("utf-8"))
            answers = out["answers"]
            provider = out.get("provider", "typesafe:jev-latest")
        else:
            print("unsupported provider", file=sys.stderr)
            return 2
        result = try_seal(g, args.gap, args.candidate, answers, provider=provider)
        save(g, args.graph)
        print(json.dumps({"answers": answers, "result": result, "status": status(g)}, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 1

    if args.cmd == "effect":
        refresh_effects(g)
        if args.id not in g["effects"]:
            print(json.dumps({"ok": False, "error": "unknown_effect", "id": args.id}, ensure_ascii=False))
            return 2
        eff = g["effects"][args.id]
        if eff["status"] != "ready":
            print(json.dumps({
                "ok": False,
                "status": eff["status"],
                "need_gaps": eff.get("after") or [],
                "need_effects": eff.get("after_effects") or [],
            }, ensure_ascii=False, indent=2))
            return 1
        args.out_dir.mkdir(parents=True, exist_ok=True)
        if eff["run"] == "emit_context_md":
            path = emit_context_md(g, args.out_dir / "CONTEXT.md")
        elif eff["run"] == "emit_aplus_passport":
            path = emit_aplus_passport(g, args.out_dir / "APLUS_PASSPORT.md")
        elif eff["run"] == "emit_codegen_stub":
            path = emit_codegen_stub(g, args.out_dir)
        else:
            print("unknown effect run", eff["run"], file=sys.stderr)
            return 2
        eff["status"] = "done"
        refresh_effects(g)
        g["journal"].append({"op": "effect", "id": args.id, "path": str(path)})
        save(g, args.graph)
        print(json.dumps({
            "ok": True,
            "path": str(path),
            "effects": {k: v["status"] for k, v in g["effects"].items()},
        }, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "next":
        print(json.dumps({"next": suggest_next(g, limit=args.limit)}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "vein":
        print(json.dumps(snapshot(g), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "dump":
        text = ukdl_dump(g)
        if args.out:
            args.out.write_text(text, encoding="utf-8")
            print(json.dumps({"ok": True, "path": str(args.out), "bytes": len(text.encode())}, indent=2))
        else:
            print(text, end="")
        return 0

    if args.cmd == "board":
        path = write_board(g, args.out, embed_ukdl=not args.no_ukdl)
        print(json.dumps({"ok": True, "path": str(path), "model": board_model(g)["counts"]}, indent=2))
        return 0

    if args.cmd == "board-json":
        print(json.dumps(board_model(g), ensure_ascii=False, indent=2))
        return 0

    return 2

if __name__ == "__main__":
    raise SystemExit(main())
