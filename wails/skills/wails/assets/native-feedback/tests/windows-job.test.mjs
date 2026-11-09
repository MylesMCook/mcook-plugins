import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { writeFile, rm } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { windowsProcess } from '../runtime/windows-process.mjs';

const directory = dirname(fileURLToPath(import.meta.url));
function running(pid) { try { process.kill(pid, 0); return true; } catch(error) { if(error.code === 'ESRCH') return false; throw error; } }
async function gone(pids) {
  const deadline = Date.now() + 10000;
  while(pids.some(running)) {
    assert.ok(Date.now() < deadline, `Owned synthetic process survived: ${pids.filter(running).join(',')}`);
    await new Promise(resolve => setTimeout(resolve, 25));
  }
}
function launch(command, args, environment=process.env) {
  const spec = windowsProcess(command, args, directory, environment);
  return spawn(spec.command, spec.args, { cwd: directory, env: spec.env, windowsHide: true, stdio:['ignore','pipe','pipe'] });
}
function records(stream, kinds) {
  return new Promise((resolve, reject) => {
    let buffer=''; const found={};
    const timer=setTimeout(()=>reject(new Error(`Synthetic process metadata missing: ${kinds.filter(kind=>!found[kind]).join(',')}`)),20000);
    stream.on('data', chunk=> {
      buffer+=chunk;
      const lines=buffer.split(/\r?\n/); buffer=lines.pop();
      for(const line of lines) {
        try { const record=JSON.parse(line); if(kinds.includes(record.kind))found[record.kind]=record.pid; } catch {}
      }
      if(kinds.every(kind=>found[kind])){clearTimeout(timer);resolve(found);}
    });
    stream.once('error', error=>{clearTimeout(timer);reject(error);});
  });
}
async function killOwned(child) {
  if(child.exitCode === null && child.signalCode === null) {
    const killer=spawn('taskkill.exe',['/PID',String(child.pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});
    await once(killer,'exit');
  }
}

test('Windows owned job returns its child exit code', {skip:process.platform!=='win32',timeout:30000}, async()=> {
  const child=launch(process.execPath,['-e','process.stdout.write("normal exit"); process.exit(7)']);
  let stderr='';child.stderr.on('data', chunk=>stderr+=chunk);
  try {const [code]=await once(child,'close');assert.equal(code,7,stderr);} finally {await killOwned(child);}
});

const leaf='process.on("SIGTERM",()=>{}); console.log(JSON.stringify({kind:"descendant",pid:process.pid})); setInterval(()=>{},1000)';
const leader=`const {spawn}=require("node:child_process");console.log(JSON.stringify({kind:"leader",pid:process.pid}));const c=spawn(process.execPath,["-e",${JSON.stringify(leaf)}],{stdio:["ignore","pipe","ignore"]});c.stdout.pipe(process.stdout);setInterval(()=>{},1000);`;

test('Windows owned job kills a descendant when its leader exits', {skip:process.platform!=='win32',timeout:30000}, async()=> {
  const code=leader.replace('c.stdout.pipe(process.stdout);setInterval(()=>{},1000);','c.stdout.once("data",data=>{process.stdout.write(data,()=>process.exit(0));});');
  const wrapper=launch(process.execPath,['-e',code]);
  let stderr='';wrapper.stderr.on('data', chunk=>stderr+=chunk);
  const closed=once(wrapper,'close');
  try {
    const pids=await records(wrapper.stdout,['leader','descendant']);
    assert.equal((await closed)[0],0,stderr);
    await gone(Object.values(pids));
  } finally {await killOwned(wrapper);}
});

test('Windows owned job kills its complete child tree after Node parent death', {skip:process.platform!=='win32',timeout:45000}, async()=> {
  const driver=join(directory,'synthetic-parent.mjs');
  await writeFile(driver,`import {spawn} from 'node:child_process';\nimport {windowsProcess} from '../runtime/windows-process.mjs';\nconst spec=windowsProcess(process.execPath,['-e',${JSON.stringify(leader)}],${JSON.stringify(directory)},process.env);\nconst wrapper=spawn(spec.command,spec.args,{cwd:${JSON.stringify(directory)},env:spec.env,windowsHide:true,stdio:['ignore','pipe','pipe']});\nconsole.log(JSON.stringify({kind:'wrapper',pid:wrapper.pid}));\nwrapper.stdout.pipe(process.stdout);wrapper.stderr.pipe(process.stderr);setInterval(()=>{},1000);\n`);
  const parent=spawn(process.execPath,[driver],{cwd:directory,windowsHide:true,stdio:['ignore','pipe','pipe']});
  let wrapperPID;
  let stderr='';parent.stderr.on('data', chunk=>stderr+=chunk);
  try {
    const pids=await records(parent.stdout,['wrapper','leader','descendant']);
    wrapperPID=pids.wrapper;
    const exited=once(parent,'exit');
    parent.kill('SIGKILL');
    await exited;
    await gone(Object.values(pids));
    // PowerShell may emit its empty CLIXML stream header while the parent dies.
    // Preserve a failure for actual diagnostics, rather than treating framing
    // from the PowerShell host as an orphaned child process.
    assert.match(stderr,/^(?:#< CLIXML\r?\n)?$/);
  } finally {
    if(parent.exitCode===null && parent.signalCode===null)parent.kill('SIGKILL');
    if(wrapperPID && running(wrapperPID)) {const killer=spawn('taskkill.exe',['/PID',String(wrapperPID),'/T','/F'],{windowsHide:true,stdio:'ignore'});await once(killer,'exit');}
    await rm(driver,{force:true});
  }
});
