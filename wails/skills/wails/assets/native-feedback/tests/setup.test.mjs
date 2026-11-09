import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, rm, symlink, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';
import { detect, reconcile, setup, packageManagerCommand } from '../setup.mjs';

test('dependency commands use Windows cmd launchers with bounded arguments',()=>{
  assert.deepEqual(packageManagerCommand('pnpm',['install','--frozen-lockfile'],'darwin'),{command:'pnpm',args:['install','--frozen-lockfile']});
  assert.equal(packageManagerCommand('pnpm',['install','--lockfile-only','--ignore-scripts'],'win32').args.at(-1),'pnpm.cmd install --lockfile-only --ignore-scripts');
  assert.equal(packageManagerCommand('npm',['ci'],'win32').args.at(-1),'npm.cmd ci');
  assert.throws(()=>packageManagerCommand('pnpm',['install&echo'],'win32'));
});

test('detects split pnpm React/Vite Wails layout without changing files', async () => {
  const root = await mkdtemp(join(tmpdir(), 'feedback-layout-'));
  try {
    await mkdir(join(root, 'app/native'), {recursive:true});
    await mkdir(join(root, 'app/src'));
    await writeFile(join(root,'app/package.json'), JSON.stringify({dependencies:{react:'19', '@wailsio/runtime':'3.0.0-beta.28'},devDependencies:{vite:'8',typescript:'6'},scripts:{dev:'node scripts/build-plugins.mjs && vite',build:'tsc && vite build'}}));
    await writeFile(join(root,'app/._package.json'),'archive metadata, not a package manifest');
    await writeFile(join(root,'app/pnpm-lock.yaml'), 'lockfileVersion: 9');
    await writeFile(join(root,'app/index.html'), '<script type="module" src="/src/main.tsx"></script>');
    await writeFile(join(root,'app/src/main.tsx'), '<App />');
    await writeFile(join(root,'app/vite.config.ts'), 'export default {}');
    await writeFile(join(root,'app/native/go.mod'), 'module example/app/native\nrequire github.com/wailsapp/wails/v3 v3.0.0-beta.28\n');
    await writeFile(join(root,'app/native/main.go'), 'package main');
    const plan = await detect(root);
    assert.equal(plan.frontend,'app'); assert.equal(plan.native,'app/native');
    assert.equal(plan.packageManager,'pnpm'); assert.equal(plan.module,'example/app/native');
    assert.equal(plan.devScript,'dev'); assert.equal(plan.entry,'app/src/main.tsx');
    assert.equal(await readFile(join(root,'app/vite.config.ts'),'utf8'), 'export default {}');
  } finally {await rm(root,{recursive:true,force:true});}
});

test('three-way reconciliation preserves independent work and refuses conflicts', () => {
  assert.equal(reconcile('one\ntwo\n','one\ntwo\n','one\nfeedback\ntwo\n'), 'one\nfeedback\ntwo\n');
  assert.equal(reconcile('one\nfeedback\ntwo\n','one\nfeedback\ntwo\n','one\ntwo\n'), 'one\ntwo\n');
  assert.throws(() => reconcile('different\n','one\n','replacement\n'), /conflict/i);
  assert.equal(reconcile('a\nb\nc\nd\nchanged\n','a\nb\nc\nd\ne\n','feedback\na\nb\nc\nd\ne\n'),'feedback\na\nb\nc\nd\nchanged\n');
});

