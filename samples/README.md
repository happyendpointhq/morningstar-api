# Sample responses

The API's public documentation has no example responses, so these are **live responses
from 20 October 2026**, saved as files.

| File | Request | Notes |
|---|---|---|
| `stock_details.json` | `GET /stock/details?ticker=AAPL&exchange=xnas` | Trimmed: only the first link, two competitors, no news, stories or industry peers, layout hints (column widths, sort order) removed, and the two premium sections (status `401`) reduced to their status. |
| `stock_real-time.json` | `GET /stock/real-time?performanceId=0P000003MH` | Microsoft, during US market hours. Unchanged. |

They are useful for writing parsers and tests before you subscribe. Prices and ratios
change constantly, so do not hard-code these values.
