// Dependency-free check that a topic uses only fields topic.schema.json declares (catches typos and
// schema drift). Follows $ref, properties, additionalProperties, items, prefixItems and enum; full
// type checking stays with an editor's JSON Schema support and build.mjs --check.
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

export const SCHEMA = JSON.parse(readFileSync(join(dirname(fileURLToPath(import.meta.url)), "topic.schema.json"), "utf8"));
const deref = (s) => (s && s.$ref ? deref(s.$ref.slice(2).split("/").reduce((o, k) => o[k], SCHEMA)) : s);

export function unknownFields(value, schema = SCHEMA, path = "topic") {
  const s = deref(schema), out = [];
  if (!s || value === null || typeof value !== "object") {
    if (s && s.enum && !s.enum.includes(value)) out.push(`${path}: "${value}" is not one of ${s.enum.join(", ")}`);
    return out;
  }
  if (Array.isArray(value)) {
    value.forEach((v, i) => out.push(...unknownFields(v, (s.prefixItems && s.prefixItems[i]) || s.items, `${path}[${i}]`)));
    return out;
  }
  for (const [k, v] of Object.entries(value)) {
    const sub = (s.properties || {})[k];
    if (sub) out.push(...unknownFields(v, sub, `${path}.${k}`));
    else if (s.additionalProperties === false) out.push(`${path}.${k}: not a known field`);
    else if (typeof s.additionalProperties === "object") out.push(...unknownFields(v, s.additionalProperties, `${path}.${k}`));
  }
  return out;
}
