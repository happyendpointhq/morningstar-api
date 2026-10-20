// Morningstar API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs AAPL xnas

const HOST = 'morningstar13.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Morningstar API ${res.status}: ${await res.text()}`);
  return res.json();
}

// Each section of /stock/details has its own status; premium ones come back 401.
const section = (details, name) =>
  details.components?.[name]?.status === 200 ? details.components[name].payload : null;

const [ticker = 'AAPL', exchange = 'xnas'] = process.argv.slice(2);
const details = await get('/stock/details', { ticker, exchange });
const { page } = details;
console.log(`${page.name} (${page.exchange}:${page.ticker}) performanceID ${page.performanceID}`);

const stats = section(details, 'keyStatistics')?.dataPoints ?? {};
for (const point of Object.values(stats)) {
  if (typeof point.value !== 'number' || point.locked) continue;
  const suffix = point.unit === 'percent' ? '%' : '';
  console.log(`  ${point.name.padEnd(28)} ${point.value.toFixed(2)}${suffix}`);
}
