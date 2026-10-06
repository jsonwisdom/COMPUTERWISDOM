import fs from 'node:fs';

const dir = 'school-of-wisdom';
const source = fs.readFileSync(`${dir}/updates.jsonl`, 'utf8').trim().split(/\r?\n/).filter(Boolean);
const items = source.map((line, i) => {
  try { return JSON.parse(line); }
  catch (e) { throw new Error(`Invalid JSONL at line ${i+1}: ${e.message}`); }
});

if (!items.length) throw new Error('updates.jsonl must contain at least one update');
const ids = new Set();
for (const item of items) {
  if (!item.id || !item.published_at || !item.title) throw new Error('Each update requires id, published_at, title');
  if (ids.has(item.id)) throw new Error(`Duplicate update id: ${item.id}`);
  ids.add(item.id);
}
for (let i=1;i<items.length;i++) {
  if (new Date(items[i].published_at) < new Date(items[i-1].published_at)) {
    throw new Error(`Append order regression: ${items[i].id}`);
  }
}

const latest = items.at(-1);
fs.writeFileSync(`${dir}/latest.json`, JSON.stringify(latest, null, 2) + '\n');

const home='https://jsonwisdom.github.io/COMPUTERWISDOM/school-of-wisdom/';
const feed={
  version:'https://jsonfeed.org/version/1.1',
  title:'School of Wisdom Updates',
  home_page_url:home,
  feed_url:home+'feed.json',
  items:[...items].reverse().slice(0,50).map(x=>({
    id:x.id,url:home,title:x.title,date_published:new Date(x.published_at).toISOString(),content_text:x.summary||''
  }))
};
fs.writeFileSync(`${dir}/feed.json`, JSON.stringify(feed, null, 2) + '\n');

const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const entries=[...items].reverse().slice(0,50).map(x=>`  <entry>
    <id>${esc(x.id)}</id>
    <title>${esc(x.title)}</title>
    <updated>${new Date(x.published_at).toISOString()}</updated>
    <link href="${home}"/>
    <summary>${esc(x.summary||'')}</summary>
  </entry>`).join('\n');
const xml=`<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>School of Wisdom Updates</title>
  <id>${home}</id>
  <link href="${home}feed.xml" rel="self"/>
  <link href="${home}"/>
  <updated>${new Date(latest.published_at).toISOString()}</updated>
${entries}
</feed>
`;
fs.writeFileSync(`${dir}/feed.xml`, xml);
console.log(`School of Wisdom built from ${items.length} append-only update(s); latest=${latest.id}`);
