import { readFile, writeFile, readdir, lstat, mkdir, realpath, mkdtemp, rm, rename, open } from 'node:fs/promises';
import { writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { resolve, join, relative, dirname, sep } from 'node:path';
import { tmpdir } from 'node:os';
const kit = dirname(fileURLToPath(import.meta.url));
const ledgerPath = '.wails-feedback/setup.json';
const ignored = new Set(['node_modules','.git','dist','build','.wails-feedback']);
const exists = async p => {try {await lstat(p); return true;} catch(e) {if(e.code==='ENOENT') return false; throw e;}};
const slash = p => p.split(sep).join('/');

export function packageManagerCommand(manager, args, platform=process.platform) {
  if(!['pnpm','npm'].includes(manager) || args.some(arg=>!/^[-a-z0-9]+$/i.test(arg))) throw new Error('Unsupported package manager command.');
  return platform==='win32'
    ? {command:process.env.ComSpec??'cmd.exe',args:['/d','/s','/c',`${manager}.cmd ${args.join(' ')}`]}
    : {command:manager,args};
}
function runPackageManager(manager,args,options) {
  const command=packageManagerCommand(manager,args);
  return spawnSync(command.command,command.args,options);
}

async function scan(root, depth=0, prefix='') {
  const files=[];
  for (const entry of await readdir(join(root,prefix), {withFileTypes:true})) {
    if (ignored.has(entry.name) || entry.name.startsWith('._') || entry.name==='.DS_Store') continue;
    const path=join(prefix,entry.name);
    if (entry.isFile()) files.push(slash(path));
    else if(entry.isDirectory() && depth<3) files.push(...await scan(root,depth+1,path));
  }
  return files;
}

export async function detect(root) {
  root=await realpath(resolve(root));
  const files=await scan(root);
  const modules=[]; const frontends=[];
  for(const file of files) {
    if(file.endsWith('go.mod')) {
      const source=await readFile(join(root,file),'utf8');
      if (/github\.com\/wailsapp\/wails\/v3\s/.test(source)) {
        const module=source.match(/^module\s+(\S+)/m)?.[1];
        if(!module) throw new Error(`Missing module identity in ${file}`);
        modules.push({module,native:slash(dirname(file))});
      }
    }
    if(file.endsWith('package.json')) {
      const pkg=JSON.parse(await readFile(join(root,file),'utf8'));
      const deps={...pkg.dependencies,...pkg.devDependencies};
      if(deps.vite) frontends.push({pkg,frontend:slash(dirname(file)),deps});
    }
  }
  if(modules.length!==1 || frontends.length!==1) throw new Error('Expected one Wails v3 module and one Vite frontend. Run from the app repository root; ambiguous layouts are not modified.');
  const {module,native}=modules[0], {frontend,pkg,deps}=frontends[0];
  const framework=deps.react?'React':deps.vue?'Vue':deps.svelte?'Svelte':'vanilla';
  if(framework!=='React') throw new Error(`Detected ${framework}. This release supports React without migrating other frontends; no files changed.`);
  if(!deps.typescript || !deps['@wailsio/runtime']) throw new Error('Existing TypeScript and @wailsio/runtime are required. No toolchain is added automatically.');
  const locks=['pnpm-lock.yaml','package-lock.json','yarn.lock','bun.lock','bun.lockb'].filter(f=>files.includes(slash(join(frontend,f))));
  if(locks.length!==1 || !['pnpm-lock.yaml','package-lock.json'].includes(locks[0])) throw new Error('Expected one pnpm or npm lockfile. Ambiguous or unsupported package managers are not modified.');
  const packageManager=locks[0]==='pnpm-lock.yaml'?'pnpm':'npm';
  if(pkg.packageManager && !pkg.packageManager.startsWith(packageManager+'@')) throw new Error('packageManager and lockfile disagree.');
  const config=['vite.config.ts','vite.config.mts'].filter(f=>files.includes(slash(join(frontend,f))));
  if(config.length!==1) throw new Error('Expected one TypeScript Vite config.');
  const html=await readFile(join(root,frontend,'index.html'),'utf8');
  const entries=[...html.matchAll(/<script\b[^>]*type=["']module["'][^>]*src=["']([^"']+)["']/g)].map(m=>m[1]);
  if(entries.length!==1 || !/^\/?src\/[\w/.-]+\.tsx$/.test(entries[0])) throw new Error('Expected one local src/*.tsx module entry in index.html.');
  if(!pkg.scripts?.dev?.match(/\bvite\b/) || !pkg.scripts?.build?.match(/\bvite\s+build\b/)) throw new Error('Existing dev and build scripts must use Vite.');
  const entry=slash(join(frontend,entries[0].replace(/^\//,'')));
  const main=slash(join(native,'main.go'));
  if(!files.includes(main) || !files.includes(entry)) throw new Error('Go main.go or frontend entry is missing.');
  const burf=module==='github.com/MylesMCook/burf/app/native';
  return {version:1,root,frontend,native,module,framework,packageManager,lock:slash(join(frontend,locks[0])),config:slash(join(frontend,config[0])),entry,main,devScript:'dev',buildScript:'build',trustedMarker:burf?'__BURF_WAILS__':null,appName:pkg.name??'Wails app',burf,nativePrepare:burf?'scripts/native-prepare.mjs':null,windowsLoader:burf?'scripts/webview2-loader.mjs':null};
}

// Merge an owned edit with subsequent unrelated work. Conflicts abort before writes.
export function reconcile(current,base,desired) {
  if(current===base || current===desired) return desired;
  const dir=mkdtempSync(join(tmpdir(),'feedback-merge-'));
  try {
    for(const [name,value] of [['current',current],['base',base],['desired',desired]]) writeFileSync(join(dir,name),value);
    const result=spawnSync('git',['merge-file','-p',join(dir,'current'),join(dir,'base'),join(dir,'desired')],{encoding:'utf8'});
    if(result.status!==0) throw new Error('Setup conflict: an owned edit changed. Restore or reconcile that edit before rerunning or undoing.');
    return result.stdout;
  } finally {rmSync(dir,{recursive:true,force:true});}
}

async function safePath(root,file) {
  if(typeof file!=='string' || /[\\:\x00-\x1f]/.test(file) || file.startsWith('/') || file.split('/').some(part=>!part || part==='.' || part==='..')) throw new Error(`Unsafe managed path ${file}`);
  if(!resolve(root,file).startsWith(root+sep)) throw new Error(`Managed path escapes app root: ${file}`);
  let path=root;
  for(const part of file.split('/')) {path=join(path,part); if(await exists(path) && (await lstat(path)).isSymbolicLink()) throw new Error(`Refusing symlink ${file}`);}
  return path;
}

export async function replaceFile(path, content, mode) {
  const temporary = path + '.wails-feedback-tmp';
  // Exclusive creation proves ownership; never remove a pre-existing file.
  const handle = await open(temporary, 'wx', mode);
  let installed = false;
  try {
    await handle.writeFile(content);
    await handle.close();
    await rename(temporary, path);
    installed = true;
  } finally {
    await handle.close();
    if (!installed) await rm(temporary, {force:true});
  }
}

async function commit(root, changes) {
  const written=[];
  // Validate the complete transaction before touching any app file.
  for(const change of changes) {
    const path=await safePath(root,change.path);
    const current=await exists(path)?await readFile(path,'utf8'):null;
    if(current!==change.current) throw new Error(`File changed during setup: ${change.path}`);
  }
  try {
    for(const change of changes) {
      const path=await safePath(root,change.path);
      const current=await exists(path)?await readFile(path,'utf8'):null;
      if(current!==change.current) throw new Error(`File changed during setup: ${change.path}`);
      if(change.desired===null) await rm(path);
      else {await mkdir(dirname(path),{recursive:true}); const mode=current===null?(change.path===ledgerPath?0o600:0o644):(await lstat(path)).mode&0o777; await replaceFile(path,change.desired,mode);}
      written.push(change);
    }
  } catch(error) {
    for(const change of written.reverse()) {const path=join(root,change.path); if(change.current===null) await rm(path,{force:true}); else await writeFile(path,change.current);}
    throw error;
  }
}

async function managed(root,records,undo=false) {
  const changes=[];
  for(const record of records) {
    const path=await safePath(root,record.path);
    const current=await exists(path)?await readFile(path,'utf8'):null;
    const base=undo?record.after:record.before, desired=undo?record.before:record.after;
    let merged;
    if(current===base || current===desired) merged=desired;
    else if(current===null || base===null || desired===null) throw new Error(`Setup conflict in ${record.path}; preserve it before ${undo?'undo':'rerun'}.`);
    else merged=reconcile(current,base,desired);
    if(merged!==current) changes.push({path:record.path,current,desired:merged});
  }
  return changes;
}

export async function setup(root,options={}) {
  root=await realpath(resolve(root));
  const ledger=await safePath(root,ledgerPath);
  if(await exists(ledger)) {
    const previous=JSON.parse(await readFile(ledger,'utf8'));
    if(previous.version!==1 || !Array.isArray(previous.files) || previous.files.some(record=>!record || typeof record.path!=='string' || (record.before!==null && typeof record.before!=='string') || (record.after!==null && typeof record.after!=='string')) || new Set(previous.files.map(record=>record.path)).size!==previous.files.length) throw new Error('Unsupported setup ledger; no files changed.');
    for(const record of previous.files) await safePath(root,record.path);
    if(typeof previous.plan?.frontend!=='string') throw new Error('Unsupported setup ledger plan; no files changed.');
    const plans=previous.files.filter(record=>record.path==='wails-feedback/plan.json' || record.path.endsWith('/wails-feedback/plan.json'));
    if(plans.length!==1 || plans[0].path!==slash(join(previous.plan.frontend,'wails-feedback/plan.json'))) throw new Error('Setup ledger layout differs from its generated plan; no files changed.');
    const recordedPlan=JSON.parse(plans[0].after);
    if(['frontend','native','module'].some(key=>previous.plan[key]!==recordedPlan[key])) throw new Error('Setup ledger layout differs from its generated plan; no files changed.');
    const runtime=slash(join(previous.plan.frontend,'wails-feedback'));
    const state=await safePath(root,runtime+'/state');
    if(!options.dryRun && await exists(await safePath(root,runtime+'/state/run.lock'))) throw new Error('Close the feedback run before setup or undo. If its lock is stale, verify its owner before removing state/run.lock.');
    const retainPrivateIgnore=Boolean(options.undo && await exists(state));
    const changes=await managed(root,previous.files,Boolean(options.undo));
    if(retainPrivateIgnore) {
      const protective=changes.find(c=>c.path===runtime+'/.gitignore');
      if(protective) {
        protective.desired=protective.desired??protective.current;
        if(!protective.desired.split(/\r?\n/).includes('state/')) protective.desired+=(protective.desired.endsWith('\n')||!protective.desired?'':'\n')+'state/\n';
      }
    }
    if(options.undo) changes.push({path:ledgerPath,current:await readFile(ledger,'utf8'),desired:null});
    if(!options.dryRun) await commit(root,changes);
    if(!options.dryRun && options.install!==false) {
      const plan=await detect(root);
      const result=runPackageManager(plan.packageManager,plan.packageManager==='pnpm'?['install','--frozen-lockfile']:['ci'],{cwd:join(root,plan.frontend),stdio:'inherit'});
      if(result.status!==0) throw new Error('Owned files were reconciled, but dependency restoration failed. Restore from the current lockfile.');
    }
    return {action:options.undo?'undo':'rerun',changes:changes.map(c=>c.path),retainedPrivateState:retainPrivateIgnore,plan:previous.plan};
  }
  if(options.undo) throw new Error('No native-feedback setup exists here.');
  const plan=await detect(root);
  if(options.dryRun) return {action:'plan',plan};
  const require=createRequire(join(root,plan.frontend,'package.json'));
  let ts; try {ts=require('typescript');} catch {throw new Error(`Restore existing dependencies with ${plan.packageManager} install, then rerun setup.`);}
  const {wireVite,wireReact}=await import('./scripts/wire-ts.mjs');
  const records=[];
  async function add(path,after) {const before=await exists(join(root,path))?await readFile(join(root,path),'utf8'):null; records.push({path,before,after});}
  const go=spawnSync('go',['run',join(kit,'scripts/wire-go.go'),'--module',plan.module],{input:await readFile(join(root,plan.main),'utf8'),encoding:'utf8',cwd:root});
  if(go.status!==0) throw new Error(go.stderr||'Go main could not be wired.');
  await add(plan.main,go.stdout);
  const startupEntries=['/'+slash(relative(plan.frontend,plan.entry))];
  if(plan.burf) startupEntries.push('/src/plugins/host.ts','/src/App.tsx','/bindings/'+plan.module+'/desktop/service.ts');
  startupEntries.push('/src/native-feedback/FeedbackGate.tsx','/src/native-feedback/FeedbackOverlay.tsx');
  await add(plan.config,wireVite(await readFile(join(root,plan.config),'utf8'),ts,'./src/native-feedback/feature.mjs',startupEntries));
  let overlayImport=slash(relative(dirname(join(root,plan.entry)),join(root,plan.frontend,'src/native-feedback/NativeFeedback')));
  if(!overlayImport.startsWith('.')) overlayImport='./'+overlayImport;
  await add(plan.entry,wireReact(await readFile(join(root,plan.entry),'utf8'),ts,overlayImport));
  for(const [source,dest] of [['backend',join(plan.native,'internal/nativefeedback')],['frontend',join(plan.frontend,'src/native-feedback')],['runtime',join(plan.frontend,'wails-feedback')]]) {
    for(const file of await scan(join(kit,source))) {
      if(file.includes('/tests/') || (file.endsWith('.test.mjs') && source!=='runtime')) continue;
      const path=slash(join(dest,file));
      let content=await readFile(join(kit,source,file),'utf8');
      content=content.replaceAll('WAILS_FEEDBACK_MODULE',source==='frontend'?JSON.stringify(plan.module):plan.module).replaceAll('WAILS_FEEDBACK_APP_NAME',JSON.stringify(plan.appName)).replaceAll('WAILS_FEEDBACK_TRUSTED_MARKER',JSON.stringify(plan.trustedMarker));
      if(await exists(join(root,path)) && !(source==='runtime' && file==='.gitignore' && (await readFile(join(root,path),'utf8')).replaceAll('\r\n','\n')===content.replaceAll('\r\n','\n'))) throw new Error(`Refusing to overwrite ${path}`);
      await add(path,content);
    }
  }
  const runtimeRoot=slash(relative(join(root,plan.frontend,'wails-feedback'),root)) || '.';
  await add(slash(join(plan.frontend,'wails-feedback/plan.json')),JSON.stringify({...plan,root:runtimeRoot},null,2)+'\n');
  const packagePath=slash(join(plan.frontend,'package.json'));
  const pkg=JSON.parse(await readFile(join(root,packagePath),'utf8'));
  for(const script of ['dev:feedback','feedback:connect','feedback:disconnect','test:feedback']) if(pkg.scripts[script]) throw new Error(`Existing ${script} script would be overwritten.`);
  pkg.scripts['dev:feedback']='node wails-feedback/run.mjs';
  pkg.scripts['feedback:connect']='node wails-feedback/connect-codex.mjs';
  pkg.scripts['feedback:disconnect']='node wails-feedback/connect-codex.mjs --remove';
  pkg.scripts['test:feedback']='node --test wails-feedback/mcp.test.mjs';
  if(pkg.scripts.test) pkg.scripts.test+=' && node --test wails-feedback/mcp.test.mjs';
  for(const [name,version] of Object.entries({agentation:'3.1.2','agentation-mcp':'1.3.2'})) {
    if(pkg.dependencies?.[name] || pkg.devDependencies?.[name]) throw new Error(`Existing ${name} dependency needs explicit reconciliation; setup will not replace it.`);
    (pkg.devDependencies??={})[name]=version;
  }
  let pnpmPolicy;
  if(plan.packageManager==='pnpm') {
    const path=slash(join(plan.frontend,'pnpm-workspace.yaml'));
    const source=await exists(join(root,path))?await readFile(join(root,path),'utf8'):'';
    if(/^\s+better-sqlite3:\s*false\s*$/m.test(source)) throw new Error('Existing pnpm policy denies the companion SQLite build. No files changed.');
    if(!/^\s+better-sqlite3:\s*true\s*$/m.test(source)) {
      if(/^allowBuilds:\s*$/m.test(source)) pnpmPolicy=source.replace(/^allowBuilds:\s*$/m,'allowBuilds:\n  better-sqlite3: true');
      else if(/\ballowBuilds\s*:/.test(source)) throw new Error('Unsupported pnpm allowBuilds policy syntax; no files changed.');
      else pnpmPolicy=source+'\nallowBuilds:\n  better-sqlite3: true\n';
      await add(path,pnpmPolicy);
    }
  }
  // Generate dependency resolution in a disposable folder before changing the app.
  const stage=await mkdtemp(join(tmpdir(),'wails-feedback-deps-'));
  try {
    await writeFile(join(stage,'package.json'),JSON.stringify(pkg,null,2)+'\n');
    await writeFile(join(stage,plan.lock.split('/').at(-1)),await readFile(join(root,plan.lock)));
    for(const file of ['pnpm-workspace.yaml','.npmrc']) {
      const original=join(root,plan.frontend,file);
      if(await exists(original)) await writeFile(join(stage,file),await readFile(original));
    }
    if(pnpmPolicy!==undefined) await writeFile(join(stage,'pnpm-workspace.yaml'),pnpmPolicy);
    const args=plan.packageManager==='pnpm'?['install','--lockfile-only','--ignore-scripts']:['install','--package-lock-only','--ignore-scripts'];
    if(options.resolveDependencies) await options.resolveDependencies(stage,plan);
    else {
      const resolution=runPackageManager(plan.packageManager,args,{cwd:stage,encoding:'utf8'});
      if(resolution.status!==0) throw new Error('Dependency resolution failed; app files unchanged. '+resolution.stderr);
    }
    await add(packagePath,JSON.stringify(pkg,null,2)+'\n');
    await add(plan.lock,await readFile(join(stage,plan.lock.split('/').at(-1)),'utf8'));
  } finally {await rm(stage,{recursive:true,force:true});}
  if(plan.burf) {
    const path='scripts/ui-manifest.mjs';
    const source=await readFile(join(root,path),'utf8');
    const anchor='  if (!files["index.html"]) throw new Error("Missing index.html");';
    if(!source.includes(anchor)) throw new Error('Burf UI manifest guard changed; no files modified.');
    await add(path,source.replace(anchor,anchor+'\n  if ((await readFile(join(dist, "index.html"), "utf8")).includes("wails-native-feedback")) throw new Error("Feedback bundles cannot be installed as release UI.");'));
  }
  const files=records.filter(r=>r.before!==r.after);
  const changes=files.map(r=>({path:r.path,current:r.before,desired:r.after}));
  changes.push({path:ledgerPath,current:null,desired:JSON.stringify({version:1,plan:{...plan,root:undefined},files},null,2)+'\n'});
  await commit(root,changes);
  if(options.install!==false) {
    const result=runPackageManager(plan.packageManager,plan.packageManager==='pnpm'?['install','--frozen-lockfile']:['ci'],{cwd:join(root,plan.frontend),stdio:'inherit'});
    if(result.status!==0) throw new Error('Setup files are installed, but dependency restoration failed. Rerun your package manager install or use --undo.');
  }
  return {action:'setup',plan,changes:changes.map(c=>c.path)};
}

if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  const flags=new Set(process.argv.slice(2).filter(s=>s.startsWith('--')));
  const unknown=[...flags].filter(s=>!['--dry-run','--undo','--no-install','--help'].includes(s));
  if(unknown.length) {console.error(`Unknown option: ${unknown.join(', ')}`);process.exitCode=1;}
  else if(flags.has('--help')) console.log('node setup.mjs [repository-root] [--dry-run | --undo] [--no-install]\nDetects React/Vite and npm/pnpm Wails v3 apps; preserves existing scripts.');
  else {
    try {console.log(JSON.stringify(await setup(process.argv.slice(2).find(s=>!s.startsWith('--'))??process.cwd(),{dryRun:flags.has('--dry-run'),undo:flags.has('--undo'),install:!flags.has('--no-install')}),null,2));}
    catch(error) {console.error(error.message);process.exitCode=1;}
  }
}
