#!/usr/bin/env node
/** SEAL TypeSafe mint: stdin {state, questions, model?} → stdout {provider, answers} */
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const require = createRequire(
  process.env.TYPESAFE_SDK_REQUIRE_FROM || join(process.cwd(), "package.json")
);

function ensureKey() {
  if (process.env.TYPESAFE_API_KEY) return;
  throw new Error(
    "TYPESAFE_API_KEY missing. Export it before striking user_trust / irreversible gaps."
  );
}

function flattenDesc(v) {
  if (v == null) return "";
  if (typeof v === "string") return v;
  if (typeof v === "object") {
    if (v.what) {
      const bits = [v.what];
      if (v.not_for) bits.push(`Not for: ${v.not_for}`);
      if (Array.isArray(v.examples)) bits.push(`Examples: ${v.examples.join("; ")}`);
      if (Array.isArray(v.signals)) bits.push(`Signals: ${v.signals.join("; ")}`);
      return bits.join(" | ");
    }
    return JSON.stringify(v);
  }
  return String(v);
}

function normalizeCriteria(type, criteria) {
  if (criteria == null) return undefined;
  if (type === "choice") {
    const out = {};
    for (const [k, v] of Object.entries(criteria)) out[k] = flattenDesc(v);
    return out;
  }
  if (type === "score") {
    return (Array.isArray(criteria) ? criteria : []).map(flattenDesc);
  }
  if (type === "noul") {
    if (typeof criteria !== "object") return criteria;
    return {
      true: flattenDesc(criteria.true ?? criteria.yes),
      false: flattenDesc(criteria.false ?? criteria.no),
    };
  }
  return criteria;
}

const { TypeSafeClient, noul, choice, score } = require("@typesafe-ai/sdk");

const chunks = [];
for await (const c of process.stdin) chunks.push(c);
const input = JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
if (!input.state || !input.questions) throw new Error("need state and questions");

ensureKey();

const questions = {};
for (const [id, q] of Object.entries(input.questions)) {
  const instructions = q.instructions;
  const criteria = normalizeCriteria(q.type, q.criteria);
  if (q.type === "noul") {
    questions[id] = criteria ? noul(instructions, criteria) : noul(instructions);
  } else if (q.type === "choice") {
    questions[id] = choice(instructions, criteria);
  } else if (q.type === "score") {
    questions[id] = score(instructions, criteria);
  } else {
    throw new Error(`unknown type ${q.type}`);
  }
}

const client = new TypeSafeClient();
const response = await client.systemOne({
  model: input.model || "jev-latest",
  state: input.state,
  questions,
});

const answers = {};
for (const [id, a] of Object.entries(response.answers)) {
  if (typeof a.noul === "number") answers[id] = { noul: a.noul };
  else if (a.choice != null)
    answers[id] = { choice: a.choice, confidence: a.confidence, probabilities: a.probabilities };
  else if (a.score != null)
    answers[id] = {
      score: a.score,
      confidence: a.confidence,
      probabilities: a.probabilities,
      legend: a.legend,
    };
  else answers[id] = a;
}

process.stdout.write(
  JSON.stringify({ provider: `typesafe:${response.model || "jev-latest"}`, answers }) + "\n"
);