async function fixture() {
  const root=await mkdtemp(join(tmpdir(),'feedback-install-'));
  await mkdir(join(root,'app/native'),{recursive:true});
  await mkdir(join(root,'app/src'));
  await mkdir(join(root,'scripts'));
  for(const [source,path] of [['burf-main.go','app/native/main.go'],['burf-vite.ts','app/vite.config.ts'],['burf-main.tsx','app/src/main.tsx']]) await writeFile(join(root,path),await readFile(new URL('fixtures/'+source,import.meta.url)));
  await symlink(join(process.env.WAILS_FEEDBACK_TEST_APP,'node_modules'),join(root,'app/node_modules'),process.platform==='win32'?'junction':'dir');
  await writeFile(join(root,'app/native/go.mod'),'module github.com/MylesMCook/burf/app/native\nrequire github.com/wailsapp/wails/v3 v3.0.0-beta.28\n');
  await writeFile(join(root,'app/index.html'),'<script type="module" src="/src/main.tsx"></script>');
  await writeFile(join(root,'app/package.json'),JSON.stringify({name:'burf',dependencies:{react:'19','@wailsio/runtime':'3.0.0-beta.28'},devDependencies:{typescript:'6',vite:'8'},scripts:{dev:'node scripts/build-plugins.mjs && vite',build:'tsc && vite build'}})+'\n');
  await writeFile(join(root,'app/pnpm-lock.yaml'),'fixture lock\n');
  await writeFile(join(root,'app/pnpm-workspace.yaml'),'allowBuilds:\n  esbuild: true\nminimumReleaseAge: 60\n');
  await writeFile(join(root,'scripts/ui-manifest.mjs'),'async function manifest(dist) {\n  const files = {};\n  if (!files["index.html"]) throw new Error("Missing index.html");\n}\n');
  return root;
}
async function snapshot(root, prefix='') {
  const files={};
  for(const entry of await readdir(join(root,prefix),{withFileTypes:true})) {
    if(entry.name==='node_modules') continue;
    const path=join(prefix,entry.name);
    if(entry.isDirectory()) Object.assign(files,await snapshot(root,path));
    else files[path.replaceAll('\\','/')]=await readFile(join(root,path),'utf8');
  }
  return files;
}
const options={install:false,resolveDependencies:async stage=>{await writeFile(join(stage,'pnpm-lock.yaml'),'resolved fixture lock\n');}};

test('complete installer wires split app, reruns unchanged, and undo preserves later unrelated work', async () => {
  const root=await fixture();
  try {
    const before=await snapshot(root);
    const first=await setup(root,options);
    assert.equal(first.action,'setup');
    const installed=await snapshot(root);
    assert.match(installed['app/native/main.go'],/nativefeedback.Attach/);
    assert.match(installed['scripts/ui-manifest.mjs'],/Feedback bundles cannot/);
    assert.match(installed['app/pnpm-workspace.yaml'],/esbuild: true/);
    assert.match(installed['app/pnpm-workspace.yaml'],/better-sqlite3: true/);
    assert.equal(JSON.parse(installed['app/wails-feedback/plan.json']).root,'../..');
    assert.deepEqual((await setup(root,options)).changes,[]);
    assert.deepEqual(await snapshot(root),installed);
    await writeFile(join(root,'app/src/main.tsx'),installed['app/src/main.tsx']+'\n// independent later work\n');
    await setup(root,{...options,undo:true});
    const restored=await snapshot(root);
    before['app/src/main.tsx']+='\n// independent later work\n';
    assert.deepEqual(restored,before);
  } finally {await rm(root,{recursive:true,force:true});}
});

test('owned conflict and resolver failure leave all app bytes unchanged', async () => {
  const root=await fixture();
  try {
    const before=await snapshot(root);
    await assert.rejects(setup(root,{install:false,resolveDependencies:()=>{throw new Error('synthetic resolution failure');}}),/resolution failure/);
    assert.deepEqual(await snapshot(root),before);
    await setup(root,options);
    await writeFile(join(root,'app/src/main.tsx'),'conflicting replacement\n');
    const conflict=await snapshot(root);
    await assert.rejects(setup(root,{...options,undo:true}),/conflict/i);
    assert.deepEqual(await snapshot(root),conflict);
  } finally {await rm(root,{recursive:true,force:true});}
});

