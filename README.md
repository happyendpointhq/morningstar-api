# Morningstar API and Scraper

The Morningstar API returns Morningstar research data as JSON: real-time stock quotes,
company profiles, valuation, profitability and financial strength ratios against
competitors, financial statements, trailing returns, dividends and splits, ownership,
ESG sustainability data, earnings call transcripts, news, and market data for
commodities, currencies, indexes and sectors. It is a REST API, so you can use
Morningstar data in your own code without writing or maintaining a Morningstar scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/morningstar?utm_source=github&utm_medium=readme&utm_campaign=morningstar-api).
It is a data API, not investment advice.

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/morningstar13
- Product page: https://happyendpoint.com/library/morningstar?utm_source=github&utm_medium=readme&utm_campaign=morningstar-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://morningstar13.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 21, all `GET` |
| Identifiers | `ticker` plus `exchange` (for example `AAPL` and `xnas`), or Morningstar's `performanceId` (`0P000000GY`) |
| Format | JSON, in Morningstar's own data point structure |

---

## What data you get

**Stocks**
- Overview page: identifiers, company profile, sector, industry, style box, employees, key statistics, competitors, news
- Real-time quote: last price, change, bid and ask, open, high, low, volume, 52-week range, market cap, trading status
- Chart data and news, with full news articles

**Fundamentals and research**
- Financial statements: income statement, balance sheet and cash flow, annual or quarterly, original or restated
- Key metrics: summary, growth, profitability, financial health and cash flow
- Valuations, trailing returns (day, month, quarter), dividends and splits
- Fair value chart and table, sustainability assessment and breakdown
- Earnings call transcripts
- Ownership (major, concentrated, buying, selling; mutual funds or institutions) and insider transaction charts

**Markets**
- Commodities, currencies and indexes
- Market movers, sector performance over 3 months to 10 years
- Calendars: earnings, economic releases, IPOs and splits

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/morningstar13). Copy
`.env.example` to `.env` and paste your key.

### 2. Make a request

`/stock/details` takes a ticker and exchange and returns the `performanceID` that the other
research endpoints take:

```bash
curl "https://morningstar13.p.rapidapi.com/stock/details?ticker=AAPL&exchange=xnas" \
  -H "x-rapidapi-host: morningstar13.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://morningstar13.p.rapidapi.com/stock/real-time?performanceId=0P000000GY" \
  -H "x-rapidapi-host: morningstar13.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py apple
```

```python
from client import component, fmt, get

details = get("/stock/details", ticker="AAPL", exchange="xnas")
performance_id = details["page"]["performanceID"]

stats = component(details, "keyStatistics")["dataPoints"]
print(fmt(stats["priceToEarnings[normalized]"]), fmt(stats["dividendYield[trailing]"]))

quote = get("/stock/real-time", performanceId=performance_id)[performance_id]
print(quote["lastPrice"]["value"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs AAPL xnas
```

---

## Example response

Part of `GET /stock/real-time?performanceId=0P000003MH` (Microsoft), from a live call on
20 October 2026 during market hours. The full responses are in [`samples/`](samples/).

```json
{
  "0P000003MH": {
    "lastPrice": {
      "value": 528.83,
      "date": { "value": "2026-10-20T09:50:07-04:00" },
      "currency": { "value": "USD" },
      "exchange": { "value": "XCBO" }
    },
    "percentNetChange": { "value": -0.8939 },
    "previousClosePrice": {
      "value": 533.52,
      "date": { "value": "2026-10-19" },
      "exchange": { "value": "XNAS" }
    },
    "volume": {
      "value": 726951,
      "date": { "value": "2026-10-20T09:35:08-04:00" },
      "exchange": { "value": "XNAS" }
    },
    "yearHighPrice": { "value": 553.5, "date": { "value": "2025-10-28" } },
    "marketCap": { "value": 3963013628546.7, "currency": { "value": "USD" } },
    "tradingStatus": { "value": "Open" }
  }
}
```

---

## Endpoints

Base URL: `https://morningstar13.p.rapidapi.com`

### Search and stock overview

| Endpoint | Returns |
|---|---|
| `GET /auto-complete` | Companies, funds and ETFs matching a query |
| `GET /stock/details` | The stock's overview page: identifiers, profile, key statistics, competitors, news |
| `GET /stock/real-time` | Real-time quote by `performanceId` |
| `GET /stock/chart` | Price chart data |
| `GET /stock/news` | News for a stock |
| `GET /news/details` | One full news article by its Morningstar URL path |

### Fundamentals and research

| Endpoint | Returns |
|---|---|
| `GET /stock/financials` | Income statement, balance sheet or cash flow; annual or quarterly; original or restated |
| `GET /stock/key-metrics` | Summary, growth, profitability, health or cash flow metrics |
| `GET /stock/valuations` | Valuation history |
| `GET /stock/fair-value` | Fair value chart or table |
| `GET /stock/trailing-return` | Trailing returns by day, month or quarter |
| `GET /stock/dividends` | Dividends or splits |
| `GET /stock/sustainability` | Sustainability assessment or breakdown |
| `GET /stock/earning-transcript` | Earnings call transcript |
| `GET /stock/ownership` | Major, concentrated, buying or selling holders; mutual funds or institutions |
| `GET /stock/executive` | Key executives, board, insider transaction chart and history |

### Markets

