"""SEAL UKDL subset — serialization only (S7).

Allowed kinds: meta | gap | candidate | seal | effect | entity | rel
Banned (L3–L5 / executable fantasy): action | pipeline | quantum
Also rejected in this subset: block | schema | include | context | function
(those remain UKDL-full-spec; SEAL does not execute documents.)

Canonical form mirrors UKDL node fences:
  :: kind id=<id> [attrs]
  @field: value
  ::
"""
from __future__ import annotations
import json
import re
from typing import Any

ALLOWED = frozenset({"meta", "gap", "candidate", "seal", "effect", "entity", "rel"})
BANNED = frozenset({
    "action", "pipeline", "quantum",  # L3–L5
    "block", "schema", "include", "context", "function",  # not SEAL kernel surface
})

_OPEN = re.compile(
    r"^::\s*(?P<kind>[A-Za-z_][\w-]*)\s+id=(?P<id>[^\s]+)(?P<rest>.*?)\s*$"
)
_FIELD = re.compile(r"^@(?P<key>[A-Za-z_][\w.-]*):\s*(?P<val>.*)$")
_CLOSE = re.compile(r"^::\s*$")


class UkdlSubsetError(ValueError):
    pass


def _fmt_val(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        if "\n" in v or '"' in v:
            return '"""\n' + v.replace('"""', '\\"""') + '\n"""'
        return json.dumps(v, ensure_ascii=False)
    return json.dumps(v, ensure_ascii=False)


def _parse_val(raw: str) -> Any:
    s = raw.strip()
    if s == "null":
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    if s.startswith('"""'):
        # caller joins multiline
        return s
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # bare @ref
        if s.startswith("@"):
            return s
        return s.strip("'") if (s.startswith("'") and s.endswith("'")) else s


def dump(graph: dict[str, Any]) -> str:
    """Serialize Seal Graph to SEAL UKDL subset text."""
    lines: list[str] = [
        "%% SEAL UKDL subset — not executable UKDL L3–L5",
        "%% Allowed: meta gap candidate seal effect entity rel",
        "%% Banned: action pipeline quantum (and block/schema/include/context)",
        "",
    ]
    p = graph.get("product") or {}
    lines.append(f":: meta id=meta:product-{p.get('id', 'unknown')}")
    lines.append(f"@seal_version: {_fmt_val(graph.get('seal_version', '0.1.0'))}")
    lines.append(f"@product: {_fmt_val(p.get('id'))}")
    lines.append(f"@idea: {_fmt_val(p.get('idea'))}")
    lines.append(f"@pack: {_fmt_val(p.get('pack'))}")
    lines.append(f"@pack_version: {_fmt_val(p.get('pack_version'))}")
    lines.append(f"@lang: {_fmt_val(p.get('lang', 'ko'))}")
    if p.get("created_at"):
        lines.append(f"@created_at: {_fmt_val(p['created_at'])}")
    lines.append("@ukdl_level: 1")
    lines.append("@seal_dialect: \"seal-ukdl-0.1\"")
    lines.append("::")
    lines.append("")

    for gid, gap in (graph.get("gaps") or {}).items():
        risk = gap.get("risk") or "read"
        lines.append(f":: gap id={gid} risk={risk}")
        lines.append(f"@ask: {_fmt_val(gap.get('ask', ''))}")
        lines.append(f"@status: {_fmt_val(gap.get('status', 'open'))}")
        if gap.get("requires"):
            lines.append(f"@requires: {_fmt_val(gap['requires'])}")
        if gap.get("sealed_by"):
            lines.append(f"@sealed_by: {_fmt_val(gap['sealed_by'])}")
        lines.append("::")
        lines.append("")
        for req in gap.get("requires") or []:
            rid = f"rel:requires-{gid.replace('.', '-')}-from-{req.replace('.', '-')}"
            lines.append(f":: rel id={rid} type=requires from=@{req} to=@{gid}")
            lines.append("@summary: \"seal prerequisite\"")
            lines.append("::")
            lines.append("")

    for cid, cand in (graph.get("candidates") or {}).items():
        gap_ref = cand.get("gap") or cand.get("gap_id")
        lines.append(f":: candidate id={cid} gap=@{gap_ref}")
        lines.append(f"@value: {_fmt_val(cand.get('value'))}")
        lines.append(f"@by: {_fmt_val(cand.get('by', 'human'))}")
        if cand.get("model"):
            lines.append(f"@model: {_fmt_val(cand['model'])}")
        lines.append("::")
        lines.append("")

    for sid, seal in (graph.get("seals") or {}).items():
        gap_ref = seal.get("gap")
        lines.append(f":: seal id={sid} gap=@{gap_ref}")
        if seal.get("candidate"):
            lines.append(f"@candidate: @{seal['candidate']}")
        if seal.get("provider"):
            lines.append(f"@provider: {_fmt_val(seal['provider'])}")
        if seal.get("at"):
            lines.append(f"@at: {_fmt_val(seal['at'])}")
        if seal.get("strike_id"):
            lines.append(f"@strike_id: {_fmt_val(seal['strike_id'])}")
        elif seal.get("strike"):
            lines.append(f"@strike_id: {_fmt_val(seal['strike'])}")
        lines.append("::")
        lines.append("")

    for eid, eff in (graph.get("effects") or {}).items():
        lines.append(f":: effect id={eid}")
        lines.append(f"@status: {_fmt_val(eff.get('status', 'locked'))}")
        if eff.get("after") is not None:
            lines.append(f"@after: {_fmt_val(eff['after'])}")
        if eff.get("after_effects") is not None:
            lines.append(f"@after_effects: {_fmt_val(eff['after_effects'])}")
        if eff.get("run"):
            lines.append(f"@run: {_fmt_val(eff['run'])}")
        if eff.get("risk"):
            lines.append(f"@risk: {_fmt_val(eff['risk'])}")
        lines.append("::")
        lines.append("")

    # Vein as entity annotations (not a kernel kind — attach under meta-adjacent entity)
    vein = graph.get("vein") or {}
    if vein:
        lines.append(":: entity id=ent:vein type=SealVein")
        lines.append(f"@edges: {_fmt_val(vein)}")
        lines.append("@summary: \"weights from sealed transitions only\"")
        lines.append("::")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse(text: str) -> dict[str, Any]:
    """Parse SEAL UKDL subset into a partial Seal Graph dict.

    Does not re-hydrate pack schemas; merges onto open_product separately if needed.
    """
    nodes = _parse_nodes(text)
    banned_hit = [n for n in nodes if n["kind"] in BANNED]
    if banned_hit:
        kinds = sorted({n["kind"] for n in banned_hit})
        raise UkdlSubsetError(
            f"banned UKDL kinds in SEAL subset (L3–L5 / non-kernel): {kinds}. "
            "Use Gaps+Effects instead of action/pipeline/quantum."
        )
    unknown = [n for n in nodes if n["kind"] not in ALLOWED]
    if unknown:
        kinds = sorted({n["kind"] for n in unknown})
        raise UkdlSubsetError(f"unknown kinds for SEAL subset: {kinds}")

    graph: dict[str, Any] = {
        "seal_version": "0.1.0",
        "product": {},
        "gaps": {},
        "candidates": {},
        "seals": {},
        "effects": {},
        "vein": {},
        "journal": [{"op": "ukdl_parse", "nodes": len(nodes)}],
    }

    for n in nodes:
        kind, nid, fields, attrs = n["kind"], n["id"], n["fields"], n["attrs"]
        if kind == "meta":
            graph["seal_version"] = fields.get("seal_version", graph["seal_version"])
            graph["product"] = {
                "id": fields.get("product") or nid.replace("meta:product-", ""),
                "idea": fields.get("idea", ""),
                "pack": fields.get("pack", ""),
                "pack_version": fields.get("pack_version"),
                "lang": fields.get("lang", "ko"),
                "created_at": fields.get("created_at"),
            }
        elif kind == "gap":
            graph["gaps"][nid] = {
                "id": nid,
                "ask": fields.get("ask", ""),
                "risk": attrs.get("risk") or fields.get("risk") or "read",
                "status": fields.get("status", "open"),
                "requires": fields.get("requires") or [],
                "sealed_by": fields.get("sealed_by"),
            }
        elif kind == "candidate":
            gap = attrs.get("gap") or fields.get("gap")
            if isinstance(gap, str) and gap.startswith("@"):
                gap = gap[1:]
            graph["candidates"][nid] = {
                "id": nid,
                "gap": gap,
                "value": fields.get("value"),
                "by": fields.get("by", "human"),
                "model": fields.get("model"),
            }
        elif kind == "seal":
            gap = attrs.get("gap") or fields.get("gap")
            if isinstance(gap, str) and gap.startswith("@"):
                gap = gap[1:]
            cand = fields.get("candidate")
            if isinstance(cand, str) and cand.startswith("@"):
                cand = cand[1:]
            graph["seals"][nid] = {
                "id": nid,
                "gap": gap,
                "candidate": cand,
                "provider": fields.get("provider"),
                "at": fields.get("at"),
                "strike_id": fields.get("strike_id") or fields.get("strike"),
            }
        elif kind == "effect":
            graph["effects"][nid] = {
                "id": nid,
                "status": fields.get("status", "locked"),
                "after": fields.get("after"),
                "after_effects": fields.get("after_effects"),
                "run": fields.get("run"),
                "risk": fields.get("risk"),
            }
        elif kind == "entity" and nid == "ent:vein":
            edges = fields.get("edges") or {}
            if isinstance(edges, dict):
                graph["vein"] = edges
        elif kind == "rel":
            # informational; requires already on gaps
            pass
        elif kind == "entity":
            pass

    return graph


def _parse_nodes(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    nodes: list[dict[str, Any]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("%%"):
            i += 1
            continue
        m = _OPEN.match(stripped)
        if not m:
            i += 1
            continue
        kind = m.group("kind")
        nid = m.group("id")
        rest = m.group("rest") or ""
        attrs = _parse_attrs(rest)
        fields: dict[str, Any] = {}
        i += 1
        while i < len(lines):
            s = lines[i].strip()
            if _CLOSE.match(s):
                i += 1
                break
            fm = _FIELD.match(s)
            if fm:
                key = fm.group("key")
                val_raw = fm.group("val").strip()
                if val_raw.startswith('"""'):
                    # multiline
                    if val_raw == '"""' or not val_raw.endswith('"""') or val_raw.count('"""') == 1:
                        buf = []
                        if val_raw.startswith('"""') and len(val_raw) > 3 and val_raw.endswith('"""'):
                            fields[key] = val_raw[3:-3]
                        else:
                            if val_raw != '"""':
                                buf.append(val_raw[3:])
                            i += 1
                            while i < len(lines):
                                if lines[i].strip() == '"""':
                                    break
                                buf.append(lines[i])
                                i += 1
                            fields[key] = "\n".join(buf)
                    else:
                        fields[key] = val_raw[3:-3]
                else:
                    fields[key] = _parse_val(val_raw)
            i += 1
        nodes.append({"kind": kind, "id": nid, "attrs": attrs, "fields": fields})
    return nodes


def _parse_attrs(rest: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for part in rest.split():
        if "=" in part:
            k, v = part.split("=", 1)
            attrs[k] = v
    return attrs


def validate_text(text: str) -> dict[str, Any]:
    """Return {ok, kinds, banned, errors} without raising."""
    try:
        nodes = _parse_nodes(text)
    except Exception as e:
        return {"ok": False, "errors": [str(e)], "kinds": [], "banned": []}
    kinds = [n["kind"] for n in nodes]
    banned = sorted({k for k in kinds if k in BANNED})
    unknown = sorted({k for k in kinds if k not in ALLOWED and k not in BANNED})
    errors = []
    if banned:
        errors.append(f"banned: {banned}")
    if unknown:
        errors.append(f"unknown: {unknown}")
    return {
        "ok": not errors,
        "kinds": kinds,
        "banned": banned,
        "unknown": unknown,
        "errors": errors,
        "node_count": len(nodes),
        "destroys": "ukdl L3–L5 action/pipeline/quantum as executors",
    }