test('undo refuses a running workflow and preserves Git protection for retained private state', async () => {
  const root=await fixture();
  try {
    await setup(root,options);
    const state=join(root,'app/wails-feedback/state');
    const protectiveIgnore=await readFile(join(root,'app/wails-feedback/.gitignore'),'utf8');
    await mkdir(join(state,'run.lock'),{recursive:true});
    await writeFile(join(state,'test-token'),'synthetic private token');
    await writeFile(join(state,'annotations.sqlite'),'synthetic annotation database');
    const running=await snapshot(root);
    const ledgerPath=join(root,'.wails-feedback/setup.json');
    const receipt=await readFile(ledgerPath,'utf8');
    const wrong=JSON.parse(receipt);wrong.plan.frontend='docs-site';
    await writeFile(ledgerPath,JSON.stringify(wrong));
    const malformed=await snapshot(root);
    await assert.rejects(setup(root,{...options,undo:true}),/ledger layout differs/);
    assert.deepEqual(await snapshot(root),malformed);
    await writeFile(ledgerPath,receipt);
    await assert.rejects(setup(root,{...options,undo:true}),/Close the feedback run/);
    await assert.rejects(setup(root,options),/Close the feedback run/);
    assert.equal((await setup(root,{...options,dryRun:true})).action,'rerun');
    assert.deepEqual(await snapshot(root),running);
    await rm(join(state,'run.lock'),{recursive:true});
    assert.equal((await setup(root,{...options,undo:true})).retainedPrivateState,true);
    assert.equal(await readFile(join(root,'app/wails-feedback/.gitignore'),'utf8'),protectiveIgnore);
    execFileSync('git',['init','--quiet'],{cwd:root});
    for(const file of ['test-token','annotations.sqlite']) execFileSync('git',['check-ignore','--quiet','app/wails-feedback/state/'+file],{cwd:root});
    await setup(root,options);
    assert.deepEqual((await setup(root,options)).changes,[]);
    await setup(root,{...options,undo:true});
    assert.equal(await readFile(join(state,'test-token'),'utf8'),'synthetic private token');
  } finally {await rm(root,{recursive:true,force:true});}
});

test('malformed Windows receipt paths and symlink receipts are rejected', async () => {
  const root=await fixture();
  try {
    await mkdir(join(root,'.wails-feedback'));
    const ledger=join(root,'.wails-feedback/setup.json');
    await writeFile(ledger,JSON.stringify({version:1,files:[{path:'..\\outside',before:null,after:'owned'}]}));
    await assert.rejects(setup(root,{install:false,undo:true}),/Unsafe managed path/);
    await rm(ledger);
    await symlink(join(root,'app/package.json'),ledger);
    await assert.rejects(setup(root,{install:false,undo:true}),/symlink/);
  } finally {await rm(root,{recursive:true,force:true});}
});

test('a failed atomic rename removes only its own temporary file and can be retried', async () => {
  const { replaceFile } = await import('../setup.mjs');
  const root=await mkdtemp(join(tmpdir(),'feedback-rename-'));
  const path=join(root,'target');
  try {
    await mkdir(path);
    await assert.rejects(replaceFile(path,'new bytes',0o600));
    assert.deepEqual(await readdir(root),['target']);
    await rm(path,{recursive:true});
    await replaceFile(path,'new bytes',0o600);
    assert.equal(await readFile(path,'utf8'),'new bytes');
    await writeFile(path+'.wails-feedback-tmp','unrelated bytes');
    await assert.rejects(replaceFile(path,'replacement',0o600),{code:'EEXIST'});
    assert.equal(await readFile(path+'.wails-feedback-tmp','utf8'),'unrelated bytes');
    assert.equal(await readFile(path,'utf8'),'new bytes');
  } finally {await rm(root,{recursive:true,force:true});}
});

test('undo preserves private ignore bytes and reinstall accepts equivalent LF or CRLF rules',async()=>{
  const root=await fixture();
  try{
    await setup(root,options);
    const path=join(root,'app/wails-feedback/.gitignore');
    const original=await readFile(path,'utf8');
    const alternate=original.includes('\r\n')?original.replaceAll('\r\n','\n'):original.replaceAll('\n','\r\n');
    const ledger=join(root,'.wails-feedback/setup.json');const receipt=JSON.parse(await readFile(ledger,'utf8'));
    receipt.files.find(f=>f.path==='app/wails-feedback/.gitignore').after=alternate;
    await writeFile(ledger,JSON.stringify(receipt));await writeFile(path,alternate);
    await mkdir(join(root,'app/wails-feedback/state'));
    await writeFile(join(root,'app/wails-feedback/state/private-data'),'synthetic');
    await setup(root,{...options,undo:true});
    assert.equal(await readFile(path,'utf8'),alternate);
    await setup(root,options);
    assert.deepEqual((await setup(root,options)).changes,[]);
    assert.equal(await readFile(join(root,'app/wails-feedback/state/private-data'),'utf8'),'synthetic');
  }finally{await rm(root,{recursive:true,force:true});}
});
