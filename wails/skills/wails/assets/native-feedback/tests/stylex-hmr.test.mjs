import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { nativeStylexHMR } from '../frontend/stylex-hmr.mjs';
const source = `const DEV_CSS_PATH = '/virtual:stylex.css';
const AFTER_UPDATE_DELAY = 180;
async function fetchCSS() {
  const t = Date.now();
  const r = await fetch(DEV_CSS_PATH + '?t=' + t, {cache: 'no-store'});
  return r.text();
}
async function update() {
  try {
    const css = await fetchCSS();
    applied.push(css);
  } catch {}
}
update();
if(import.meta.hot){
  import.meta.hot.on('stylex:css-update', update);
  import.meta.hot.on('vite:afterUpdate', () => setTimeout(update, AFTER_UPDATE_DELAY));
  import.meta.hot.dispose(() => {
    applied.push('disposed');
  });
}`;
const settle = () => new Promise(resolve => setImmediate(resolve));
function fixture(input) {
  const hooks = new Map(), requests = [], applied = [], timers = [];
  let dispose;
  const hot = { on(event, cb) { hooks.set(event, cb); }, dispose(cb) { dispose = cb; } };
  const code = input.replaceAll('import.meta.hot', 'hot');
  vm.runInNewContext(code, { hot, applied, AbortController, Date, setTimeout(cb, ms) { const timer = { cb, ms }; timers.push(timer); return timer; }, clearTimeout(timer) { timer.cleared = true; }, fetch(url, options) { return new Promise((resolve,reject) => { requests.push({url,options,resolve,reject}); options.signal?.addEventListener('abort',()=>reject(new Error('aborted'))); }); } });
  return { hooks, requests, applied, timers, dispose: () => dispose() };
}

test('a stalled CSS response cannot block later HMR and bursts retain latest CSS', async () => {
  const output = nativeStylexHMR().transform(source, '/@id/virtual:stylex:runtime');
  const f = fixture(output.code);
  assert.equal(f.requests.length, 1);
  for (let i=0;i<10;i++) assert.equal(f.hooks.get('stylex:css-update')(), undefined);
  assert.equal(f.requests.length, 1);
  let laterHMR = false;
  await Promise.resolve(f.hooks.get('stylex:css-update')()).then(()=>{laterHMR=true;});
  assert.equal(laterHMR,true);
  f.requests[0].resolve({text:async()=> 'initial'}); await settle();
  assert.equal(f.requests.length,2);
  f.requests[1].resolve({text:async()=> 'latest'}); await settle();
  assert.deepEqual(f.applied,['initial','latest']);
  assert.equal(f.hooks.get('vite:afterUpdate')().ms,180);
});

test('deadline aborts a stalled request and disposal rejects late CSS writes', async () => {
  const f = fixture(nativeStylexHMR().transform(source, 'virtual:stylex:runtime').code);
  f.hooks.get('stylex:css-update')();
  f.timers.find(x=>x.ms===5000).cb(); await settle();
  assert.equal(f.requests[0].options.signal.aborted,true);
  assert.equal(f.requests.length,2);
  // A body already being read must not write CSS after the module is disposed.
  let finishBody;
  f.requests[1].resolve({text:()=>new Promise(resolve=>{finishBody=resolve;})}); await settle();
  f.dispose(); finishBody('late'); await settle();
  assert.equal(f.requests[1].options.signal.aborted,true);
  assert.deepEqual(f.applied,['disposed']);
  assert.equal(f.hooks.get('stylex:css-update')(),undefined);
  assert.equal(f.requests.length,2);
});

test('unrelated modules remain untouched and unreviewed runtimes fail explicitly', () => {
  assert.equal(nativeStylexHMR().transform(source,'/src/App.tsx'),null);
  assert.throws(()=>nativeStylexHMR().transform(source.replace('return r.text();','return r.json();'),'virtual:stylex:runtime'),/Unsupported StyleX/);
});