| Endpoint | Returns |
|---|---|
| `GET /market/data` | Commodities, currencies or indexes |
| `GET /market/movers` | Market movers |
| `GET /market/sectors` | One sector's performance over 3 months to 10 years |
| `GET /market/calendar` | Earnings, economic releases, IPOs or splits for a date |
| `GET /health` | Service health |

---

## Things to know about the data

These come from running the examples against the live API. They are the mistakes that
produce wrong numbers rather than errors.

- **Each section of `/stock/details` has its own status.** The response holds sections such
  as `profile`, `keyStatistics` and `valuationVsBenchmarks`, each with a `status` and a
  `payload`. In our test, `companyReport` and `priceToFairValueSummary` came back with
  status `401`: they are Morningstar premium content. Check the status before reading a
  payload; `client.component()` does this.
- **Locked values are placeholders.** Premium data points such as the Morningstar Rating
  for Stocks carry `"locked": true` and a value that is not the real figure (a competitor's
  1 to 5 star rating showed `64`). Ignore any point with `locked` set; `client.value()`
  returns `None` for them.
- **Every number is a data point object.** Values sit in `.value`, next to `name`, `unit`
  and the date they apply to. Keys can include the variation in brackets:
  `priceToEarnings[normalized]`, `dividendYield[trailing]`, `dividendYield[forward]`.
- **Percentages are already in percent.** A point with `"unit": "percent"` and value `0.3091`
  is a 0.31% dividend yield, not 30.91%. Return on equity of `158.755` is 158.8%.
- **"Vs benchmarks" means vs competitors.** `valuationVsBenchmarks`,
  `profitabilityVsBenchmarks` and `financialStrengthVsBenchmarks` hold one row for the stock
  and one for each competitor Morningstar lists, labelled by ticker. For Apple the
  competitors were Samsung (`005930` on `XKRX`, prices in KRW) and Microsoft, not an index.
  `peer_compare.py` prints these side by side.
- **Some fields are simply absent.** Apple's financial strength row had no
  `interestCoverage` value while its competitors did. Treat a missing key as unknown, not
  zero.
- **The real-time quote mixes venues and times.** It is keyed by `performanceID`, and each
  field carries its own exchange and timestamp. During US market hours, `lastPrice`,
  bid, ask and the day's range came from `XCBO` (Cboe) while `previousClosePrice` and
  `volume` came from `XNAS`, and the volume timestamp was 15 minutes behind the last price.
  Read the timestamps before you compare fields.
- **Identifier casing differs between request and response.** Requests take
  `performanceId` and lower-case exchange codes (`xnas`, `xnys`); responses return
  `performanceID` and upper-case codes (`XNAS`).

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Finds a stock by name with `/auto-complete`, then its overview, key statistics and real-time quote |
| [`examples/python/peer_compare.py`](examples/python/peer_compare.py) | Valuation, profitability and financial strength against competitors, from one call |
| [`examples/python/key_stats_to_csv.py`](examples/python/key_stats_to_csv.py) | Key statistics for a list of stocks to CSV, one call per stock |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | Overview and key statistics in Node 18+, no dependencies |
| [`samples/`](samples/) | Live responses for `/stock/details` and `/stock/real-time` |

---

## API or your own Morningstar scraper

Morningstar pages are built from the same data point structure this API returns, and a
homemade scraper has to follow it through every page change, sign-in prompt and premium
gate. This API gives you the data as JSON with one key, so the work you keep is the
analysis. For a recurring bulk export rather than API calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=morningstar-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Morningstar
data without code:

```json
{
  "mcpServers": {
    "morningstar": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: morningstar13.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Does Morningstar have an API?

Morningstar licenses its data to institutions through its own products, such as Morningstar
Direct and its data feeds, priced through its sales team. It has no free self-serve
developer API. This API, built and maintained by Happy Endpoint and independent of
Morningstar, gives developers REST and JSON access.

### Is there a free Morningstar API?

Yes. The [RapidAPI listing](https://rapidapi.com/happyendpoint/api/morningstar13) has a free plan, and every endpoint can be tried on it.

### How do I use the Morningstar API in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI
headers. [`examples/python/client.py`](examples/python/client.py) has the client plus
helpers for Morningstar's section and data point structure.

### Where is the Morningstar API documentation?

Every endpoint and parameter is documented on the RapidAPI listing, and the endpoint table
above summarises them. Live example responses are in [`samples/`](samples/).

### Can I get Morningstar fund and ETF data?

`/auto-complete` searches companies, funds and ETFs and returns each match's ticker,
exchange, ISIN and performanceID. The research endpoints in this repo were tested on
stocks; try a fund's `performanceId` on the free plan to see which sections it returns.

### Can I get financial statements and earnings call transcripts?

Yes. `/stock/financials` returns the income statement, balance sheet or cash flow,
annual or quarterly, and `/stock/earning-transcript` returns the call transcript, both by
`performanceId`.

### Is this investment advice?

No. It is a data API. What you do with the numbers is your own decision.

---

## Related repos

- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment research
- [happyendpoint-mcp](https://github.com/happyendpointhq/happyendpoint-mcp) - MCP server for Happy Endpoint data in Claude and Cursor
- [awesome-ecommerce-data-apis](https://github.com/happyendpointhq/awesome-ecommerce-data-apis) - product, pricing and retail data APIs

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
