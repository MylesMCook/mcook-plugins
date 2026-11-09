// The installer supplies TypeScript from the app, avoiding another parser dependency.
function parsed(source, ts, kind) {
  const file = ts.createSourceFile('input.tsx', source, ts.ScriptTarget.Latest, true, kind);
  if (file.parseDiagnostics.length) throw new Error('Fix existing TypeScript syntax errors before setup.');
  return file;
}

function edits(source, changes) {
  return changes.sort((a, b) => b.at - a.at).reduce((text, { at, value }) => text.slice(0, at) + value + text.slice(at), source);
}

function importAt(file, ts) {
  const imports = file.statements.filter(ts.isImportDeclaration);
  return imports.length ? imports.at(-1).end : 0;
}

function newline(file) { return file.text.includes('\r\n') ? '\r\n' : '\n'; }

function addImport(file, ts, name, importPath) {
  if (!/^\.?\.?\/[A-Za-z0-9_./-]+$/.test(importPath)) throw new Error('Feedback import must be a relative module path.');
  const at = importAt(file, ts);
  return { at, value: `${at ? newline(file) : ''}import { ${name} } from ${JSON.stringify(importPath)};${at ? '' : newline(file)}` };
}

export function wireVite(source, ts, importPath, startupEntries) {
  if (/\bwithNativeFeedback\b/.test(source)) throw new Error('Vite feedback wiring already exists; use the setup receipt to rerun.');
  const file = parsed(source, ts, ts.ScriptKind.TS);
  const defaults = file.statements.filter((node) => ts.isExportAssignment(node) && !node.isExportEquals);
  if (defaults.length !== 1) throw new Error('Expected exactly one default Vite configuration export.');
  const expression = defaults[0].expression;
  return edits(source, [addImport(file, ts, 'withNativeFeedback', importPath), { at: expression.getStart(file), value: 'withNativeFeedback(' }, { at: expression.end, value: (startupEntries ? ', '+JSON.stringify(startupEntries) : '')+')' }]);
}

export function wireReact(source, ts, importPath) {
  if (/\bNativeFeedback\b/.test(source)) throw new Error('React feedback wiring already exists; use the setup receipt to rerun.');
  const file = parsed(source, ts, ts.ScriptKind.TSX);
  const apps = [];
  function visit(node) {
    if ((ts.isJsxSelfClosingElement(node) || ts.isJsxElement(node)) && (ts.isJsxSelfClosingElement(node) ? node.tagName : node.openingElement.tagName).getText(file) === 'App') apps.push(node);
    ts.forEachChild(node, visit);
  }
  visit(file);
  if (apps.length !== 1) throw new Error('Expected exactly one <App> root. Select the React entry explicitly for this layout.');
  const app = apps[0];
  // Only wire the root rendered by React; a similarly named nested component is ambiguous.
  let ancestor = app.parent;
  while (ancestor && !(ts.isCallExpression(ancestor) && ts.isPropertyAccessExpression(ancestor.expression) && ancestor.expression.name.text === 'render')) ancestor = ancestor.parent;
  if (!ancestor) throw new Error('The <App> root must be inside a React root.render call.');
  const start = app.getStart(file);
  const line = source.slice(source.lastIndexOf('\n', start - 1) + 1, start);
  const indent = /^\s*$/.test(line) ? line : '';
  if (ts.isJsxElement(app.parent) || ts.isJsxFragment(app.parent)) {
    return edits(source, [addImport(file, ts, 'NativeFeedback', importPath), { at: app.end, value: `${newline(file)}${indent}<NativeFeedback />` }]);
  }
  // An app directly passed as render's argument needs a fragment for its new sibling.
  if (ancestor.arguments.length !== 1 || ancestor.arguments[0] !== app) throw new Error('The <App> root has an unsupported wrapper; preserve it by choosing a supported entry.');
  return edits(source, [addImport(file, ts, 'NativeFeedback', importPath), { at: start, value: '<>' }, { at: app.end, value: '<NativeFeedback /></>' }]);
}
