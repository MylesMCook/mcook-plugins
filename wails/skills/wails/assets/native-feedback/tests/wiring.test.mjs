import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { wireVite, wireReact } from '../scripts/wire-ts.mjs';
const require = createRequire(process.env.WAILS_FEEDBACK_TEST_APP + '/package.json');
const ts = require('typescript');
const fixture = (name) => readFileSync(new URL(`fixtures/${name}`, import.meta.url), 'utf8');

test('Vite wrapper preserves Burf configuration and plugin ordering', () => {
  for(const eol of ['\n','\r\n']) {
  const source = fixture('burf-vite.ts').replaceAll('\r\n','\n').replaceAll('\n',eol);
  const output = wireVite(source, ts, './src/native-feedback/vite');
  assert.equal(output.replace('import { withNativeFeedback } from "./src/native-feedback/vite";'+eol, '').replace('withNativeFeedback(defineConfig(', 'defineConfig(').replace(/\)\);\s*$/, ');'+eol), source);
  assert.throws(() => wireVite(output, ts, './src/native-feedback/vite'), /already/);
  }
});

test('React insertion keeps asynchronous restore and root boundary', () => {
  for(const eol of ['\n','\r\n']) {
  const source = fixture('burf-main.tsx').replaceAll('\r\n','\n').replaceAll('\n',eol);
  const output = wireReact(source, ts, './native-feedback/NativeFeedback');
  assert.equal(output.replace('import { NativeFeedback } from "./native-feedback/NativeFeedback";'+eol, '').replace(eol+'        <NativeFeedback />', ''), source);
  }
  const simple = 'import App from "./App";\ncreateRoot(document.getElementById("root")).render(<App />);\n';
  assert.match(wireReact(simple, ts, './feedback'), /render\(<>\s*<App \/>\s*<NativeFeedback \/>\s*<\/?>\)/);
  assert.throws(() => wireReact('<App />; <App />;', ts, './feedback'), /exactly one/);
});

function wireGo(source) {
  const run = spawnSync('go', ['run', fileURLToPath(new URL('../scripts/wire-go.go', import.meta.url)), '--module', 'example.test/app/native'], { cwd: import.meta.dirname, input: source, encoding: 'utf8' });
  assert.equal(run.status, 0, run.stderr);
  return run.stdout;
}

test('Go insertion preserves asset/security and lifecycle behavior', () => {
  const source = fixture('burf-main.go');
  const output = wireGo(source);
  assert.match(output, /nativefeedback.Services\(feedbackBridge, \[\]application.Service\{application.NewService\(service\)\}\)/);
  assert.match(output, /nativefeedback.Attach\(feedbackBridge, window\)/);
  assert.match(output, /defer nativefeedback.Stop\(feedbackBridge\)/);
  assert.match(output, /nativefeedback.InstanceID\(feedbackBridge, identity\)/);
  assert.match(output, /if feedbackErr != nil \{\n\t\treturn feedbackErr/);
  const assets = source.slice(source.indexOf('\t\tAssets:'), source.indexOf('\n\t\tMac:'));
  assert.ok(output.includes(assets));
  assert.ok(output.includes('desktop.Attach(service, app, window)'));
  const restored = output
    .replace('\t"example.test/app/native/internal/nativefeedback"\n', '')
    .replace(/feedbackBridge, feedbackErr := nativefeedback\.Start\(nativefeedback\.Config\{CompanionURL: os\.Getenv\("WAILS_FEEDBACK_COMPANION_URL"\)\}\)\n\tif feedbackErr != nil \{\n\t\treturn feedbackErr\n\t\}\n\tdefer nativefeedback\.Stop\(feedbackBridge\)\n\t/, '')
    .replace('nativefeedback.Services(feedbackBridge, []application.Service{application.NewService(service)})', '[]application.Service{application.NewService(service)}')
    .replace('nativefeedback.InstanceID(feedbackBridge, identity)', 'identity')
    .replace('\n\tnativefeedback.Attach(feedbackBridge, window)', '');
  assert.equal(restored, source, 'every original byte remains outside the intended insertions');
});

test('simple Go template gains service and panic boundary without dependencies', () => {
  const source = `package main\nimport "github.com/wailsapp/wails/v3/pkg/application"\nfunc main() {\n app := application.New(application.Options{Name: "Sample"})\n window := app.Window.NewWithOptions(application.WebviewWindowOptions{Name: "main"})\n _ = window\n app.Run()\n}\n`;
  const output = wireGo(source);
  assert.match(output, /Services: nativefeedback.Services\(feedbackBridge, nil\)/);
  assert.match(output, /panic\(feedbackErr\)/);
});

test('ambiguous and repeated Go wiring fails without returning changed source', () => {
  const source = fixture('burf-main.go');
  for (const input of [wireGo(source), source.replace('Name: "main"', 'Name: "secondary"').replace('desktop.Attach(service, app, window)', 'second := app.Window.NewWithOptions(application.WebviewWindowOptions{Name: "other"})\n\t_ = second\n\tdesktop.Attach(service, app, window)')]) {
    const run = spawnSync('go', ['run', fileURLToPath(new URL('../scripts/wire-go.go', import.meta.url)), '--module', 'example.test/app/native'], { cwd: import.meta.dirname, input, encoding: 'utf8' });
    assert.notEqual(run.status, 0);
    assert.equal(run.stdout, '');
    assert.match(run.stderr, /already|exactly one trusted main/);
  }
});

test('an explicit main window wins while foreign window creation remains unchanged', () => {
  const other = 'other := app.Window.NewWithOptions(application.WebviewWindowOptions{Name: "browser"})\n\t_ = other';
  const source = fixture('burf-main.go').replace('desktop.Attach(service, app, window)', `${other}\n\tdesktop.Attach(service, app, window)`);
  const output = wireGo(source);
  assert.ok(output.includes(other));
  assert.match(output, /nativefeedback.Attach\(feedbackBridge, window\)/);
  assert.doesNotMatch(output, /nativefeedback.Attach\(feedbackBridge, other\)/);
});

test('TS unsupported layouts stop before configuration edits', () => {
  assert.throws(() => wireVite('const config = {};', ts, './feedback'), /exactly one default/);
  assert.throws(() => wireReact('const Component = () => <App />;', ts, './feedback'), /root.render/);
  assert.throws(() => wireReact('root.render(condition ? <App /> : null)', ts, './feedback'), /unsupported wrapper/);
  assert.throws(() => wireVite('export default {};', ts, 'external-package'), /relative module/);
});
