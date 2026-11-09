import test from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {once} from 'node:events';
import {nativeStartup,readinessPath} from '../frontend/startup.mjs';
async function fixture(environment) {
  let middleware;const errors=[];
  const server=createServer((req,res)=>middleware(req,res,()=>res.end('existing application asset')));
  nativeStartup(['/src/main.tsx','/src/App.tsx']).configureServer({httpServer:server,environments:{client:environment},config:{logger:{error:e=>errors.push(e)}},middlewares:{use:fn=>{middleware=fn;}}});
  server.listen(0,'127.0.0.1');await once(server,'listening');
  return {url:'http://127.0.0.1:'+server.address().port,errors,close:()=>new Promise(r=>server.close(r))};
}

test('readiness stays unavailable until startup modules and their dependency crawl finish; HTML and other assets keep working',async()=>{
  let finish;const waiting=new Promise(resolve=>{finish=resolve;});const warmed=[];
  const f=await fixture({async transformRequest(entry){warmed.push(entry);return {code:'module'};},waitForRequestsIdle:()=>waiting});
  try {
    const before=await fetch(f.url+readinessPath);assert.equal(before.status,503);assert.equal(before.headers.get('Cache-Control'),'no-store');
    assert.equal(await(await fetch(f.url+'/')).text(),'existing application asset');
    assert.equal(await(await fetch(f.url+'/src/other.ts')).text(),'existing application asset');
    assert.deepEqual(warmed,['/src/main.tsx','/src/App.tsx']);
    assert.equal((await fetch(f.url+readinessPath)).status,503);
    finish();
    assert.equal((await fetch(f.url+readinessPath)).status,204);
    await fetch(f.url+'/index.html?fresh=1');assert.equal(warmed.length,2);
  }finally{finish();await f.close();}
});

test('a failed preparation reports failure without replacing the application HTML',async()=>{
  const f=await fixture({async transformRequest(){throw Error('synthetic syntax failure');},async waitForRequestsIdle(){throw Error('must not wait after failure');}});
  try{assert.equal(await(await fetch(f.url)).text(),'existing application asset');assert.equal((await fetch(f.url+readinessPath)).status,500);assert.ok(f.errors.some(e=>e.includes('synthetic syntax failure')));}finally{await f.close();}
});

test('unsupported Vite server APIs fail before middleware is installed',()=>{
  assert.throws(()=>nativeStartup(['/src/main.tsx']).configureServer({environments:{client:{}},httpServer:{},middlewares:{use(){throw Error('must not install');}}}),/module readiness support/);
});
