/* Local preview only. No cookies, no telemetry, no state writes. */
import {createServer} from "node:http";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {dirname,join} from "node:path";
const root=dirname(fileURLToPath(import.meta.url));
const files=new Map([
 ["/",["index.html","text/html; charset=utf-8"]],
 ["/index.html",["index.html","text/html; charset=utf-8"]],
 ["/style.css",["style.css","text/css; charset=utf-8"]],
 ["/app.mjs",["app.mjs","text/javascript; charset=utf-8"]],
 ["/engine.mjs",["engine.mjs","text/javascript; charset=utf-8"]],
 ["/catalog.v0.1.json",["catalog.v0.1.json","application/json; charset=utf-8"]]
]);
const port=Number(process.env.PORT||8787);
const host="127.0.0.1";
const app=createServer(async(req,res)=>{
 const pathname=(req.url||"/").split("?")[0];
 const item=files.get(pathname);
 res.setHeader("Cache-Control","no-store");
 res.setHeader("X-Content-Type-Options","nosniff");
 res.setHeader("Referrer-Policy","no-referrer");
 if(req.method!=="GET"&&req.method!=="HEAD"){res.writeHead(405).end();return}
 if(!item){res.writeHead(404).end();return}
 try{
  const bytes=await readFile(join(root,item[0]));
  res.writeHead(200,{"Content-Type":item[1],"Content-Length":bytes.byteLength});
  res.end(req.method==="HEAD"?undefined:bytes);
 }catch(e){res.writeHead(500).end()}
});
app.listen(port,host,()=>process.stdout.write("Local anonymous game preview: http://"+host+":"+port+"/\n"));