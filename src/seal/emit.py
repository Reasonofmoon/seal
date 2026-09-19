from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .graph import sealed_facts

def emit_context_md(graph: dict[str, Any], out: Path) -> Path:
    facts = sealed_facts(graph)
    lines = [
        f"# CONTEXT — {graph['product']['id']}",
        "",
        "> Emitted by SEAL effect.emit_context. Facts below are sealed only.",
        "",
        "## Idea",
        graph["product"]["idea"],
        "",
        "## Sealed facts",
    ]
    for k in ("jtbd", "persona", "vision", "constraints", "ethics_bans"):
        if k in facts:
            lines.append(f"### {k}")
            v = facts[k]
            if isinstance(v, list):
                lines.extend([f"- {i}" for i in v])
            elif isinstance(v, dict):
                for kk, vv in v.items():
                    lines.append(f"- **{kk}**: {vv}")
            else:
                lines.append(str(v))
            lines.append("")
    # also dump rubric assertions if present
    for k, v in facts.items():
        if str(k).startswith("gap.af.rubric.") or k in ("jtbd", "persona", "vision", "constraints", "ethics_bans"):
            continue
        if str(k).startswith("gap."):
            continue
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def emit_aplus_passport(graph, out: Path) -> Path:
    """Replaces AF overall.aplus_threshold_passed — seals only."""
    sealed = [gid for gid, g in graph["gaps"].items() if g.get("status") == "sealed"]
    lines = [
        f"# A+ Passport — {graph['product']['id']}",
        "",
        "> SEAL conquest of App Factory `audit-spec`. This file is emitted only when every rubric Gap is sealed.",
        "",
        f"- pack: `{graph['product'].get('pack')}`",
        f"- seals: {len(graph.get('seals', {}))}",
        f"- open_gaps: {len([1 for g in graph['gaps'].values() if g.get('status')=='open'])}",
        "",
        "## Sealed rubric gaps",
    ]
    for gid in sealed:
        if gid.startswith("gap.af.rubric.") or "spec.corpus" in gid:
            lines.append(f"- {gid}")
    lines.append("")
    lines.append("## Legacy mapping")
    lines.append("- `has_blocking_spec_gaps` -> any unsealed rubric gap OR failed strike")
    lines.append("- `aplus_threshold_passed` -> this passport exists")
    lines.append("")
    lines.append("## Next effects (S5)")
    lines.append("1. `effect.emit_context` (requires this passport done)")
    lines.append("2. `effect.codegen_vertical_slice` (requires passport + context done)")
    lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def emit_codegen_stub(graph: dict, out_dir: Path) -> Path:
    """Post-passport scaffold. Replaces app-factory implement/apply as the unlock gate.

    Does not call a generative coding model. Coding agents fill the stub after unlock.
    """
    facts = sealed_facts(graph)
    public_facts = {k: v for k, v in facts.items() if not str(k).startswith("gap.")}
    out_dir.mkdir(parents=True, exist_ok=True)
    app = out_dir / ".seal_app"
    app.mkdir(parents=True, exist_ok=True)

    readme = [
        f"# {graph['product']['id']} — SEAL codegen unlock",
        "",
        "> Emitted by `effect.codegen_vertical_slice` AFTER A+ passport + CONTEXT.",
        "> Replaces `app-factory implement` / `apply-implementation` as the unlock gate.",
        "> This stub is not production code.",
        "",
        "## Idea",
        graph["product"]["idea"],
        "",
        "## Sealed inputs (do not invent past these)",
        "```json",
        json.dumps(public_facts, ensure_ascii=False, indent=2),
        "```",
        "",
        "## First vertical slice",
        "1. One screen that serves the sealed JTBD/persona when present.",
        "2. Honor sealed ethics bans.",
        "3. Respect sealed constraints.",
        "",
    ]
    (app / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    pid = graph["product"]["id"]
    tsx = (
        "/* SEAL stub — post-passport only */\n"
        "export default function App() {\n"
        "  return (\n"
        "    <main>\n"
        f"      <h1>{pid}</h1>\n"
        "      <p>Implement from sealed CONTEXT / passport. No seal, no advance.</p>\n"
        "    </main>\n"
        "  );\n"
        "}\n"
    )
    (app / "App.tsx").write_text(tsx, encoding="utf-8")
    (app / "seal.meta.json").write_text(
        json.dumps(
            {
                "product": pid,
                "pack": graph["product"].get("pack"),
                "seals": len(graph.get("seals", {})),
                "replaces": [
                    "app-factory implement",
                    "app-factory apply-implementation",
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return app
